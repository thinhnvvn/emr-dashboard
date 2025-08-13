# Test kết nối db
import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='emr_db',
        user='postgres',
        password='1234'  # thay bằng mật khẩu thật
    )
    print("✅ Kết nối thành công!")
    conn.close()
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
