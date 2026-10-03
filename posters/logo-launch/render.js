// Renders a poster page to PNG at 1080x1350 (1x) and 2160x2700 (2x).
// Usage: node render.js            -> index.html    -> icl-s2-logo-launch(.png|@2x.png)
//        node render.js announce   -> announce.html -> icl-s2-logo-launched(.png|@2x.png)
// Needs playwright; uses PLAYWRIGHT_BROWSERS_PATH.
const path = require('path');
const { chromium } = require('playwright');

const PAGES = {
  index: 'icl-s2-logo-launch',
  announce: 'icl-s2-logo-launched',
};

(async () => {
  const name = process.argv[2] || 'index';
  const base = PAGES[name];
  if (!base) throw new Error(`unknown page "${name}", expected one of: ${Object.keys(PAGES).join(', ')}`);
  const browser = await chromium.launch();
  const src = 'file://' + path.resolve(__dirname, `${name}.html`);
  for (const scale of [1, 2]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
    await page.goto(src);
    await page.evaluate(() => document.fonts.ready);
    const out = path.resolve(__dirname, scale === 1 ? `${base}.png` : `${base}@2x.png`);
    await page.locator('.poster').screenshot({ path: out });
    console.log('wrote', out);
    await page.close();
  }
  await browser.close();
})();
