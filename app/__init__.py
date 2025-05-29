#Khởi tạo ứng dụng Flask
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'duysama' # Cần thiết nếu dùng session, form bảo mật

# Import routes sau khi app được tạo để tránh circular imports
from app import routes