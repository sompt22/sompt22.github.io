---
title: "SOMPT22 Benchmark Leaderboard"
feature_text: |
  ## Benchmark Leaderboard
  Multi-Pedestrian Tracking on SOMPT22 Test Set
feature_image: "/assets/cam2_anno.png"
layout: leaderboard
---

<div class="leaderboard-info">
  <p>
    Rankings are based on <strong>HOTA</strong> (Higher Order Tracking Accuracy) as the primary metric.
    All results are evaluated on the <strong>SOMPT22 test set</strong> using
    <a href="https://github.com/JonathonLuiten/TrackEval">TrackEval</a>.
    To submit your results, see the <a href="/challenge/">Challenge page</a>.
  </p>
</div>

<div class="leaderboard-controls">
  <input type="text" id="search-input" placeholder="Search team or tracker..." class="search-box" />
  <span class="entry-count" id="entry-count"></span>
</div>

<div class="table-responsive">
<table id="leaderboard-table" class="leaderboard-table">
  <thead>
    <tr>
      <th class="sortable col-rank" data-col="rank">#</th>
      <th class="sortable col-team" data-col="team">Team</th>
      <th class="sortable col-tracker" data-col="tracker">Tracker</th>
      <th class="sortable col-hota active desc" data-col="hota">HOTA ↓</th>
      <th class="sortable col-deta" data-col="deta">DetA</th>
      <th class="sortable col-assa" data-col="assa">AssA</th>
      <th class="sortable col-mota" data-col="mota">MOTA</th>
      <th class="sortable col-idf1" data-col="idf1">IDF1</th>
      <th class="sortable col-fp" data-col="fp">FP</th>
      <th class="sortable col-fn" data-col="fn">FN</th>
      <th class="sortable col-ids" data-col="ids">IDs</th>
      <th class="sortable col-fps" data-col="fps">FPS</th>
      <th class="col-date">Date</th>
      <th class="col-links">Links</th>
    </tr>
  </thead>
  <tbody id="leaderboard-body">
    <!-- Populated by JavaScript -->
  </tbody>
</table>
</div>

<script>
const leaderboardData = {{ site.data.leaderboard | jsonify }};

let sortCol = 'hota';
let sortAsc = false;
let filterText = '';

function renderTable() {
  const filtered = leaderboardData.filter(row => {
    const q = filterText.toLowerCase();
    return !q || row.team.toLowerCase().includes(q) || row.tracker.toLowerCase().includes(q) || (row.affiliation && row.affiliation.toLowerCase().includes(q));
  });

  const sorted = [...filtered].sort((a, b) => {
    let va = a[sortCol], vb = b[sortCol];
    if (typeof va === 'string') va = va.toLowerCase();
    if (typeof vb === 'string') vb = vb.toLowerCase();
    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  });

  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';

  sorted.forEach((row, idx) => {
    const tr = document.createElement('tr');
    if (idx === 0) tr.classList.add('rank-1');
    if (idx === 1) tr.classList.add('rank-2');
    if (idx === 2) tr.classList.add('rank-3');

    const paperLink = row.paper ? `<a href="${row.paper}" target="_blank" title="Paper">📄</a>` : '';
    const codeLink  = row.code  ? `<a href="${row.code}"  target="_blank" title="Code">💻</a>` : '';

    tr.innerHTML = `
      <td class="col-rank">${idx + 1}</td>
      <td class="col-team" title="${row.affiliation || ''}">${row.team}</td>
      <td class="col-tracker">${row.tracker}</td>
      <td class="col-hota metric-primary">${row.hota.toFixed(1)}</td>
      <td class="col-deta">${row.deta.toFixed(1)}</td>
      <td class="col-assa">${row.assa.toFixed(1)}</td>
      <td class="col-mota">${row.mota.toFixed(1)}</td>
      <td class="col-idf1">${row.idf1.toFixed(1)}</td>
      <td class="col-fp">${row.fp.toLocaleString()}</td>
      <td class="col-fn">${row.fn.toLocaleString()}</td>
      <td class="col-ids">${row.ids.toLocaleString()}</td>
      <td class="col-fps">${row.fps.toFixed(1)}</td>
      <td class="col-date">${row.date}</td>
      <td class="col-links">${paperLink} ${codeLink}</td>
    `;
    body.appendChild(tr);
  });

  document.getElementById('entry-count').textContent = `${sorted.length} entries`;
}

function updateSortHeaders() {
  document.querySelectorAll('th.sortable').forEach(th => {
    th.classList.remove('active', 'asc', 'desc');
    if (th.dataset.col === sortCol) {
      th.classList.add('active', sortAsc ? 'asc' : 'desc');
      th.textContent = th.textContent.replace(/ [↑↓]$/, '');
      th.textContent += sortAsc ? ' ↑' : ' ↓';
    } else {
      th.textContent = th.textContent.replace(/ [↑↓]$/, '');
    }
  });
}

document.querySelectorAll('th.sortable').forEach(th => {
  th.style.cursor = 'pointer';
  th.addEventListener('click', () => {
    if (sortCol === th.dataset.col) {
      sortAsc = !sortAsc;
    } else {
      sortCol = th.dataset.col;
      // Lower is better for FP/FN/IDs, higher is better for metrics
      sortAsc = ['fp', 'fn', 'ids', 'rank'].includes(sortCol);
    }
    updateSortHeaders();
    renderTable();
  });
});

document.getElementById('search-input').addEventListener('input', e => {
  filterText = e.target.value;
  renderTable();
});

renderTable();
updateSortHeaders();
</script>

<style>
.leaderboard-info {
  background: #f8f9fa;
  border-left: 4px solid #0d84f7;
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
  border-radius: 0 4px 4px 0;
}
.leaderboard-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.search-box {
  padding: 0.4rem 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 260px;
}
.entry-count {
  color: #666;
  font-size: 0.85rem;
}
.table-responsive {
  overflow-x: auto;
}
.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}
.leaderboard-table th,
.leaderboard-table td {
  padding: 0.5rem 0.6rem;
  border: 1px solid #e0e0e0;
  white-space: nowrap;
  text-align: center;
}
.leaderboard-table th {
  background: #2d3748;
  color: #fff;
  font-weight: 600;
  user-select: none;
}
.leaderboard-table th.active {
  background: #0d84f7;
}
.leaderboard-table th.sortable:hover {
  background: #1a5fa8;
}
.col-team, .col-tracker {
  text-align: left !important;
}
.metric-primary {
  font-weight: 700;
  color: #0d84f7;
}
.rank-1 td { background: #fffbe6; }
.rank-2 td { background: #f5f5f5; }
.rank-3 td { background: #fdf3e3; }
.leaderboard-table tbody tr:hover td {
  background: #e8f4fd !important;
}
.col-links a {
  margin: 0 2px;
  text-decoration: none;
  font-size: 1rem;
}
</style>
