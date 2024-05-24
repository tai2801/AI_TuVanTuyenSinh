# TEST REPORT – Admission AI Chatbot

Ngày chạy: 15/06/2024 · Môi trường: Windows 10, Python 3.11, FastAPI, scikit-learn, pytest, httpx.

## 1. Huấn luyện mô hình
```
python -m app.train
-> Da huan luyen: 104 mau, 14 intent -> models/intent_model.pkl (208 KB)
```

## 2. Đánh giá trên tập kiểm tra độc lập (`scripts/evaluate.py`, 48 câu)
- Accuracy: **48/48 = 1.000**.
- Fallback đúng trên 6 câu ngoài phạm vi: **6/6**.
- Theo intent: 14/14 intent đạt tối đa trên tập kiểm tra; không có nhầm lẫn.
- Tập kiểm tra gồm câu không dấu, viết tắt (`"hoc phi nganh tri tue nhan tao bn 1 nam"`), diễn đạt khác tập huấn luyện và 6 câu ngoài phạm vi (thời tiết, giá xăng, bóng đá...).

## 3. Pytest (`tests/test_admission.py`) – 15/15 PASS
Bao phủ: bỏ dấu/chuẩn hóa viết tắt/rỗng; trích xuất ngành (chính xác, viết tắt, 2 ngành để so sánh); tổ hợp + năm; học phí kèm nguồn; slot filling hỏi lại rồi bổ sung; fallback ngoài phạm vi; so sánh 2 ngành có số liệu; gợi ý ngành theo sở thích ra CNTT; điểm chuẩn theo năm; tổ hợp; phương thức.

## 4. Kiểm thử tích hợp API (uvicorn + curl)
- `GET /health` -> ok, 12 ngành, 14 intent.
- `POST /chat` `"Học phí ngành công nghệ thông tin bao nhiêu?"` -> intent `hoi_hoc_phi`, confidence 0.905, trả `28.000.000đ/năm` kèm `source` minh họa.
- `POST /chat` không dấu `"diem chuan nganh marketing nam 2023"` -> `diem_chuan`, điểm `22.75`.
- `POST /chat` `"Giá vàng hôm nay bao nhiêu?"` -> `fallback=true`, intent `ngoai_pham_vi`.
- `POST /chat` so sánh kế toán vs tài chính – ngân hàng -> bảng so sánh kèm `data.compare`.
- `GET /api/admin/stats` không token -> 401; có token -> thống kê đúng intent + câu fallback.
- `POST/DELETE /api/admin/majors` (CRUD) hoạt động; số ngành trở về 12 sau khi xóa bản ghi test.
- Trang `/` và `/admin` -> HTTP 200.
