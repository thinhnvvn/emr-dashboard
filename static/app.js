//Gọi api và cập nhật giao diện

document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/summary')
    .then(res => res.json())
    .then(data => {
      document.getElementById('patients').textContent = data.total_patients;
      document.getElementById('visits').textContent = data.total_visits;
      document.getElementById('diagnoses').textContent = data.total_diagnoses;
    });
});

function loadAnalysis() {
    fetch('/analysis')
        .then(response => {
            if (!response.ok) {
                throw new Error('Không thể tải nội dung phân tích');
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('analysis-container').innerHTML = html;
        })
        .catch(error => {
            console.error('Lỗi khi tải phân tích:', error);
        });
}

