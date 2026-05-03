// scripts/scrape_fund_page.js
//
// Scrapes a single HedgeFollow fund page like:
//   https://hedgefollow.com/funds/Pershing+Square+Capital+Management
//
// Run via the `javascript_tool` after navigating. Set N_HOLDINGS below if
// you want more or fewer than the top 10 holdings.
//
// HOW THE STAR RATING WORKS:
//   The element <span id="fundRat" class="stars-active" style="width:96%">
//   sits over a 5-star background. Width 96% = 4.8 stars out of 5.
//   We return both the raw width string and the computed star count.
//
// IMPORTANT: This page is JS-rendered AND Cloudflare-protected. Wait at
// least 4 seconds before reading. If document.title === "Just a moment..."
// the page is still on the Cloudflare challenge — wait longer or stop.

const N_HOLDINGS = 10;

new Promise(resolve => {
  setTimeout(() => {
    // Cloudflare challenge check
    if (document.title === 'Just a moment...') {
      resolve({ error: 'cloudflare_blocked', title: document.title });
      return;
    }

    // ---- Star rating ----
    const fundRat = document.getElementById('fundRat');
    let ratingWidth = null;
    let ratingStars = null;
    if (fundRat) {
      ratingWidth = fundRat.style.width || null;            // e.g. "96%"
      const pct = parseFloat((ratingWidth || '0').replace('%', ''));
      ratingStars = isFinite(pct) ? Math.round((pct / 100) * 5 * 10) / 10 : null;
    }

    // ---- Summary row (table[0]) ----
    // Columns: Hedge Fund | Portfolio Manager | Performance | AUM (13F) | # of Holdings | ...
    const tables = Array.from(document.querySelectorAll('table'));
    const summaryRow = tables[0]?.querySelectorAll('tr')[1];
    const summaryCells = summaryRow ? Array.from(summaryRow.querySelectorAll('td')).map(c => c.innerText.trim()) : [];

    const summary = {
      fund_name:   summaryCells[0] || null,
      manager:     summaryCells[1] || null,
      performance: summaryCells[2] || null,   // latest quarter
      aum_13f:     summaryCells[3] || null,
      holdings_n:  summaryCells[4] || null,
    };

    // ---- Top holdings (table[1]) ----
    // Columns: Stock | Company | % of Portfolio | Shares Owned | Value Owned | ...
    const holdingsTable = tables[1];
    const holdings = [];
    if (holdingsTable) {
      const rows = holdingsTable.querySelectorAll('tr');
      for (let i = 1; i <= N_HOLDINGS && i < rows.length; i++) {
        const c = rows[i].querySelectorAll('td');
        if (c.length < 3) continue;
        holdings.push({
          ticker:        (c[0]?.innerText || '').trim(),
          company:       (c[1]?.innerText || '').trim(),
          pct_portfolio: (c[2]?.innerText || '').trim(),
          // Cells 3–5 vary by page — usually shares, value, latest activity
          col3: (c[3]?.innerText || '').trim(),
          col4: (c[4]?.innerText || '').trim(),
        });
      }
    }

    // ---- Total AUM (often shown further down in a "Investment Advisor" table) ----
    let total_aum = null;
    tables.forEach(t => {
      const txt = t.innerText || '';
      if (txt.includes('Total AUM') || txt.includes('Discretionary AUM')) {
        const rs = t.querySelectorAll('tr');
        if (rs.length >= 2) {
          const cs = Array.from(rs[1].querySelectorAll('td')).map(c => c.innerText.trim());
          if (cs.length >= 4) total_aum = cs[3];
        }
      }
    });

    resolve({
      url: window.location.href,
      title: document.title,
      rating: { width: ratingWidth, stars: ratingStars },
      summary,
      total_aum,
      holdings,
    });
  }, 4000);
});
