// Renders index.html to PNG at 1080x1350 (1x) and 2160x2700 (2x).
// Usage: node render.js   (needs playwright; uses PLAYWRIGHT_BROWSERS_PATH)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const src = 'file://' + path.resolve(__dirname, 'index.html');
  for (const scale of [1, 2]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
    await page.goto(src);
    await page.evaluate(() => document.fonts.ready);
    const out = path.resolve(__dirname, scale === 1 ? 'icl-s2-logo-launch.png' : 'icl-s2-logo-launch@2x.png');
    await page.locator('.poster').screenshot({ path: out });
    console.log('wrote', out);
    await page.close();
  }
  await browser.close();
})();
