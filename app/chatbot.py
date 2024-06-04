"""Engine hoi dap tuyen sinh: intent -> entity -> sinh cau tra loi tu du lieu minh hoa.

Moi con so (hoc phi, diem chuan, chi tieu) deu lay tu
KnowledgeBase va kem truong `source`. Bot khong tu bia so lieu.
"""
from . import entities as ent
from .preprocess import normalize

CONFIDENCE_THRESHOLD = 0.45

SUGGESTIONS = {
    "hoi_hoc_phi": ["Điểm chuẩn ngành này năm 2023?", "Ngành này xét tổ hợp nào?", "Có học bổng đầu vào không?"],
    "diem_chuan": ["Học phí ngành này bao nhiêu một năm?", "Có xét học bạ không?", "So sánh ngành này với ngành khác"],
    "to_hop_xet_tuyen": ["Điểm chuẩn ngành này năm 2023?", "Học phí ngành này bao nhiêu?"],
    "goi_y_nganh": ["So sánh hai ngành gợi ý đầu tiên", "Học phí các ngành gợi ý", "Điểm chuẩn các ngành gợi ý"],
    "_default": ["Học phí ngành Công nghệ thông tin?", "Trường có những phương thức xét tuyển nào?", "Tư vấn ngành theo sở thích", "Ký túc xá giá bao nhiêu?"],
}

SUBJECT_NAMES = {"toan": "Toán", "ly": "Lý", "hoa": "Hóa", "van": "Văn", "anh": "Anh",
                 "sinh": "Sinh", "tin": "Tin học"}


def fmt_money(v):
    return f"{v:,}".replace(",", ".") + "đ"


