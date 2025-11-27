(() => {
  const chartData = window.dashboardChartData || {};

  const weekCtx = document.getElementById("workoutsByDayChart");
  if (weekCtx) {
    new Chart(weekCtx, {
      type: "bar",
      data: {
        labels: chartData.weekLabels || [],
        datasets: [
          {
            label: "Workouts",
            data: chartData.weekValues || [],
            backgroundColor: "rgba(54, 162, 235, 0.6)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        animation: {
          duration: 0,
        },
        interaction: {
          intersect: false,
        },
        scales: {
          y: {
            beginAtZero: true,
            precision: 0,
            ticks: {
              stepSize: 1,
            },
          },
        },
      },
    });
  }

  const typeCtx = document.getElementById("workoutsByTypeChart");
  if (typeCtx) {
    new Chart(typeCtx, {
      type: "doughnut",
      data: {
        labels: chartData.typeLabels || [],
        datasets: [
          {
            data: chartData.typeValues || [],
            backgroundColor: [
              "#4e79a7",
              "#f28e2b",
              "#e15759",
              "#76b7b2",
              "#59a14f",
              "#edc949",
              "#af7aa1",
              "#ff9da7",
              "#9c755f",
              "#bab0ab",
            ],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 2,
        animation: {
          duration: 0,
        },
        interaction: {
          intersect: false,
        },
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }
})();

