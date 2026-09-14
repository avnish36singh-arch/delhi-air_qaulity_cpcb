/* ==========================================================================
   SIGNAL EARTH - KANPUR INVESTIGATION CONTROLLER
   Dual-Station CPCB / UPPCB Telemetry Analytics & Plotly Visualization
   ========================================================================== */

const OBSIDIAN_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: { family: 'Inter, system-ui, sans-serif', color: '#94a3b8', size: 12 },
  margin: { t: 40, r: 24, b: 45, l: 55 },
  xaxis: { 
    gridcolor: 'rgba(255, 255, 255, 0.04)', 
    zerolinecolor: 'rgba(255, 255, 255, 0.08)',
    tickfont: { size: 11, color: '#64748b' }
  },
  yaxis: { 
    gridcolor: 'rgba(255, 255, 255, 0.04)', 
    zerolinecolor: 'rgba(255, 255, 255, 0.08)',
    tickfont: { size: 11, color: '#64748b' }
  }
};

const CONFIG = {
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d']
};

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

fetch('data/kanpur/summary.json')
  .then(r => r.json())
  .then(data => {
    renderKanpurMonthly(data.monthly);
    renderKanpurDiurnal(data.diurnal);
  })
  .catch(err => console.error('Kanpur data error:', err));

function renderKanpurMonthly(monthlyData) {
  // Kalyanpur vs Nehru Nagar
  const kalyanpur = monthlyData.filter(d => d.location_name.includes('Kalyanpur')).sort((a, b) => a.month - b.month);
  const nehru = monthlyData.filter(d => d.location_name.includes('Nehru')).sort((a, b) => a.month - b.month);

  const months = kalyanpur.map(d => MONTH_NAMES[d.month - 1]);

  const traces = [
    {
      x: months,
      y: kalyanpur.map(d => d.pm25),
      mode: 'lines+markers',
      name: 'NSI Kalyanpur — PM2.5 (µg/m³)',
      line: { color: '#a3e635', width: 2.8, shape: 'spline' },
      marker: { size: 6, color: '#a3e635' }
    },
    {
      x: months,
      y: nehru.map(d => d.pm25),
      mode: 'lines+markers',
      name: 'Nehru Nagar — PM2.5 (µg/m³)',
      line: { color: '#06b6d4', width: 2.8, shape: 'spline' },
      marker: { size: 6, color: '#06b6d4' }
    },
    {
      x: months,
      y: kalyanpur.map(d => d.pm10),
      mode: 'lines',
      name: 'NSI Kalyanpur — PM10 (µg/m³)',
      line: { color: 'rgba(163, 230, 53, 0.4)', width: 1.5, dash: 'dot', shape: 'spline' }
    },
    {
      x: months,
      y: nehru.map(d => d.pm10),
      mode: 'lines',
      name: 'Nehru Nagar — PM10 (µg/m³)',
      line: { color: 'rgba(6, 182, 212, 0.4)', width: 1.5, dash: 'dot', shape: 'spline' }
    }
  ];

  const layout = {
    ...OBSIDIAN_LAYOUT,
    yaxis: {
      ...OBSIDIAN_LAYOUT.yaxis,
      title: { text: 'Concentration (µg/m³)', font: { size: 12, color: '#94a3b8' } }
    },
    legend: {
      orientation: 'h',
      y: 1.12,
      font: { size: 11, color: '#94a3b8' }
    },
    hoverlabel: {
      bgcolor: '#090d16',
      bordercolor: 'rgba(255, 255, 255, 0.15)',
      font: { family: 'Inter', color: '#ffffff', size: 12 }
    },
    shapes: [
      { type: 'line', xref: 'paper', x0: 0, x1: 1, y0: 60, y1: 60, line: { color: 'rgba(239, 68, 68, 0.35)', width: 1, dash: 'dot' } }
    ],
    annotations: [
      { xref: 'paper', yref: 'y', x: 0.99, y: 65, text: 'CPCB 24-hr PM2.5 Standard (60 µg/m³)', showarrow: false, font: { size: 9, color: 'rgba(239, 68, 68, 0.7)', family: 'monospace' }, xanchor: 'right' }
    ]
  };

  Plotly.newPlot('chart-kanpur-monthly', traces, layout, CONFIG);
}

function renderKanpurDiurnal(diurnalData) {
  const kalyanpur = diurnalData.filter(d => d.location_name.includes('Kalyanpur')).sort((a, b) => a.hour - b.hour);
  const nehru = diurnalData.filter(d => d.location_name.includes('Nehru')).sort((a, b) => a.hour - b.hour);

  const hours = kalyanpur.map(d => `${String(d.hour).padStart(2, '0')}:00`);

  const traces = [
    {
      x: hours,
      y: kalyanpur.map(d => d.pm25),
      mode: 'lines+markers',
      name: 'NSI Kalyanpur — PM2.5 Diurnal',
      line: { color: '#f59e0b', width: 2.8, shape: 'spline' },
      marker: { size: 5, color: '#f59e0b' },
      fill: 'tozeroy',
      fillcolor: 'rgba(245, 158, 11, 0.04)'
    },
    {
      x: hours,
      y: nehru.map(d => d.pm25),
      mode: 'lines+markers',
      name: 'Nehru Nagar — PM2.5 Diurnal',
      line: { color: '#ec4899', width: 2.8, shape: 'spline' },
      marker: { size: 5, color: '#ec4899' },
      fill: 'tozeroy',
      fillcolor: 'rgba(236, 72, 153, 0.04)'
    }
  ];

  const layout = {
    ...OBSIDIAN_LAYOUT,
    xaxis: {
      ...OBSIDIAN_LAYOUT.xaxis,
      title: { text: 'Hour of Day (IST)', font: { size: 12, color: '#94a3b8' } }
    },
    yaxis: {
      ...OBSIDIAN_LAYOUT.yaxis,
      title: { text: 'Mean PM2.5 (µg/m³)', font: { size: 12, color: '#94a3b8' } }
    },
    legend: {
      orientation: 'h',
      y: 1.12,
      font: { size: 11, color: '#94a3b8' }
    },
    hoverlabel: {
      bgcolor: '#090d16',
      bordercolor: 'rgba(255, 255, 255, 0.15)',
      font: { family: 'Inter', color: '#ffffff', size: 12 }
    },
    annotations: [
      {
        x: '21:00',
        y: 80,
        xref: 'x',
        yref: 'y',
        text: 'Inversion Peak (9–10 PM)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: '#ec4899',
        font: { size: 10, color: '#f8fafc', family: 'monospace' },
        bgcolor: 'rgba(15, 23, 42, 0.85)',
        bordercolor: 'rgba(236, 72, 153, 0.5)'
      },
      {
        x: '15:00',
        y: 35,
        xref: 'x',
        yref: 'y',
        text: 'Convective Mixing Minimum (3–4 PM)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: '#f59e0b',
        font: { size: 10, color: '#f8fafc', family: 'monospace' },
        bgcolor: 'rgba(15, 23, 42, 0.85)',
        bordercolor: 'rgba(245, 158, 11, 0.5)'
      }
    ]
  };

  Plotly.newPlot('chart-kanpur-diurnal', traces, layout, CONFIG);
}
