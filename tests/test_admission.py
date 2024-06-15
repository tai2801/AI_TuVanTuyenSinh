import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import entities as ent
from app.chatbot import Chatbot
from app.knowledge import KnowledgeBase
from app.preprocess import normalize, strip_accents
from app.train import load_model

KB = KnowledgeBase()
BOT = Chatbot(KB, load_model())


# ---------- preprocessing ----------
def test_strip_accents():
    assert strip_accents("Học phí đại học") == "Hoc phi dai hoc"


def test_normalize_abbr():
    assert "cong nghe thong tin" in normalize("học phí CNTT bao nhiêu")
    assert "ky tuc xa" in normalize("KTX giá sao")


def test_normalize_empty():
    assert normalize("") == ""
    assert normalize(None) == ""


# ---------- entities ----------
def test_extract_major_exact():
    assert ent.extract_majors("học phí ngành công nghệ thông tin", KB) == ["CNTT"]


def test_extract_major_abbr():
    assert "MKT" in ent.extract_majors("nganh mkt hoc phi bao nhieu", KB)


def test_extract_major_two_for_compare():
    ms = ent.extract_majors("so sánh kế toán và tài chính ngân hàng", KB)
    assert set(ms) == {"KETO", "TCNH"}


def test_extract_combo_year():
    assert ent.extract_combo("em thi khối A01 năm 2024") == "A01"
    assert ent.extract_year("điểm chuẩn năm 2022") == 2022


# ---------- chatbot logic ----------
def test_tuition_with_major_has_source():
    r = BOT.reply("t1", "Học phí ngành công nghệ thông tin bao nhiêu?")
    assert r["intent"] == "hoi_hoc_phi"
    assert "28.000.000" in r["reply"]
    assert r["source"] and "MINH HỌA" in r["source"].upper() or r["source"]


def test_tuition_missing_major_asks_back_then_slot_fills():
    r1 = BOT.reply("s-slot", "Học phí bao nhiêu một năm?")
    assert "ngành nào" in r1["reply"]
    r2 = BOT.reply("s-slot", "Marketing")
    assert r2["intent"] == "hoi_hoc_phi"
    assert "25.000.000" in r2["reply"]


def test_out_of_scope_fallback():
    r = BOT.reply("t2", "Thời tiết hôm nay thế nào?")
    assert r["fallback"] is True


def test_compare_two_majors():
    r = BOT.reply("t3", "So sánh ngành công nghệ thông tin và khoa học máy tính")
    assert r["intent"] == "so_sanh_nganh"
    assert r["data"] and r["data"]["compare"]
    assert "30.000.000" in r["reply"] and "28.000.000" in r["reply"]


def test_suggest_by_interest():
    r = BOT.reply("t4", "Em thích lập trình và máy tính, giỏi toán, nên học ngành gì?")
    assert r["intent"] == "goi_y_nganh"
    assert r["data"]["suggested"]
    assert "CNTT" in r["data"]["suggested"]


def test_benchmark_with_year():
    r = BOT.reply("t5", "Điểm chuẩn ngành marketing năm 2022 là bao nhiêu?")
    assert r["intent"] == "diem_chuan"
    assert "22.25" in r["reply"]


def test_combo_lookup():
    r = BOT.reply("t6", "Ngành ngôn ngữ Anh xét tổ hợp nào?")
    assert r["intent"] == "to_hop_xet_tuyen"
    assert "D01" in r["reply"]


def test_methods_listed():
    r = BOT.reply("t7", "Trường có những phương thức xét tuyển nào?")
    assert r["intent"] == "phuong_thuc_xet_tuyen"
    assert "học bạ" in r["reply"].lower()
