# Architecture

```
[Frontend HTML/JS] --HTTP--> [FastAPI app.main]
                                 |
                                 +--> [Chatbot engine app.chatbot]
                                 |       +--> predict intent (model pkl: TF-IDF + LogisticRegression)
                                 |       +--> entities (tu dien nganh + fuzzy, regex to hop/nam)
                                 |       +--> KnowledgeBase (data/*.json, CRUD cho admin)
                                 +--> [SQLite app.db] lich su hoi thoai + thong ke
```

- `app/preprocess.py`: chuẩn hóa tiếng Việt (bỏ dấu, viết tắt, dấu câu).
- `app/entities.py`: trích xuất ngành (khớp chính xác theo độ dài giảm dần, sau đó fuzzy 0.86), tổ hợp, năm.
- `app/train.py`: huấn luyện và nạp mô hình; tự huấn luyện nếu chưa có file pkl.
- `app/chatbot.py`: điều phối intent -> handler; slot filling theo session; ngưỡng fallback 0.45.
- `app/knowledge.py`: nạp/ghi dữ liệu JSON, CRUD ngành/FAQ.
- `app/db.py`: SQLite lưu message (kèm intent/confidence/fallback) phục vụ thống kê.
- `app/main.py`: REST API + phục vụ frontend tĩnh; admin bảo vệ bằng header X-Admin-Token (demo).
