from db_config import get_db_connection
from datetime import date
from collections import Counter

def run_advanced_analysis():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Truy vấn thông tin bệnh nhân và chẩn đoán
        cur.execute("""
            SELECT p.patient_id, p.full_name, p.date_of_birth, d.description
            FROM patients p
            LEFT JOIN visits v ON p.patient_id = v.patient_id
            LEFT JOIN diagnoses d ON v.visit_id = d.visit_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        today = date.today()
        clusters = []
        ages = []
        diagnoses = []

        for pid, name, dob, diagnosis in rows:
            if dob:
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                ages.append(age)
            else:
                age = None

            if diagnosis:
                diagnoses.append(diagnosis)
            else:
                diagnosis = "Chưa có"

            clusters.append({
                "patient_id": pid,
                "full_name": name,
                "age": age,
                "diagnosis": diagnosis,
                "cluster": "Nhóm 1"  # Tạm gán 1 nhóm, có thể phân cụm sau
            })

        avg_age = round(sum(ages) / len(ages), 1) if ages else None
        top_diagnosis = Counter(diagnoses).most_common(1)
        most_common = top_diagnosis[0][0] if top_diagnosis else "Không có dữ liệu"

        return {
            "average_age": avg_age,
            "most_common_diagnosis": most_common,
            "total_patients": len(set([c["patient_id"] for c in clusters])),
            "image_url": "https://your-image-hosting.com/cluster.png",  # nếu có ảnh
            "clusters": clusters
        }

    except Exception as e:
        print("⚠️ Lỗi phân tích nâng cao:", e)
        return {"error": str(e)}
