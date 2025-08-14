from flask import Flask, jsonify, render_template
from db_config import get_db_connection
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime
from datetime import date

import os

app = Flask(__name__)

# Route: Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

def run_advanced_analysis():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Lấy thông tin bệnh nhân và chẩn đoán
        cur.execute("""
            SELECT p.date_of_birth, d.description
            FROM patients p
            LEFT JOIN visits v ON p.patient_id = v.patient_id
            LEFT JOIN diagnoses d ON v.visit_id = d.visit_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        today = date.today()
        ages = []
        diagnoses = []

        for dob, diagnosis in rows:
            if dob:
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                ages.append(age)
            if diagnosis:
                diagnoses.append(diagnosis)

        # Tính tuổi trung bình
        avg_age = round(sum(ages) / len(ages), 1) if ages else None

        # Chẩn đoán phổ biến nhất
        most_common = Counter(diagnoses).most_common(1)
        top_diagnosis = most_common[0][0] if most_common else "Không có dữ liệu"

        return {
            "average_age": avg_age,
            "most_common_diagnosis": top_diagnosis,
            "total_patients": len(ages)
        }

    except Exception as e:
        print("⚠️ Lỗi phân tích nâng cao:", e)
        return {"error": str(e)}

# Route: Phân tích nâng cao
@app.route('/api/analysis')
def api_analysis():
    try:
        conn = get_db_connection()
        
        df = pd.read_sql("""
            SELECT patient_id, full_name, date_of_birth, contact_number
            FROM patients
        """, conn)
        
        
        
        conn.close()

        # Tính tuổi
        df['age'] = pd.to_datetime('today').year - pd.to_datetime(df['date_of_birth']).dt.year

        # Mã hóa chẩn đoán
        df['diagnosis'] = df['contact_number']
        df['diagnosis_code'] = df['diagnosis'].astype('category').cat.codes

        # Phân cụm
        kmeans = KMeans(n_clusters=3, random_state=0)
        df['cluster'] = kmeans.fit_predict(df[['age', 'diagnosis_code']])

        # Tạo thư mục nếu chưa có
        os.makedirs('static/images', exist_ok=True)

        # Vẽ biểu đồ
        image_path = 'static/images/cluster.png'
        plt.figure(figsize=(6, 4))
        plt.scatter(df['age'], df['diagnosis_code'], c=df['cluster'], cmap='viridis')
        plt.xlabel('Tuổi')
        plt.ylabel('Mã chẩn đoán')
        plt.title('Phân cụm bệnh nhân')
        plt.savefig(image_path)
        plt.close()

        # Trả dữ liệu JSON
        clusters = df[['patient_id', 'full_name', 'age', 'diagnosis', 'cluster']].to_dict(orient='records')
        return jsonify({
            "image_url": f"/{image_path}",
            "clusters": clusters
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

# Route: Danh sách bệnh nhân
@app.route('/api/patients')
def api_patients():
    try:
        conn = get_db_connection()
        
        # df = pd.read_sql("""
        #     SELECT patient_id, full_name, date_of_birth, contact_number
        #     FROM patients
        # """, conn)
        
        df = pd.read_sql("""
            SELECT 
                p.patient_id,
                p.full_name,
                p.date_of_birth,
                d.description AS diagnosis
            FROM patients p
            LEFT JOIN visits v ON p.patient_id = v.patient_id
            LEFT JOIN diagnoses d ON v.visit_id = d.visit_id
        """, conn)

        
        
        conn.close()

        # Tính tuổi
        # today = pd.Timestamp(datetime.today())
        # df['age'] = (today - pd.to_datetime(df['date_of_birth'])).dt.days // 365
        
        # Tính tuổi
        today = pd.Timestamp(datetime.today())
        df['age'] = (today - pd.to_datetime(df['date_of_birth'])).dt.days // 365

        # Trả dữ liệu JSON
        # data = df[['patient_id', 'full_name', 'age', 'contact_number']].to_dict(orient='records')
        # return jsonify({"status": "success", "patients": data})
        
        data = df[['patient_id', 'full_name', 'age', 'diagnosis']].to_dict(orient='records')
        return jsonify({"status": "success", "patients": data})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500




# Route: Thống kê tổng hợp
@app.route('/api/summary')
def api_summary():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM patients')
        total_patients = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM visits')
        total_visits = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM diagnoses')
        total_diagnoses = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            'total_patients': total_patients,
            'total_visits': total_visits,
            'total_diagnoses': total_diagnoses
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Khởi chạy Flask
if __name__ == '__main__':
    app.run(debug=True)
