# Preprocessing, Model Architecture, Training Configuration

## Preprocessing (app/preprocess.py)
1. Hạ chữ thường; 2. Bỏ dấu tiếng Việt (unicodedata + xử lý riêng đ/Đ);
3. Bỏ dấu câu; 4. Thay viết tắt phổ biến (cntt -> cong nghe thong tin, ktx -> ky tuc xa,
bn -> bao nhieu, ko -> khong...); 5. Gọn khoảng trắng.
Nhờ chuẩn hóa không dấu, một mô hình duy nhất khớp cả câu có dấu và không dấu.

## Model Architecture
Pipeline scikit-learn:
- FeatureUnion: TF-IDF word n-gram (1,2) + TF-IDF char_wb n-gram (3,5).
  Char n-gram giúp chịu sai chính tả nhẹ và biến thể viết tắt chưa có trong từ điển.
- Classifier: **Logistic Regression** (max_iter=1000, C=8.0).
  Chọn LR thay LinearSVC vì LR cho `predict_proba` để tính confidence và áp ngưỡng fallback 0.45;
  LinearSVC không có xác suất trực tiếp. Với tập dữ liệu nhỏ (104 mẫu), LR + TF-IDF cũng ổn định
  và huấn luyện trong vài giây, không cần GPU/deep learning.

## Training Configuration
- Lệnh: `python -m app.train` -> lưu `models/intent_model.pkl` (~208 KB).
- Dữ liệu: 104 mẫu / 14 intent (data/training_data.json).
- Không chia train/test từ tập huấn luyện; việc đánh giá dùng **tập kiểm tra độc lập riêng**
  (test_set.json) để tránh tự đánh giá trên dữ liệu đã học.
- Tái lập: cố định dữ liệu JSON trong repo; huấn luyện lại cho cùng kết quả đánh giá trên cùng môi trường thư viện.
