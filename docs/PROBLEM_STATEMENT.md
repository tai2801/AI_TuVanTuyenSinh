# Problem Statement, Functional & Non-functional Requirements

## Problem Statement
Thí sinh và phụ huynh có nhiều câu hỏi lặp lại về tuyển sinh (học phí, điểm chuẩn, tổ hợp,
phương thức) ngoài giờ hành chính; đội tư vấn quá tải vào mùa tuyển sinh. Cần một chatbot
tiếng Việt trả lời tức thì dựa trên dữ liệu tuyển sinh có nguồn rõ ràng, không bịa số liệu.

## Functional Requirements
- FR1: Chat hỏi đáp tiếng Việt (có dấu/không dấu/viết tắt) qua API và giao diện web.
- FR2: Phân loại intent (>= 12 intent) kèm confidence; dưới ngưỡng 0.45 -> fallback + gợi ý câu hỏi.
- FR3: Trích xuất entity ngành, tổ hợp, năm; hỏi lại (slot filling) khi thiếu ngành.
- FR4: Tra cứu học phí, điểm chuẩn theo năm, tổ hợp, phương thức xét tuyển từ dữ liệu có `source`.
- FR5: Gợi ý ngành theo sở thích + môn học mạnh, kèm lý do.
- FR6: So sánh 2 ngành (học phí, điểm chuẩn, tổ hợp, chỉ tiêu, mô tả).
- FR7: Gợi ý câu hỏi tiếp theo sau mỗi câu trả lời.
- FR8: Lưu lịch sử hội thoại (SQLite), xem lại theo session.
- FR9: Admin CRUD ngành/FAQ qua API có token; thống kê intent, câu hỏi thường gặp, câu fallback.

## Non-functional Requirements
- NFR1: Trả lời < 1 giây trên máy thường cho 1 câu hỏi (mô hình nhẹ, không dùng deep learning nặng).
- NFR2: Không bịa số liệu: mọi con số lấy từ KnowledgeBase và kèm nguồn.
- NFR3: Dữ liệu minh họa phải được ghi nhãn rõ ở UI, API và tài liệu.
- NFR4: Chạy được hoàn toàn offline sau khi cài requirements (không gọi API ngoài).
- NFR5: Mã nguồn tách module rõ (preprocess / entities / train / chatbot / db / main) để dễ kiểm thử.
