document.addEventListener("DOMContentLoaded", () => {
  const monthlyNode = document.getElementById("monthly-data");
  const categoryNode = document.getElementById("category-data");
  const monthlyCanvas = document.getElementById("monthlyChart");
  const categoryCanvas = document.getElementById("categoryChart");

  if (monthlyNode && monthlyCanvas && window.Chart) {
    const values = JSON.parse(monthlyNode.textContent);
    new Chart(monthlyCanvas, {
      type: "bar",
      data: {
        labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        datasets: [{
          label: "Expenses (₹)",
          data: values,
          backgroundColor: "rgba(255, 119, 123, 0.78)",
          borderRadius: 4,
          maxBarThickness: 24
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: "#edf0f5" }, ticks: { color: "#8b91a3", font: { size: 10 } } },
          x: { grid: { display: false }, ticks: { color: "#8b91a3", font: { size: 10 } } }
        }
      }
    });
  }

  if (categoryNode && categoryCanvas && window.Chart) {
    const items = JSON.parse(categoryNode.textContent);
    if (items.length) {
      new Chart(categoryCanvas, {
        type: "doughnut",
        data: {
          labels: items.map(item => item.category),
          datasets: [{
            data: items.map(item => Number(item.total)),
            backgroundColor: ["#6199f5","#ff777b","#f6bd60","#9b8afb","#48c7bd","#f59ab7","#a8b0c4"],
            borderWidth: 3,
            borderColor: "#fff",
            hoverOffset: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "68%",
          plugins: { legend: { display: false } }
        }
      });
    }
  }
});
