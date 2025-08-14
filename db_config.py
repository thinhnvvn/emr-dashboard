# import psycopg2

# DB_CONFIG = {
#     'host': 'localhost',
#     'port': 5432,
#     'dbname': 'emr_db',
#     'user': 'postgres',
#     'password': '1234'  # Thay bằng mật khẩu thật
# }


# from sqlalchemy import create_engine

# # def get_engine():
# #     return create_engine('postgresql://username:password@localhost:5432/emr_db')

# def get_engine():
#     return create_engine(
#         f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
#     )

# def get_db_connection():
#     # Chạy trên vscode  -- good
#     '''
#     return psycopg2.connect(
#         host='localhost',
#         port=5432,
#         dbname='emr_db',
#         user='postgres',
#         password='1234'
#     )
#     '''
#     # Chạy trên Railway
#     return psycopg2.connect(
#         host='postgres.railway.internal',
#         port=5432,
#         dbname='railway',
#         user='postgres',
#         password='AlAmndSaXPXWtiwNQGgfBIGCBWtgjmbb'
#     )


import os
import os
import psycopg2
from sqlalchemy import create_engine

DATABASE_URL = os.getenv('DATABASE_URL')

# Cấu hình kết nối — dùng biến môi trường nếu có, fallback về giá trị local
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'dbname': os.getenv('DB_NAME', 'emr_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '1234')
}

# SQLAlchemy engine — dùng cho phân tích hoặc ORM
def get_engine():
    return create_engine(
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )

# Kết nối psycopg2 — dùng cho truy vấn thủ công
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)
