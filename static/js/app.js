document.addEventListener('DOMContentLoaded', () => {
  loadAnalysis();
  loadPatients();
});

function loadAnalysis() {
  fetch('/api/analysis')
    .then(response => {
      if (!response.ok) {
        throw new Error("API /api/analysis không phản hồi.");
      }
      return response.json();
    })
    .then(data => {
      const resultDiv = document.getElementById('analysis-result');
      resultDiv.innerHTML = `
        <h4>Kết quả phân tích nâng cao:</h4>
        <img src="${data.image_url}" alt="Biểu đồ phân cụm" style="max-width:100%; margin-bottom: 20px;">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Họ tên</th>
              <th>Tuổi</th>
              <th>Chẩn đoán</th>
              <th>Nhóm</th>
            </tr>
          </thead>
          <tbody id="cluster-body">
          </tbody>
        </table>
      `;

      const tbody = document.getElementById('cluster-body');
      tbody.innerHTML = '';

      data.clusters.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${row.patient_id}</td>
          <td>${row.full_name}</td>
          <td>${row.age}</td>
          <td>${row.diagnosis}</td>
          <td><strong class="text-primary">${row.cluster}</strong></td>
        `;
        tbody.appendChild(tr);
      });
    })
    .catch(error => {
      console.error("Lỗi khi gọi /api/analysis:", error);
      const resultDiv = document.getElementById('analysis-result');
      resultDiv.innerHTML = `<div class="alert alert-danger">Không thể tải dữ liệu phân tích nâng cao.</div>`;
    });
}

function loadPatients() {
  fetch('/api/patients')
    .then(res => res.json())
    .then(data => {
      const body = document.getElementById('patient-body');
      body.innerHTML = '';

      if (data.status === 'success') {
        data.patients.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${row.patient_id}</td>
            <td>${row.full_name}</td>
            <td>${row.age}</td>
            <td>${row.diagnosis}</td>
          `;
          body.appendChild(tr);
        });
      } else {
        body.innerHTML = `<tr><td colspan="4" class="text-danger text-center">Không thể tải danh sách bệnh nhân.</td></tr>`;
      }
    })
    .catch(err => {
      console.error("Lỗi khi tải danh sách bệnh nhân:", err);
      const body = document.getElementById('patient-body');
      body.innerHTML = `<tr><td colspan="4" class="text-danger text-center">Không thể tải danh sách bệnh nhân.</td></tr>`;
    });
}


fetch('/api/summary')
  .then(res => {
    if (!res.ok) throw new Error("Không thể tải thống kê");
    return res.json();
  })
  .then(data => {
    document.getElementById('patients').textContent = data.total_patients;
    document.getElementById('visits').textContent = data.total_visits;
    document.getElementById('diagnoses').textContent = data.total_diagnoses;
  })
  .catch(err => {
    console.error("Lỗi khi tải thống kê:", err);
  });

function showAgeDistribution() {
  fetch('/api/patients')
    .then(res => res.json())
    .then(data => {
      const ages = data.patients.map(p => p.age);
      const freq = {};

      ages.forEach(age => {
        const group = `${Math.floor(age / 10) * 10}s`;
        freq[group] = (freq[group] || 0) + 1;
      });

      const labels = Object.keys(freq);
      const values = Object.values(freq);

      document.getElementById('diagnosisChart').style.display = 'none';
      document.getElementById('ageChart').style.display = 'block';

      new Chart(document.getElementById('ageChart'), {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Số lượng bệnh nhân',
            data: values,
            backgroundColor: 'rgba(54, 162, 235, 0.6)'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: '📊 Phân bố độ tuổi'
            }
          }
        }
      });
    });
}

function showDiagnosisFrequency() {
  fetch('/api/patients')
    .then(res => res.json())
    .then(data => {
      const diagnoses = data.patients.map(p => p.diagnosis);
      const freq = {};

      diagnoses.forEach(d => {
        freq[d] = (freq[d] || 0) + 1;
      });

      const labels = Object.keys(freq);
      const values = Object.values(freq);

      document.getElementById('ageChart').style.display = 'none';
      document.getElementById('diagnosisChart').style.display = 'block';

      new Chart(document.getElementById('diagnosisChart'), {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Tần suất chẩn đoán',
            data: values,
            backgroundColor: labels.map((_, i) => `hsl(${i * 30}, 70%, 60%)`)
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: '📊 Tần suất chẩn đoán'
            }
          }
        }
      });
    });
}
