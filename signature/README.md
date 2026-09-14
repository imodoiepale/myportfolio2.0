# Gmail signature

Table-based HTML with hosted images. Gmail strips `<style>` blocks, so every rule is inline. After Vercel deploys this repo, the images live at `https://imodoiepale.vercel.app/signature/assets/`.

## Install

1. Confirm the globe panel loads: [https://imodoiepale.vercel.app/signature/assets/globe-panel.jpg](https://imodoiepale.vercel.app/signature/assets/globe-panel.jpg). If that 404s, wait for the deploy or check Vercel.
2. Open [https://imodoiepale.vercel.app/signature/](https://imodoiepale.vercel.app/signature/) in Chrome (desktop). Locally you can open `preview.html` instead; that file uses relative image paths.
3. Click inside the page, then Ctrl+A and Ctrl+C. Copy the rendered table, not the HTML source.
4. In Gmail: Settings gear → See all settings → General → Signature → Create new. Name it `James – Professional` and paste.
5. Under Signature defaults, set it for new emails and for replies/forwards.
6. Scroll to the bottom and click Save Changes.
7. Send a test to yourself and click every link:

   - https://imodoiepale.vercel.app
   - mailto:ijepale@gmail.com
   - tel:+254743854888
   - https://maps.google.com/?q=Nairobi,Kenya
   - https://x.com/boi_jimi
   - https://github.com/imodoiepale
   - https://wa.me/254743854888
   - https://instagram.com/epale_dev
   - https://tiktok.com/@epalle
   - https://www.linkedin.com/in/jamesepale/

The Gmail iOS/Android apps cannot paste a rich signature. Do this on desktop. If images show as broken, the site has not finished deploying.

## Edit later

Change a URL or swap an icon in `index.html`, then regenerate `preview.html` by replacing `https://imodoiepale.vercel.app/signature/assets/` with `assets/`. Commit and push so Vercel updates the hosted files.

## Assets

| File | Use |
| --- | --- |
| `assets/globe-panel.jpg` | Left panel (~210×280) |
| `assets/globe-panel.png` | Same art, PNG original |
| `assets/signature-name.png` | Handwritten name (Allura, transparent) |
| `assets/icons/*.png` | 128px circular icons, shown at 22px / 32px |
