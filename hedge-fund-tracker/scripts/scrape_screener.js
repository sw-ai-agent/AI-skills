// scripts/scrape_screener.js
//
// Scrapes the HedgeFollow top-hedge-funds.php or largest-hedge-funds.php screener.
// Run inside the browser via the Claude in Chrome `javascript_tool` after navigating
// to one of those pages. Wraps the result in a Promise so the JS exec wrapper waits
// for the JS-rendered table to populate.
//
// Optional: change filter dropdowns first.
//   - Set #top to '20', '50', or '100'
//   - Set #institution_type to 'popular_hedge_funds' | 'hedge_funds' | 'all'
//   - Set #top_by to 'weighted3YPerfTop20' | '3YPerfTop20' | 'hf_rating'
// After changing, dispatch a 'change' event with bubbles:true.
//
// Returns: array of objects, one per fund row.

new Promise(resolve => {
  // Wait 4s for table to render after navigation / filter change
  setTimeout(() => {
    const rows = document.querySelectorAll('table tr');
    const data = [];
    let headers = null;

    rows.forEach(row => {
      const cells = row.querySelectorAll('td, th');
      if (cells.length < 4) return;  // skip ad rows / spacers

      const values = Array.from(cells).map(c => c.innerText.trim());

      if (!headers) {
        headers = values;
        return;
      }

      // Build object using headers
      const obj = {};
      headers.forEach((h, i) => { obj[h] = values[i] || ''; });

      // Try to extract clean fund name + manager from the "Fund Manager" cell
      // Format is typically: "Fund Name\nManager Name"
      const fmCell = obj['Fund Manager'] || values[1] || '';
      const parts = fmCell.split('\n').map(s => s.trim()).filter(Boolean);
      obj._fund_name = parts[0] || '';
      obj._manager   = parts[1] || '';

      data.push(obj);
    });

    resolve({ headers, count: data.length, rows: data });
  }, 4000);
});
