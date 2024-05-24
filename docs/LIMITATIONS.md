# Limitations

1. Dữ liệu tuyển sinh là **minh họa** của trường giả định; muốn dùng thật phải thay bằng dữ liệu
   chính thức của trường và cập nhật trường `source`.
2. Tập huấn luyện nhỏ (104 mẫu/14 intent); độ chính xác đo được (48/48) là trên tập kiểm tra
   do nhóm tự soạn, chưa phản ánh câu hỏi tự do ngoài thực tế.
3. Gợi ý ngành dùng rule chấm điểm từ khóa (sở thích + môn mạnh), không phải mô hình học sâu;
   có thể bỏ sót cách diễn đạt sở thích lạ.
4. Nhận diện ngành bằng từ điển + fuzzy matching: tên ngành mới thêm qua admin cần bổ sung
   alias trong app/entities.py và nên huấn luyện lại mô hình.
5. Token admin là cơ chế demo đơn giản (header tĩnh), không dùng cho production;
   production cần đăng nhập + phân quyền thật và cơ sở dữ liệu có giao dịch thay cho file JSON.
6. Slot filling chỉ giữ trong bộ nhớ theo session (mất khi server khởi động lại).
