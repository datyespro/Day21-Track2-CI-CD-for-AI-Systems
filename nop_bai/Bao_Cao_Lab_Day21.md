# BÁO CÁO THỰC HÀNH MLOPS - DAY 21

**Họ và tên:** Nguyễn Thành Đạt 
**Mã sinh viên:** 2A202600203
**Link Repo GitHub:** https://github.com/datyespro/Day21-Track2-CI-CD-for-AI-Systems.git  -  (nhánh main)

---

## 1. Bộ siêu tham số (Hyperparameters) đã chọn và lý do

Ở Bước 1, qua quá trình thử nghiệm tracking với MLflow, tôi đã chọn bộ siêu tham số tốt nhất cho mô hình Random Forest như sau:
- `n_estimators: 500`
- `max_depth: 20`
- `min_samples_split: 3`
- `criterion: entropy`
- `class_weight: balanced`

**Lý do chọn:** 
Bộ tham số này giúp mô hình xử lý tốt sự mất cân bằng dữ liệu (nhờ `class_weight: balanced`) và đạt được sự cân bằng tối ưu giữa Accuracy (0.68) và F1-score (0.68) cao nhất trong các lần chạy thử nghiệm ở Phase 1. Đồng thời, mô hình không bị quá khớp (overfitting) nhờ kiểm soát được `max_depth` và `min_samples_split`. Ở Phase 2 (sau khi thêm dữ liệu mới), mô hình với bộ tham số này cũng đã tăng độ chính xác lên 0.74.

---

## 2. Khó khăn gặp phải và cách giải quyết

- **Khó khăn 1:** Khi chạy các lệnh kiểm tra `curl` để gọi API dự đoán trên máy tính local (hệ điều hành Windows), lệnh `curl -X POST ...` báo lỗi do cú pháp không tương thích với Windows PowerShell.
  - **Cách giải quyết:** Sử dụng lệnh `Invoke-RestMethod` riêng của PowerShell với cú pháp truyền headers và body JSON chuẩn, hoặc chuyển sang dùng Command Prompt (CMD) / Git Bash để chạy lệnh curl mặc định.

- **Khó khăn 2:** Khi đẩy file dữ liệu thay đổi lên GitHub để kích hoạt CI/CD pipeline, cần đảm bảo tránh đẩy nhầm file CSV thực tế mà chỉ đẩy file con trỏ của DVC nhằm tối ưu dung lượng Git.
  - **Cách giải quyết:** Đã config file `.gitignore` để tự động loại bỏ các file `*.csv` thô, sau đó thao tác tuần tự `dvc push` (để đẩy dữ liệu lên AWS S3) rồi mới `git push` (để kích hoạt GitHub Actions).

---
*(Đính kèm 4 ảnh chụp màn hình riêng lẻ hoặc dán trực tiếp vào cuối file báo cáo này)*
