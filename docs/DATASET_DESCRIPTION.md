# Dataset Description

## Dữ liệu tuyển sinh (data/)
- `majors.json`: 12 ngành của trường giả định ACU: mã, tên, tổ hợp, học phí/năm,
  điểm chuẩn minh họa 2021–2023, chỉ tiêu, mô tả, sở thích liên quan, môn học mạnh, `source`.
- `admission_methods.json`: 4 phương thức (điểm thi THPT, học bạ, ĐGNL, xét tuyển thẳng) kèm điều kiện và mốc thời gian minh họa.
- `faqs.json`: 7 FAQ (học bổng x2, ký túc xá x2, thời gian, hồ sơ, liên hệ), mỗi mục có `source`.
- Nguồn: **100% là số liệu minh họa phục vụ đồ án**.
  Trường `source` trong từng bản ghi ghi rõ điều này và được đính kèm trong câu trả lời của bot.

## Dữ liệu huấn luyện (data/training_data.json)
104 câu mẫu tự viết cho 14 intent (chao_hoi, cam_on, hoi_hoc_phi, diem_chuan, to_hop_xet_tuyen,
phuong_thuc_xet_tuyen, goi_y_nganh, so_sanh_nganh, hoc_bong, ky_tuc_xa, thoi_gian_tuyen_sinh,
ho_so_xet_tuyen, lien_he, ngoai_pham_vi).

## Tập kiểm tra (data/test_set.json)
48 câu độc lập (không trùng nguyên văn tập huấn luyện): có câu không dấu, viết tắt, diễn đạt khác,
6 câu ngoài phạm vi kỳ vọng fallback. Dùng bởi scripts/evaluate.py và được mô tả trong EVALUATION.
