# DSS - Health Expert System

## Giới thiệu
DSS (Decision Support System) là hệ thống chuyên gia hỗ trợ chẩn đoán sức khỏe sử dụng trí tuệ nhân tạo. Dự án này giúp người dùng tự kiểm tra triệu chứng, nhận tư vấn sức khỏe và lưu lại lịch sử chẩn đoán.

## Tính năng chính
- Chẩn đoán bệnh dựa trên triệu chứng nhập vào
- Lưu và xem lại lịch sử chẩn đoán
- Quản lý tài khoản người dùng (đăng ký, đăng nhập, cập nhật thông tin)
- Giao diện chatbot AI hỗ trợ tư vấn
- Trang hỗ trợ và liên hệ

## Hướng dẫn cài đặt & chạy
1. **Clone repository:**
   ```bash
   git clone https://github.com/Duysama123/DSS.git
   cd DSS
   ```
2. **Cài đặt môi trường ảo (nếu cần):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Linux/Mac
   venv\Scripts\activate    # Trên Windows
   ```
3. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Chạy ứng dụng:**
   ```bash
   python run.py
   ```
5. **Truy cập:**
   Mở trình duyệt và truy cập `http://localhost:5000`

## Cấu trúc thư mục
```
DSS/
├── app/                  # Mã nguồn chính của ứng dụng Flask
│   ├── static/           # File tĩnh (CSS, JS, hình ảnh)
│   ├── templates/        # Giao diện HTML
│   └── ...
├── data/                 # Dữ liệu mẫu, file hỗ trợ
├── models/               # Mô hình AI, file huấn luyện
├── notebooks/            # Notebook Jupyter cho phân tích, thử nghiệm
├── requirements.txt      # Danh sách thư viện Python
├── run.py                # File chạy chính
└── README.md             # Mô tả dự án
```

## Thông tin liên hệ
- **Tác giả:** Nhóm 3
- **GitHub:** [https://github.com/Duysama123/DSS](https://github.com/Duysama123/DSS)

Nếu có thắc mắc hoặc đóng góp, vui lòng liên hệ qua email hoặc tạo issue trên GitHub. 