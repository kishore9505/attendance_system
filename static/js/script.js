// script.js
// Client-side helpers: form validation + Chart.js rendering

document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("searchForm");
  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      const input = document.getElementById("rollNoInput");
      if (!input.value.trim()) {
        e.preventDefault();
        alert("Please enter your roll number.");
      }
    });
  }
});

/**
 * Renders the attendance percentage doughnut chart on the dashboard page.
 * Called from dashboard.html with the student's data injected via Jinja.
 */
function renderAttendanceChart(canvasId, percentage, color) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Attended", "Missed"],
      datasets: [{
        data: [percentage, Math.max(0, 100 - percentage)],
        backgroundColor: [color, "rgba(255,255,255,0.15)"],
        borderWidth: 0
      }]
    },
    options: {
      cutout: "72%",
      plugins: {
        legend: { labels: { color: "#fff" } }
      }
    }
  });
}

/**
 * Renders the risk distribution pie chart on the admin dashboard.
 */
function renderRiskDistributionChart(canvasId, safeCount, mediumCount, dangerCount) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Safe", "Medium Risk", "Danger"],
      datasets: [{
        data: [safeCount, mediumCount, dangerCount],
        backgroundColor: ["#22c55e", "#eab308", "#ef4444"],
      }]
    },
    options: {
      plugins: { legend: { labels: { color: "#fff" } } }
    }
  });
}

/**
 * Renders the department-wise average attendance bar chart on the admin dashboard.
 */
function renderBranchChart(canvasId, labels, values) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Avg Attendance %",
        data: values,
        backgroundColor: "#06b6d4"
      }]
    },
    options: {
      scales: {
        x: { ticks: { color: "#fff" } },
        y: { ticks: { color: "#fff" }, beginAtZero: true, max: 100 }
      },
      plugins: { legend: { labels: { color: "#fff" } } }
    }
  });
}
