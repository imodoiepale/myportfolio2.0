# Gmail signature

Table-based HTML with hosted images. Gmail strips `<style>` blocks, so every rule in the table is inline. After Vercel deploys this repo, images live at `https://imodoiepale.vercel.app/signature/assets/`. The signature table is **540px** wide so it reads as an email footer, not a banner.

The **install steps live on the page** you copy from: [https://imodoiepale.vercel.app/signature/](https://imodoiepale.vercel.app/signature/)

`preview.html` is a local look at the table. Do not paste it into Gmail. Relative image paths will break.

## Email

The live signature uses **ijepale@gmail.com** for the visible address and `mailto:`.

`james@nsait.co.ke` was on an earlier mockup. Do not put it in `index.html` or `preview.html`.

## Install

1. Confirm the globe loads: [https://imodoiepale.vercel.app/signature/assets/globe-panel.jpg](https://imodoiepale.vercel.app/signature/assets/globe-panel.jpg). If that 404s, wait for Vercel.
2. Open [https://imodoiepale.vercel.app/signature/](https://imodoiepale.vercel.app/signature/) in **Chrome on a computer**.
3. Click **Copy signature**. Do not Ctrl+A the whole page. That copies the instructions and page padding, which shows up as empty space in the email.
4. Gmail → gear → See all settings → General → Signature. Create new (`James – Professional`) or replace the existing one. Paste.
5. Signature defaults: new emails and replies/forwards.
6. Scroll to the **bottom** of Settings and click Save Changes.
7. Compose a new email. If Gmail inserted a blank line above the globe, click it and press Backspace.
8. Send a test to yourself and click every link:

   - https://imodoiepale.vercel.app
   - mailto:ijepale@gmail.com
   - tel:+254743854888
   - https://maps.google.com/?q=Nairobi,Kenya
   - https://x.com/boi_jimi
   - https://github.com/imodoiepale
   - https://wa.me/254743854888
   - https://instagram.com/epale_dev
   - https://www.tiktok.com/@b0ijimi
   - https://www.linkedin.com/in/jamesepale/

The Gmail iOS/Android apps cannot paste a rich signature. Set it on desktop. If images are broken, the site has not finished deploying, or you copied from a local file.

## Edit later

Change a URL or swap an icon in `index.html`, then update `preview.html` by replacing `https://imodoiepale.vercel.app/signature/assets/` with `assets/`. Commit and push so Vercel updates the hosted files. Then copy the signature into Gmail again.

## Assets

| File | Use |
| --- | --- |
| `assets/globe-panel.jpg` | Left panel (Africa globe), shown at 150×158 |
| `assets/globe-panel.png` | Same crop, PNG original |
| `assets/signature-name.png` | Handwritten name with underline (transparent, padded so Gmail does not clip the J), shown at 236×59 |
| `assets/icons/*.png` | Circular icons, shown at 16px (contact) / 22px (social); source files stay 128px |
