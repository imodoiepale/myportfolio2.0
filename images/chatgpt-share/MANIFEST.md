# ChatGPT share image recovery

Recovered **2026-09-14** from the local Codex desktop Chromium cache (the public share at `https://chatgpt.com/share/6aa7f342-2a38-83e9-834e-17ca7770b81c` only exposes `sediment://` pointers; the actual PNGs were already on disk from viewing that conversation in the Codex app).

Conversation id: `6aa7f342-2a38-83e9-834e-17ca7770b81c`

Cache source (duplicates at 12:19 and 16:08; later copies used):

`C:\Users\itsupport\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Roaming\Codex\web\Codex\Default\Cache\Cache_Data\`

Dimensions via Python Pillow.

## Recovered from Codex cache (ChatGPT conversation)

| Original path | Size | Dimensions | Destination | Likely identity |
|---|---:|---|---|---|
| `...\Cache_Data\f_000099` (dup `f_000099` only; 16:08) | 1,256,842 | 1672×941 RGB | `globe-signature-banner.png` + `original-banner-1672x941-1256842.png` | Wide 16:9 email signature composite with LinkedIn. Matches `wide_clean_modern_professional_email_signature_s_1.png` (wxh 1672×941). |
| `...\Cache_Data\f_000093` (dup `f_00003d`) | 1,256,170 | 1672×941 RGB | `globe-signature-banner-no-linkedin.png` + `original-banner-1672x941-1256170.png` | Same 16:9 layout without LinkedIn. Matches `a_clean_modern_professional_email_signature_ba_1.png`. |
| `...\Cache_Data\f_00009c` (dup `f_000041`) | 1,257,778 | 1906×825 RGBA | `signature-dark-composite.png` + `original-wide-1906x825-1257778.png` | Dark/black composite of globe panel + contact block. Exact `size_bytes` 1257778 for `file_00000000d360820c984000e29c9b3999`. Text is distorted. |
| `...\Cache_Data\f_00009e` | 1,303,991 | 1774×887 RGB | `signature-early-layout.png` + `original-wide-1774x887-1303991.png` | Earlier signature layout (“Imodoi Epale”, four value tiles). |
| `...\Cache_Data\f_000094` (dup `f_00003b`) | 2,068,721 | 1122×1402 RGB | `hero-connect-create-grow.png` + `original-hero-1122x1402-2068721.png` | Portrait hero poster. Matches `a_high_tech_digital_sci_fi_corporate_poster_hero_1_batch_1.png` (wxh 1122×1402). |
| `...\Cache_Data\f_00009d` (dup `f_00003f`) | 824,565 | 1254×1254 RGBA | `icon-x.png` + `original-icon-1254-824565.png` | X / Twitter circle icon. |
| `...\Cache_Data\f_000097` (dup `f_00003e`) | 747,116 | 1254×1254 RGBA | `icon-github.png` + `original-icon-1254-747116.png` | GitHub circle icon. |
| `...\Cache_Data\f_000098` (dup `f_000040`) | 964,313 | 1254×1254 RGBA | `icon-whatsapp.png` + `original-icon-1254-964313.png` | WhatsApp circle icon. |
| `...\Cache_Data\f_000096` (dup `f_00003a`) | 991,868 | 1254×1254 RGBA | `icon-instagram.png` + `original-icon-1254-991868.png` | Instagram circle icon. Matches `a_clean_graphic_illustration_of_the_instagram_app_7_batch_7.png`. |
| `...\Cache_Data\f_00009a` (dup `f_000039`) | 779,330 | 1254×1254 RGBA | `icon-tiktok.png` + `original-icon-1254-779330.png` | TikTok circle icon. |
| `...\Cache_Data\f_000095` (dup `f_000042`) | 964,346 | 1254×1254 RGBA | `icon-website.png` + `original-icon-1254-964346.png` | Website / globe circle icon. |
| `...\Cache_Data\f_00009b` (dup `f_00003c`) | 728,673 | 1254×1254 RGBA | `icon-phone.png` + `original-icon-1254-728673.png` | Phone circle icon. |

All seven square icons match the conversation batch (`a_clean_vector_style_icon_image_on_a_transparent_b_2_batch_2.png` through `_8_batch_8.png`, 1254×1254).

## Already in this folder (not from Codex cache)

| Path | Size | Dimensions | Notes |
|---|---:|---|---|
| `globe-panel.png` | 402,343 | 864×1152 JPEG | Cursor-generated portrait globe card (same bytes as `signature/assets/globe-panel.png`, 17:22). **Not** a ChatGPT conversation file. Left in place; not overwritten. No standalone ChatGPT globe-panel PNG was in cache (the globe card only appears inside the 16:9 composites). |
| `og-share.png` | 135,973 | 1200×630 | ChatGPT share OG image (`ogimg.chatgpt.com/.../igc.png`), from `%TEMP%\chatgpt_dl`. |
| `old-site-screenshot.png` | 62,871 | 1024×485 | Prior site screenshot, unrelated to image gen. |

## Copied into `signature/assets`

Existing `signature/assets/globe-panel.png` was **not overwritten** by this recovery (it was a Cursor-generated JPEG at copy time; a sibling later replaced it with a larger PNG, now 1,166,870 bytes). Cache composites were not copied over it.

Icons copied (no prior files to compare):

- `signature/assets/icon-x.png`
- `signature/assets/icon-github.png`
- `signature/assets/icon-whatsapp.png`
- `signature/assets/icon-instagram.png`
- `signature/assets/icon-tiktok.png`
- `signature/assets/icon-website.png`
- `signature/assets/icon-phone.png`

Same seven files also copied into empty `signature/assets/icons/`.

## Missing from cache

- Standalone ChatGPT `globe-panel.png` (portrait left globe card as its own file). Only embedded in 16:9 banners.
- Standalone `icon-linkedin.png` (LinkedIn appears only inside `globe-signature-banner.png`).
- Original ChatGPT filenames (`a_clean_modern_professional_email_signature_ba_1.png`, `/mnt/data/ghostwriter_images/generated/...`) — those paths are the ChatGPT Linux sandbox, not present on this Windows disk.
- ChatGPT desktop app data (`%APPDATA%\ChatGPT`, `%LOCALAPPDATA%\ChatGPT`) does not exist.

## Other image-heavy folders found (not copied)

Codex session image-gen (unrelated chats, Aug–Sep 2026), 70 PNGs:

```
C:\Users\itsupport\.codex\generated_images\
  01a00fb3-3060-7b81-aa51-b5da5f59a6cd\   15 png  (2026-08-17)
  01a0195b-25ea-73f2-94f4-6673415b3d61\   17 png  (2026-08-19/20)
  01a0435b-983a-7e00-b0b3-5c7741d0628f\   10 png  (2026-09-04)
  01a08083-03b3-7491-823e-c948e7b13b34\   12 png  (2026-09-09)
  01a08a60-b6bc-7a60-8c23-ecc4baeb6faf\    6 png  (2026-09-10)
  01a08a61-b344-7ff1-a548-3f90d9e8de7a\   10 png  (2026-09-10)
```

`C:\Users\itsupport\Documents\Codex\` is dated Codex worktrees (`2026-08-17` … `2026-09-14`), not ChatGPT image storage.

`C:\Users\itsupport\Documents\ChatGPT\` only contains `bulk-printing` (no images).
