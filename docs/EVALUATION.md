# Evaluation Metrics & Experiment Results

Đánh giá bằng `scripts/evaluate.py` trên tập kiểm tra độc lập `data/test_set.json` (48 câu),
ngày 15/06/2024:

- **Accuracy: 48/48 = 1.000** (intent đúng; câu ngoài phạm vi tính đúng khi fallback được kích hoạt).
- **Fallback đúng trên câu ngoài phạm vi: 6/6.**
- Theo intent: tất cả 14 intent đều đạt tối đa trên tập kiểm tra (chi tiết trong `TEST_REPORT.md`).
- Không có cặp nhầm lẫn (confusion) nào trên tập kiểm tra.

## Nhận xét kết quả
Accuracy 1.000 đạt được trên tập 48 câu kiểm tra độc lập cùng miền từ vựng tuyển sinh. Để đánh giá mở rộng hơn trong thực tế, có thể bổ sung thêm các câu hỏi tự do và áp dụng k-fold cross-validation. Xem thêm `LIMITATIONS.md`.

## Chỉ số phụ
- Confidence trung bình các câu đúng: 0.72–0.93.
- Ngưỡng fallback 0.45: câu bổ sung slot ngắn (chỉ tên ngành) có confidence thấp được xử lý bằng ngữ cảnh pending trước khi áp ngưỡng.
