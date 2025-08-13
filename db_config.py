import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'emr_db',
    'user': 'postgres',
    'password': '1234'  # Thay bằng mật khẩu thật
}


from sqlalchemy import create_engine

# def get_engine():
#     return create_engine('postgresql://username:password@localhost:5432/emr_db')

def get_engine():
    return create_engine(
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )

def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='emr_db',
        user='postgres',
        password='1234'
    )