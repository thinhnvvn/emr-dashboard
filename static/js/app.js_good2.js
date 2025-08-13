document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/summary')
    .then(res => res.json())
    .then(data => {
      document.getElementById('patients').textContent = data.total_patients;
      document.getElementById('visits').textContent = data.total_visits;
      document.getElementById('diagnoses').textContent = data.total_diagnoses;
    });

  // Tự động tải phân tích nâng cao khi trang vừa load
  loadAnalysis();
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
        <img id="cluster-image" src="${data.image_url}" alt="Biểu đồ phân cụm" style="max-width:100%; margin-bottom: 20px;">
        <table class="table table-bordered" id="cluster-table">
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

      const body = document.getElementById('cluster-body');
      body.innerHTML = '';

      if (Array.isArray(data.clusters)) {
        data.clusters.forEach(row => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${row.id}</td>
            <td>${row.full_name}</td>
            <td>${row.age}</td>
            <td>${row.diagnosis}</td>
            <td><strong class="text-primary">${row.cluster}</strong></td>
          `;
          body.appendChild(tr);
        });
      } else {
        body.innerHTML = `<tr><td colspan="5" class="text-danger text-center">Không có dữ liệu phân cụm.</td></tr>`;
      }
    })
    .catch(error => {
      console.error("Lỗi khi gọi /api/analysis:", error);
      const resultDiv = document.getElementById('analysis-result');
      resultDiv.innerHTML = `<div class="alert alert-danger">Không thể tải dữ liệu phân tích nâng cao.</div>`;
    });
}

function drawAgeChart(data) {
  const ctx = document.getElementById('ageChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: 'Phân bố độ tuổi',
        data: Object.values(data),
        backgroundColor: 'rgba(75, 192, 192, 0.6)'
      }]
    }
  });
}
