// Auto-hide flash messages
setTimeout(() => {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(flash => flash.style.display = 'none');
}, 4000);

// Toggle dark mode
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('toggle-dark');
  if (toggle) {
    toggle.addEventListener('click', () => {
      document.body.classList.toggle('dark');
      localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    });
  }

  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
  }
});

// Example Chart.js bar chart
function renderDashboardChart() {
  const ctx = document.getElementById('activityChart');
  if (ctx) {
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['admin', 'user1', 'hacker'],
        datasets: [{
          label: 'Login Attempts',
          data: [3, 2, 1],
          backgroundColor: ['#007bff', '#28a745', '#dc3545']
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
}

window.onload = renderDashboardChart;
