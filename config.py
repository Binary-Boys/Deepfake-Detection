import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

