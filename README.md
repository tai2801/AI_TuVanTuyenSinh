# Admission AI Chatbot
## Chatbot tư vấn tuyển sinh đại học (môn Trí tuệ nhân tạo – HUIT)

Chatbot tiếng Việt tư vấn tuyển sinh cho trường giả định **Đại học Công nghệ Á Châu (ACU)**:
trả lời về ngành học, tổ hợp, phương thức xét tuyển, học phí, điểm chuẩn, học bổng, ký túc xá,
hồ sơ, thời gian tuyển sinh; gợi ý ngành theo sở thích; so sánh 2 ngành; hỏi lại khi thiếu thông tin;
fallback lịch sự khi câu hỏi ngoài phạm vi.

> ⚠️ **Toàn bộ số liệu tuyển sinh là DỮ LIỆU MINH HỌA** phục vụ đồ án (học phí, điểm chuẩn,
> chỉ tiêu, lịch). Mỗi câu trả lời định lượng đều kèm nguồn dữ liệu (`source`).

## Công nghệ
Python · FastAPI · scikit-learn (TF-IDF word+char n-gram + Logistic Regression) · SQLite · HTML/CSS/JS thuần.

## Cài đặt và chạy
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.train            # huấn luyện mô hình -> models/intent_model.pkl (có sẵn trong repo, chạy lại nếu đổi dữ liệu)
uvicorn app.main:app --port 8000
```
Mở http://localhost:8000 (trang chat) và http://localhost:8000/admin (quản trị/thống kê).

## API chính
| Method | Endpoint | Mô tả |
|---|---|---|
| GET | /health | Trạng thái, số ngành/intent |
| POST | /chat | {session_id, message} -> {reply, intent, confidence, entities, source, suggestions, fallback, data} |
| GET | /api/majors, /api/majors/{code} | Danh sách/chi tiết ngành |
| GET | /api/methods | Phương thức xét tuyển |
| GET | /api/history/{session_id} | Lịch sử hội thoại |
| GET | /api/admin/stats | Thống kê (cần header X-Admin-Token) |
| POST/DELETE | /api/admin/majors, /api/admin/faqs | CRUD dữ liệu tư vấn (cần token) |

Token admin demo: `admin-demo-123` (đổi bằng biến môi trường `ADMIN_TOKEN`, xem `.env.example`).
Đây chỉ là cơ chế demo cho đồ án, không dùng cho production.

## Kiểm thử và đánh giá
```bash
python -m pytest tests/ -q     # 15 test
python scripts/evaluate.py     # đánh giá trên 48 câu độc lập: accuracy, fallback, confusion
```
Kết quả đánh giá và kiểm thử: xem `docs/EVALUATION.md` và `docs/TEST_REPORT.md`.

## Cấu trúc
- `app/` – preprocess, entities, train, chatbot (engine), knowledge, db, main (FastAPI)
- `data/` – majors.json (12 ngành), admission_methods.json, faqs.json, training_data.json (104 mẫu/14 intent), test_set.json (48 câu)
- `frontend/` – trang chat + trang admin (HTML/CSS/JS thuần)
- `models/` – intent_model.pkl (~208 KB)
- `docs/` – Overview, Problem/FR/NFR, Use Case, Architecture, Activity/Sequence, Dataset, Model, Evaluation, Limitations, Test Report, Future, References
- `scripts/evaluate.py`, `tests/test_admission.py`

## Giấy phép
MIT License (xem `LICENSE`).
