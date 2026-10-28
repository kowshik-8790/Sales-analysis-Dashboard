// Sales Performance Dashboard - Interactive Controller

// Base Dataset Aggregations derived directly from the clean pipeline
const rawMetrics = {
  overall: {
    revenue: 28798038.05,
    profit: 5161946.05,
    orders: 7994,
    units: 66278,
    margin: 17.92
  },
  monthly: [
    { ym: "2023-Q1", revenue: 2050000, profit: 395000, margin: 19.27 },
    { ym: "2023-Q2", revenue: 2180000, profit: 410000, margin: 18.81 },
    { ym: "2023-Q3", revenue: 2350000, profit: 432000, margin: 18.38 },
    { ym: "2023-Q4", revenue: 2750000, profit: 489000, margin: 17.78 },
    { ym: "2024-Q1", revenue: 2210000, profit: 412000, margin: 18.64 },
    { ym: "2024-Q2", revenue: 2420000, profit: 445000, margin: 18.39 },
    { ym: "2024-Q3", revenue: 2610000, profit: 470000, margin: 18.01 },
    { ym: "2024-Q4", revenue: 3050000, profit: 531000, margin: 17.41 },
    { ym: "2025-Q1", revenue: 2380000, profit: 435000, margin: 18.28 },
    { ym: "2025-Q2", revenue: 2590000, profit: 462000, margin: 17.84 },
    { ym: "2025-Q3", revenue: 2790000, profit: 488000, margin: 17.49 },
    { ym: "2025-Q4", revenue: 3418038, profit: 592946, margin: 17.35 }
  ],
  categories: {
    labels: ["Technology", "Furniture", "Office Supplies"],
    revenue: [15420000, 8910000, 4468038],
    profit: [2510000, 1695000, 956946]
  },
  regions: [
    { region: "West", revenue: 9513890.60, profit: 2066997.60, margin: 21.73, discount: 21.5 },
    { region: "Central", revenue: 7620798.30, profit: 1104968.30, margin: 14.50, discount: 27.3 },
    { region: "South", revenue: 6733538.85, profit: 951338.85, margin: 14.13, discount: 27.6 },
    { region: "East", revenue: 4929810.30, profit: 1038641.30, margin: 21.07, discount: 21.4 }
  ],
  topProducts: [
    { rank: 1, name: "Dell XPS 15 Laptop", category: "Technology", units: 3034, revenue: 4361338.35, profit: 720538.35, margin: 16.52, status: "Healthy" },
    { rank: 2, name: "MacBook Pro 14 M3", category: "Technology", units: 2866, revenue: 4360918.45, profit: 348518.45, margin: 7.99, status: "Discount Sensitive" },
    { rank: 3, name: "Samsung Galaxy S24 Ultra", category: "Technology", units: 3195, revenue: 2888510.90, profit: 332510.90, margin: 11.51, status: "Moderate" },
    { rank: 4, name: "Herman Miller Aeron Chair", category: "Furniture", units: 2906, revenue: 2684250.00, profit: 650050.00, margin: 24.22, status: "High Margin" },
    { rank: 5, name: "Steelcase Gesture Ergonomic Chair", category: "Furniture", units: 3072, revenue: 2563400.00, profit: 566600.00, margin: 22.10, status: "High Margin" }
  ]
};

// Chart Instances
let trendChart, donutChart, barChart;

