from flask import Flask, jsonify, render_template
from db_config import get_db_connection
# from analysis import run_advanced_analysis
from psycopg2.extras import RealDictCursor
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def home():
    return render_template('index.html')

@app.route('/api/patients')
def get_patients():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.patient_id, p.full_name, p.date_of_birth,
                   COALESCE(string_agg(d.description, ', '), 'Chưa có') AS diagnosis
            FROM patients p
            LEFT JOIN visits v ON p.patient_id = v.patient_id
            LEFT JOIN diagnoses d ON v.visit_id = d.visit_id
            GROUP BY p.patient_id, p.full_name, p.date_of_birth
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        today = date.today()
        result = []
        for row in rows:
            pid, name, dob, diagnosis = row
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            result.append([pid, name, age, diagnosis])

        return jsonify(result)
    except Exception as e:
        print("⚠️ Lỗi khi truy vấn DB:", e)
        return jsonify({'error': str(e)})

@app.route('/api/summary')
def get_summary():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM patients")
        total_patients = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM visits")
        total_visits = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM diagnoses")
        total_diagnoses = cur.fetchone()[0]

        conn.close()
        return jsonify({
            "total_patients": total_patients,
            "total_visits": total_visits,
            "total_diagnoses": total_diagnoses
        })
    except Exception as e:
        print("⚠️ Lỗi khi lấy thống kê:", e)
        return jsonify({'error': str(e)})

@app.route('/api/analysis')
def analysis():
    try:
        # good cho vscode
        # result = run_advanced_analysis()
        # return jsonify(result)
        return jsonify({"message": "Phân tích nâng cao chưa khả dụng trên Railway"})
    except Exception as e:
        print("⚠️ Lỗi phân tích:", e)
        return jsonify({"error": "Không thể phân tích"}), 500

if __name__ == '__main__':
    app.run(debug=True)