class Chatbot:
    def __init__(self, kb, model):
        self.kb = kb
        self.model = model
        self.pending = {}  # session_id -> {"intent":..., "majors":[...]}

    # ---------- du doan intent ----------
    def predict(self, text):
        proba = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        best = int(proba.argmax())
        return classes[best], float(proba[best])

    # ---------- goi y nganh ----------
    def suggest_majors(self, text, top=3):
        t = normalize(text)
        scored = []
        for m in self.kb.majors:
            score, reasons = 0, []
            for kw in m.get("interests", []):
                if normalize(kw) in t:
                    score += 2
                    reasons.append(f"hợp sở thích “{kw}”")
            for s in m.get("strong_subjects", []):
                if f" {s} " in f" {t} " or f"mon {s}" in t or f"giỏi {s}" in t or f"gioi {s}" in t:
                    score += 1
                    reasons.append(f"phù hợp thế mạnh môn {SUBJECT_NAMES.get(s, s)}")
            if score:
                scored.append((score, m, reasons))
        scored.sort(key=lambda x: (-x[0], x[1]["name"]))
        return scored[:top]

    # ---------- xu ly chinh ----------
    def reply(self, session_id, text):
        intent, conf = self.predict(text)
        majors = ent.extract_majors(text, self.kb)
        combo = ent.extract_combo(text)
        year = ent.extract_year(text)
        result = {"intent": intent, "confidence": round(conf, 3),
                  "entities": {"majors": majors, "combo": combo, "year": year},
                  "fallback": False, "source": None, "data": None,
                  "suggestions": SUGGESTIONS.get(intent, SUGGESTIONS["_default"])}

        # Slot filling: cau tra loi cho cau hoi truoc dang cho bo sung nganh.
        # Cau bo sung ngan (chi ten nganh) thuong co confidence thap nen phai
        # uu tien ngu canh pending TRUOC khi ap nguong fallback.
        pend = self.pending.pop(session_id, None)
        pend_applied = False
        if pend and majors:
            intent = pend["intent"]
            pend_applied = True
            result["intent"] = intent
            result["suggestions"] = SUGGESTIONS.get(intent, SUGGESTIONS["_default"])
            if intent == "so_sanh_nganh":
                majors = list(dict.fromkeys(pend.get("majors", []) + majors))
                result["entities"]["majors"] = majors

        if not pend_applied and (conf < CONFIDENCE_THRESHOLD or intent == "ngoai_pham_vi"):
            result["fallback"] = True
            result["reply"] = ("Xin lỗi, câu hỏi này nằm ngoài phạm vi tư vấn tuyển sinh của mình "
                               "(ngành học, học phí, điểm chuẩn, phương thức xét tuyển...). "
                               "Bạn thử hỏi theo các gợi ý bên dưới, hoặc liên hệ Phòng Tuyển sinh để được hỗ trợ.")
            return result

        handler = getattr(self, f"_h_{intent}", None)
        if handler is None:
            result["fallback"] = True
            result["reply"] = "Mình chưa có dữ liệu cho nội dung này. Bạn thử hỏi về ngành học, học phí hoặc điểm chuẩn nhé."
            return result
        out = handler(session_id, text, majors, combo, year)
        result.update(out)
        return result

    # ---------- helpers ----------
    def _ask_major(self, session_id, intent, majors, question):
        self.pending[session_id] = {"intent": intent, "majors": majors}
        names = ", ".join(m["name"] for m in self.kb.majors[:6])
        return {"reply": f"{question}\nHiện trường có {len(self.kb.majors)} ngành, ví dụ: {names}... Bạn chỉ cần gõ tên ngành là được."}

    def _major_or_ask(self, session_id, intent, majors, question):
        if not majors:
            return None, self._ask_major(session_id, intent, majors, question)
        return self.kb.get_major(majors[0]), None

    # ---------- handlers ----------
    def _h_chao_hoi(self, sid, text, majors, combo, year):
        return {"reply": "Chào bạn! Mình là trợ lý tư vấn tuyển sinh của Đại học Công nghệ Á Châu (ACU – dữ liệu minh họa). "
                         "Bạn muốn hỏi về ngành học, học phí, điểm chuẩn hay phương thức xét tuyển?"}

    def _h_cam_on(self, sid, text, majors, combo, year):
        return {"reply": "Không có gì! Chúc bạn chọn được ngành phù hợp. Cần hỏi thêm về tuyển sinh cứ nhắn mình nhé."}

    def _h_hoi_hoc_phi(self, sid, text, majors, combo, year):
        m, ask = self._major_or_ask(sid, "hoi_hoc_phi", majors, "Bạn muốn hỏi học phí của ngành nào?")
        if ask:
            return ask
        return {"reply": f"Học phí ngành {m['name']} là {fmt_money(m['tuition_per_year'])}/năm (minh họa, áp dụng 2024). "
                         f"Học phí có thể điều chỉnh nhẹ theo lộ trình công bố từng năm.",
                "source": m["source"], "data": {"major": m["code"], "tuition_per_year": m["tuition_per_year"]}}

    def _h_diem_chuan(self, sid, text, majors, combo, year):
        m, ask = self._major_or_ask(sid, "diem_chuan", majors, "Bạn muốn xem điểm chuẩn của ngành nào?")
        if ask:
            return ask
        y = year or 2023
        score = m["benchmark_scores"].get(str(y))
        hist = ", ".join(f"{k}: {v}" for k, v in sorted(m["benchmark_scores"].items()))
        if score is None:
            return {"reply": f"Mình chưa có điểm chuẩn minh họa năm {y} của ngành {m['name']}. Dữ liệu hiện có: {hist}.",
                    "source": m["source"]}
        return {"reply": f"Điểm chuẩn (minh họa) ngành {m['name']} năm {y} là {score} điểm. Lịch sử 3 năm: {hist}. "
                         f"Lưu ý điểm chuẩn thay đổi theo năm và số lượng thí sinh.",
                "source": m["source"], "data": {"major": m["code"], "year": y, "score": score}}

    def _h_to_hop_xet_tuyen(self, sid, text, majors, combo, year):
        if majors:
            m = self.kb.get_major(majors[0])
            ok = f" Ngành xét tổ hợp {combo}: {'CÓ' if combo in m['combos'] else 'KHÔNG'}." if combo else ""
            return {"reply": f"Ngành {m['name']} xét tuyển các tổ hợp: {', '.join(m['combos'])}.{ok}",
                    "source": m["source"], "data": {"major": m["code"], "combos": m["combos"]}}
        if combo:
            ms = [m for m in self.kb.majors if combo in m["combos"]]
            names = ", ".join(m["name"] for m in ms)
            return {"reply": f"Tổ hợp {combo} xét tuyển được {len(ms)} ngành: {names}. Bạn quan tâm ngành nào trong số này?",
                    "data": {"combo": combo, "majors": [m["code"] for m in ms]}}
        return self._ask_major(sid, "to_hop_xet_tuyen", majors,
                               "Bạn muốn xem tổ hợp xét tuyển của ngành nào? (Hoặc gõ mã tổ hợp, ví dụ A01, để xem các ngành xét tổ hợp đó.)")

    def _h_phuong_thuc_xet_tuyen(self, sid, text, majors, combo, year):
        t = normalize(text)
        chosen = None
        for meth in self.kb.methods:
            keys = {"THPT": ["thi thpt", "diem thi"], "HOCBA": ["hoc ba"],
                    "DGNL": ["danh gia nang luc", "dgnl"], "XTT": ["xet tuyen thang", "tuyen thang"]}
            if any(k in t for k in keys.get(meth["code"], [])):
                chosen = meth
                break
        if chosen:
            return {"reply": f"Phương thức {chosen['name']}: {chosen['description']} Điều kiện: {chosen['condition']} Thời gian: {chosen['timeline']}",
                    "source": chosen["source"], "data": {"method": chosen["code"]}}
        lines = "\n".join(f"- {m['name']}: {m['condition']}" for m in self.kb.methods)
        return {"reply": f"Năm 2024 (minh họa), ACU áp dụng {len(self.kb.methods)} phương thức xét tuyển:\n{lines}\nBạn muốn tìm hiểu kỹ phương thức nào?",
                "source": self.kb.methods[0]["source"]}

    def _h_goi_y_nganh(self, sid, text, majors, combo, year):
        scored = self.suggest_majors(text)
        if not scored:
            return {"reply": "Để gợi ý đúng ngành, bạn cho mình biết thêm: bạn thích làm việc gì "
                             "(ví dụ lập trình, kinh doanh, vẽ, tài chính...) và học tốt môn nào (Toán, Anh, Văn, Lý...)?"}
        lines = []
        for score, m, reasons in scored:
            lines.append(f"- {m['name']} (học phí {fmt_money(m['tuition_per_year'])}/năm, điểm chuẩn 2023 minh họa {m['benchmark_scores'].get('2023')}): "
                         + "; ".join(dict.fromkeys(reasons)) + ".")
        return {"reply": "Dựa trên sở thích/môn mạnh bạn nêu, mình gợi ý:\n" + "\n".join(lines),
                "source": self.kb.majors[0]["source"],
                "data": {"suggested": [m["code"] for _, m, _ in scored]}}

    def _h_so_sanh_nganh(self, sid, text, majors, combo, year):
        majors = list(dict.fromkeys(majors))
        if len(majors) < 2:
            return self._ask_major(sid, "so_sanh_nganh", majors,
                                   "Bạn muốn so sánh ngành nào với ngành nào? Hãy nêu tên 2 ngành, ví dụ: “so sánh Công nghệ thông tin và Khoa học máy tính”.")
        a, b = self.kb.get_major(majors[0]), self.kb.get_major(majors[1])
        diff = a["tuition_per_year"] - b["tuition_per_year"]
        rows = [
            ["Tiêu chí", a["name"], b["name"]],
            ["Học phí/năm", fmt_money(a["tuition_per_year"]), fmt_money(b["tuition_per_year"])],
            ["Điểm chuẩn 2023 (minh họa)", a["benchmark_scores"].get("2023"), b["benchmark_scores"].get("2023")],
            ["Tổ hợp xét tuyển", ", ".join(a["combos"]), ", ".join(b["combos"])],
            ["Chỉ tiêu (minh họa)", a["quota"], b["quota"]],
            ["Mô tả", a["description"], b["description"]],
        ]
        note = (f"Học phí {a['name']} cao hơn {fmt_money(abs(diff))}/năm." if diff > 0 else
                f"Học phí {b['name']} cao hơn {fmt_money(abs(diff))}/năm." if diff < 0 else "Hai ngành có học phí bằng nhau.")
        text_rows = "\n".join(f"{r[0]}: {r[1]} | {r[2]}" for r in rows[1:])
        return {"reply": f"So sánh {a['name']} và {b['name']}:\n{text_rows}\n{note}",
                "source": a["source"], "data": {"compare": rows}}

    def _faq_reply(self, topic, sid):
        items = self.kb.faq_by_topic(topic)
        if not items:
            return {"reply": "Mình chưa có dữ liệu cho nội dung này trong bộ dữ liệu minh họa."}
        body = "\n".join(f"- {f['answer']}" for f in items)
        return {"reply": body, "source": items[0]["source"]}

    def _h_hoc_bong(self, sid, text, majors, combo, year):
        return self._faq_reply("hoc_bong", sid)

    def _h_ky_tuc_xa(self, sid, text, majors, combo, year):
        return self._faq_reply("ky_tuc_xa", sid)

    def _h_thoi_gian_tuyen_sinh(self, sid, text, majors, combo, year):
        r = self._faq_reply("thoi_gian", sid)
        methods = "; ".join(f"{m['name']}: {m['timeline']}" for m in self.kb.methods)
        r["reply"] += f"\nTheo phương thức: {methods}"
        return r

    def _h_ho_so_xet_tuyen(self, sid, text, majors, combo, year):
        return self._faq_reply("ho_so", sid)

    def _h_lien_he(self, sid, text, majors, combo, year):
        return self._faq_reply("lien_he", sid)
