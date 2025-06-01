# Thêm các dòng này vào đầu tệp
from dotenv import load_dotenv
import os

load_dotenv() # Tải biến từ .env

#Khởi tạo ứng dụng Flask
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'duysama' # Cần thiết nếu dùng session, form bảo mật

# Import routes sau khi app được tạo để tránh circular imports
from app import routes

# Dòng này không cần thiết nữa vì đã dùng os.environ.get trong routes.py
# OPENROUTER_API_KEY = "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"
