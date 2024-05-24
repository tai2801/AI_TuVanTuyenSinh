# Activity & Sequence (luồng đặt câu hỏi – tra cứu học phí)

## Activity
1. Người dùng nhập câu hỏi -> 2. Chuẩn hóa văn bản -> 3. Phân loại intent + confidence
-> 4a. confidence < 0.45 hoặc intent ngoài phạm vi -> fallback + gợi ý.
-> 4b. Đủ tin cậy -> 5. Trích entity -> 6a. Thiếu ngành -> hỏi lại, lưu pending theo session.
-> 6b. Đủ entity -> 7. Truy vấn KnowledgeBase -> 8. Trả lời + source + gợi ý câu tiếp -> 9. Lưu lịch sử.

## Sequence
```
User -> Frontend: gui cau hoi
Frontend -> API POST /chat: {session_id, message}
API -> Chatbot: reply(session, message)
Chatbot -> Model: predict_proba -> (intent, confidence)
Chatbot -> Entities: extract_majors/combo/year
Chatbot -> KnowledgeBase: get_major(code) / faq_by_topic(...)
KnowledgeBase --> Chatbot: du lieu + source
Chatbot --> API: {reply, intent, confidence, entities, source, suggestions}
API -> DB: save user + assistant (kem intent/fallback)
API --> Frontend: JSON
Frontend -> User: hien bong chat + chip goi y
```
