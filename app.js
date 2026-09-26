let rawSalesData = [];
let trendChart, categoryChart, regionChart, discountImpactChart;

fetch('sales_data.json')
  .then(res => res.json())
  .then(data => {
    rawSalesData = data;
    initDashboard();
  })
  .catch(err => {
    console.error('Error loading sales json data:', err);
  });

function initDashboard() {
  document.getElementById('regionFilter').addEventListener('change', updateDashboard);
  document.getElementById('categoryFilter').addEventListener('change', updateDashboard);
  document.getElementById('discountFilter').addEventListener('change', updateDashboard);
  
  updateDashboard();
}

function updateDashboard() {
  const selectedRegion = document.getElementById('regionFilter').value;
  const selectedCategory = document.getElementById('categoryFilter').value;
  const selectedDiscount = document.getElementById('discountFilter').value;

  const filtered = rawSalesData.filter(d => {
    const regionMatch = selectedRegion === 'All' || d.region === selectedRegion;
    const categoryMatch = selectedCategory === 'All' || d.category === selectedCategory;
    let discountMatch = true;
    if (selectedDiscount === 'HighErosion') discountMatch = d.high_discount_erosion;
    if (selectedDiscount === 'Normal') discountMatch = !d.high_discount_erosion;
    return regionMatch && categoryMatch && discountMatch;
  });

  // Calculate KPIs
  const totalRev = filtered.reduce((acc, curr) => acc + curr.net_revenue, 0);
  const totalProfit = filtered.reduce((acc, curr) => acc + curr.profit, 0);
  const overallMargin = totalRev > 0 ? (totalProfit / totalRev) * 100 : 0;
  const highErosionCount = filtered.filter(d => d.high_discount_erosion).length;

  document.getElementById('kpiRevenue').innerText = `$${(totalRev / 1000000).toFixed(2)}M`;
  document.getElementById('kpiProfit').innerText = `$${(totalProfit / 1000).toFixed(2)}K`;
  document.getElementById('kpiMargin').innerText = `${overallMargin.toFixed(2)}%`;
  document.getElementById('kpiErosion').innerText = `${highErosionCount} Orders`;

  renderCharts(filtered);
  renderTable(filtered.slice(0, 15));
}

function renderCharts(data) {
  // Monthly trends
  const monthlyData = {};
  data.forEach(d => {
    const month = d.order_date.substring(0, 7);
    if (!monthlyData[month]) monthlyData[month] = { rev: 0, profit: 0 };
    monthlyData[month].rev += d.net_revenue;
    monthlyData[month].profit += d.profit;
  });
  const months = Object.keys(monthlyData).sort();
  const revs = months.map(m => monthlyData[m].rev);
  const profits = months.map(m => monthlyData[m].profit);

  if (trendChart) trendChart.destroy();
  const ctx1 = document.getElementById('salesTrendChart').getContext('2d');
  trendChart = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: months,
      datasets: [
        { label: 'Revenue ($)', data: revs, borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: true, tension: 0.3 },
        { label: 'Profit ($)', data: profits, borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.1)', fill: true, tension: 0.3 }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9ca3af' } } }, scales: { x: { ticks: { color: '#9ca3af' } }, y: { ticks: { color: '#9ca3af' } } } }
  });

  // Category breakdown
  const catData = {};
  data.forEach(d => {
    catData[d.category] = (catData[d.category] || 0) + d.net_revenue;
  });
  if (categoryChart) categoryChart.destroy();
  const ctx2 = document.getElementById('categoryChart').getContext('2d');
  categoryChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: Object.keys(catData),
      datasets: [{ data: Object.values(catData), backgroundColor: ['#3b82f6', '#8b5cf6', '#06b6d4', '#f59e0b'] }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#9ca3af' } } } }
  });

  // Regional breakdown
  const regData = {};
  data.forEach(d => {
    regData[d.region] = (regData[d.region] || 0) + d.net_revenue;
  });
  if (regionChart) regionChart.destroy();
  const ctx3 = document.getElementById('regionChart').getContext('2d');
  regionChart = new Chart(ctx3, {
    type: 'bar',
    data: {
      labels: Object.keys(regData),
      datasets: [{ label: 'Revenue by Region ($)', data: Object.values(regData), backgroundColor: '#60a5fa', borderRadius: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#9ca3af' } }, y: { ticks: { color: '#9ca3af' } } } }
  });

  // Discount vs Profit Margin Scatter / Grouped Bar
  const discGroups = { '0%': [], '5-10%': [], '15-20%': [], '25%+ (Erosion)': [] };
  data.forEach(d => {
    if (d.discount_pct === 0) discGroups['0%'].push(d.profit_margin);
    else if (d.discount_pct <= 0.10) discGroups['5-10%'].push(d.profit_margin);
    else if (d.discount_pct <= 0.20) discGroups['15-20%'].push(d.profit_margin);
    else discGroups['25%+ (Erosion)'].push(d.profit_margin);
  });
  const avgMargins = Object.keys(discGroups).map(k => {
    const arr = discGroups[k];
    return arr.length ? (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1) : 0;
  });

  if (discountImpactChart) discountImpactChart.destroy();
  const ctx4 = document.getElementById('discountImpactChart').getContext('2d');
  discountImpactChart = new Chart(ctx4, {
    type: 'bar',
    data: {
      labels: Object.keys(discGroups),
      datasets: [{ label: 'Avg Profit Margin (%)', data: avgMargins, backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'], borderRadius: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#9ca3af' } }, y: { ticks: { color: '#9ca3af' } } } }
  });
}

function renderTable(sampleData) {
  const tbody = document.getElementById('transactionTableBody');
  tbody.innerHTML = '';
  sampleData.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${row.order_id}</strong></td>
      <td>${row.order_date}</td>
      <td>${row.region}</td>
      <td>${row.category}</td>
      <td>${row.product}</td>
      <td>$${row.net_revenue.toLocaleString()}</td>
      <td>$${row.profit.toLocaleString()}</td>
      <td><span class="pill ${row.profit_margin >= 20 ? 'pill-success' : 'pill-danger'}">${row.profit_margin}%</span></td>
      <td>${(row.discount_pct * 100).toFixed(0)}%</td>
    `;
    tbody.appendChild(tr);
  });
}
