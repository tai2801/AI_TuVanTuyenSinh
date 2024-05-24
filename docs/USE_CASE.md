# Use Case

Actors: **Thí sinh/Phụ huynh** (chat, tra cứu, nhận gợi ý), **Quản trị viên tuyển sinh** (CRUD dữ liệu, xem thống kê).

| UC | Tên | Luồng chính |
|----|-----|-------------|
| UC1 | Hỏi đáp tuyển sinh | Người dùng nhập câu -> phân loại intent -> trích entity -> trả lời + nguồn + gợi ý tiếp |
| UC2 | Tra cứu học phí/điểm chuẩn | Như UC1; nếu thiếu ngành -> bot hỏi lại (slot filling), người dùng bổ sung tên ngành |
| UC3 | Gợi ý ngành | Người dùng nêu sở thích/môn mạnh -> chấm điểm liên quan -> trả top 3 kèm lý do |
| UC4 | So sánh 2 ngành | Nhận diện 2 ngành -> bảng so sánh + nhận xét chênh học phí |
| UC5 | Hỏi ngoài phạm vi | Confidence thấp/intent ngoai_pham_vi -> fallback xin lỗi + gợi ý câu hỏi trong phạm vi |
| UC6 | Quản trị dữ liệu | Admin gửi token -> thêm/sửa/xóa ngành, FAQ (ghi vào JSON dữ liệu) |
| UC7 | Thống kê | Admin xem phân bố intent, câu hỏi thường gặp, danh sách câu fallback để bổ sung dữ liệu |

Luồng phụ UC1: câu không dấu/viết tắt được chuẩn hóa trước khi phân loại; câu chứa tổ hợp (A01)
mà không có ngành -> trả danh sách ngành xét tổ hợp đó.