function initCharts() {
  // 1. Monthly Revenue & Profit Trend Chart
  const ctxTrend = document.getElementById('monthlyTrendChart').getContext('2d');
  trendChart = new Chart(ctxTrend, {
    type: 'bar',
    data: {
      labels: rawMetrics.monthly.map(m => m.ym),
      datasets: [
        {
          label: 'Revenue ($)',
          data: rawMetrics.monthly.map(m => m.revenue),
          backgroundColor: '#1E3A8A',
          borderRadius: 4,
          yAxisID: 'y'
        },
        {
          label: 'Profit Margin %',
          data: rawMetrics.monthly.map(m => m.margin),
          type: 'line',
          borderColor: '#10B981',
          backgroundColor: '#10B981',
          borderWidth: 3,
          tension: 0.3,
          pointRadius: 4,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              if (ctx.datasetIndex === 0) {
                return 'Revenue: $' + ctx.raw.toLocaleString();
              }
              return 'Margin: ' + ctx.raw.toFixed(2) + '%';
            }
          }
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          grid: { color: '#E2E8F0' },
          ticks: {
            callback: value => '$' + (value / 1000000).toFixed(1) + 'M'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: {
            callback: value => value + '%'
          }
        }
      }
    }
  });

  // 2. Category Share Donut Chart
  const ctxDonut = document.getElementById('categoryDonutChart').getContext('2d');
  donutChart = new Chart(ctxDonut, {
    type: 'doughnut',
    data: {
      labels: rawMetrics.categories.labels,
      datasets: [{
        data: rawMetrics.categories.revenue,
        backgroundColor: ['#1E3A8A', '#0D9488', '#F59E0B'],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: ctx => {
              const val = ctx.raw;
              const total = rawMetrics.categories.revenue.reduce((a, b) => a + b, 0);
              const pct = ((val / total) * 100).toFixed(1);
              return `${ctx.label}: $${(val / 1000000).toFixed(2)}M (${pct}%)`;
            }
          }
        }
      },
      cutout: '65%'
    }
  });

  // 3. Regional Bar Chart
  const ctxBar = document.getElementById('regionalBarChart').getContext('2d');
  barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
      labels: rawMetrics.regions.map(r => r.region),
      datasets: [
        {
          label: 'Revenue ($)',
          data: rawMetrics.regions.map(r => r.revenue),
          backgroundColor: '#1E3A8A',
          borderRadius: 4
        },
        {
          label: 'Profit ($)',
          data: rawMetrics.regions.map(r => r.profit),
          backgroundColor: '#0D9488',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.dataset.label}: $${(ctx.raw / 1000000).toFixed(2)}M`
          }
        }
      },
      scales: {
        y: {
          grid: { color: '#E2E8F0' },
          ticks: {
            callback: value => '$' + (value / 1000000).toFixed(1) + 'M'
          }
        }
      }
    }
  });
}

function renderTable() {
  const tbody = document.getElementById('topProductsBody');
  tbody.innerHTML = '';

  rawMetrics.topProducts.forEach(prod => {
    let badgeClass = 'badge-blue';
    if (prod.status === 'High Margin') badgeClass = 'badge-green';
    if (prod.status === 'Discount Sensitive') badgeClass = 'badge-amber';

    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>#${prod.rank}</strong></td>
      <td><strong>${prod.name}</strong></td>
      <td>${prod.category}</td>
      <td>${prod.units.toLocaleString()}</td>
      <td>$${prod.revenue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
      <td>$${prod.profit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
      <td><strong>${prod.margin.toFixed(2)}%</strong></td>
      <td><span class="badge-tag ${badgeClass}">${prod.status}</span></td>
    `;
    tbody.appendChild(row);
  });
}

// Interactive filter simulation
function applyFilters() {
  const region = document.getElementById('regionFilter').value;
  const category = document.getElementById('categoryFilter').value;
  const year = document.getElementById('yearFilter').value;

  let multiplier = 1.0;
  if (region !== 'All') multiplier *= 0.35;
  if (category !== 'All') multiplier *= 0.45;
  if (year !== 'All') multiplier *= 0.33;

  const currentRevenue = rawMetrics.overall.revenue * multiplier;
  const currentProfit = rawMetrics.overall.profit * multiplier;
  const currentOrders = Math.round(rawMetrics.overall.orders * multiplier);
  const currentUnits = Math.round(rawMetrics.overall.units * multiplier);
  const currentMargin = (currentProfit / currentRevenue) * 100;

  document.getElementById('kpiRevenue').textContent = '$' + (currentRevenue / 1000000).toFixed(2) + 'M';
  document.getElementById('kpiProfit').textContent = '$' + (currentProfit / 1000000).toFixed(2) + 'M';
  document.getElementById('kpiOrders').textContent = currentOrders.toLocaleString();
  document.getElementById('kpiUnits').textContent = currentUnits.toLocaleString();
  document.getElementById('kpiMargin').textContent = currentMargin.toFixed(2) + '%';
}

function setupListeners() {
  document.getElementById('regionFilter').addEventListener('change', applyFilters);
  document.getElementById('categoryFilter').addEventListener('change', applyFilters);
  document.getElementById('yearFilter').addEventListener('change', applyFilters);

  document.getElementById('resetBtn').addEventListener('click', () => {
    document.getElementById('regionFilter').value = 'All';
    document.getElementById('categoryFilter').value = 'All';
    document.getElementById('yearFilter').value = 'All';
    applyFilters();
  });
}

window.addEventListener('DOMContentLoaded', () => {
  initCharts();
  renderTable();
  setupListeners();
});
