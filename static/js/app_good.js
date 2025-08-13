document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/summary')
    .then(res => res.json())
    .then(data => {
      //document.getElementById('patients').textContent = data.total_patients;
      //document.getElementById('visits').textContent = data.total_visits;
      //  document.getElementById('diagnoses').textContent = data.total_diagnoses;
    });
});

// function loadAnalysis() {
//     fetch('/analysis')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Không thể tải nội dung phân tích');
//             }
//             return response.text();
//         })
//         .then(html => {
//             document.getElementById('analysis-container').innerHTML = html;
//         })
//         .catch(error => {
//             console.error('Lỗi khi tải phân tích:', error);
//         });
// }

// 

function loadAnalysisOld() {
  fetch('/api/analysis')
    .then(res => {
      if (!res.ok) {
        throw new Error("Không thể kết nối tới API phân tích.");
      }
      return res.json();
    })
    .then(data => {
      // Hiển thị hình ảnh phân cụm
      const imageElement = document.getElementById('cluster-image');
      imageElement.src = data.image_url;
      imageElement.alt = "Biểu đồ phân cụm";

      // Hiển thị bảng phân cụm
      const table = document.getElementById('cluster-table');
      const body = document.getElementById('cluster-body');
      table.style.display = 'table';
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
    .catch(err => {
      console.error("Lỗi khi tải phân tích:", err);
      const body = document.getElementById('cluster-body');
      body.innerHTML = `<tr><td colspan="5" class="text-danger text-center">Lỗi khi tải dữ liệu phân tích.</td></tr>`;
    });
}

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
        <img src="${data.image_path}" alt="Biểu đồ phân cụm" style="max-width:100%; margin-bottom: 20px;">
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
          <tbody>
            ${data.data.map(row => `
              <tr>
                <td>${row.ID}</td>
                <td>${row.Name}</td>
                <td>${row.Age}</td>
                <td>${row.Diagnosis}</td>
                <td><strong class="text-primary">${row.Cluster}</strong></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    })
    .catch(error => {
      console.error("Lỗi khi gọi /api/analysis:", error);
      alert("Không thể tải dữ liệu phân tích nâng cao.");
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


