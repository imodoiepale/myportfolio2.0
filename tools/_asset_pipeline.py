"""Download NSAIT imagery, AI-lab SVGs, compress project art, render signature name."""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
CTX = ssl.create_default_context()


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        return resp.read()


def save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def looks_like_image(data: bytes) -> bool:
    return data[:8] == b"\x89PNG\r\n\x1a\n" or data[:2] == b"\xff\xd8" or data[:4] == b"RIFF" or data[:4] == b"<svg" or data[:5] == b"<?xml" or data[:4] == b"GIF8"


def compress_image(src: Path, max_px: int = 1200, max_kb: int = 250) -> None:
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    if max(img.size) > max_px:
        img.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
    ext = src.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        img = img.convert("RGB")
        q = 86
        while q >= 55:
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=q, optimize=True)
            if buf.tell() <= max_kb * 1024 or q == 55:
                src.write_bytes(buf.getvalue())
                print(f"jpg {src.name} {src.stat().st_size // 1024}KB {img.size}")
                return
            q -= 6
    else:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        # Prefer JPEG for opaque generated covers if still huge
        if img.mode == "RGB" or (img.mode == "RGBA" and img.getextrema()[-1][0] == 255):
            rgb = img.convert("RGB")
            q = 86
            dest = src.with_suffix(".png")
            while q >= 52:
                buf = BytesIO()
                rgb.save(buf, format="JPEG", quality=q, optimize=True)
                if buf.tell() <= max_kb * 1024 or q == 52:
                    # keep original extension as png if that's what HTML expects — write JPEG bytes into png? NO.
                    # Convert large png covers to stay png but quantized, or rewrite as jpg.
                    if buf.tell() <= max_kb * 1024:
                        jpg_path = src.with_suffix(".jpg")
                        if src.suffix.lower() == ".png" and src.parent.name == "projects":
                            # keep png name: recompress as optimized PNG first
                            pass
                    break
                q -= 6
        buf = BytesIO()
        img.save(buf, format="PNG", optimize=True)
        data = buf.getvalue()
        if len(data) > max_kb * 1024:
            rgb = img.convert("RGB")
            q = 82
            best = None
            while q >= 50:
                b2 = BytesIO()
                rgb.save(b2, format="JPEG", quality=q, optimize=True)
                best = b2.getvalue()
                if len(best) <= max_kb * 1024:
                    break
                q -= 6
            jpg = src.with_suffix(".jpg")
            jpg.write_bytes(best)
            print(f"converted {src.name} -> {jpg.name} {len(best)//1024}KB {rgb.size}")
            if jpg != src and src.exists() and src.suffix.lower() == ".png":
                # keep png too but overwrite png with resized PNG if small enough else leave jpg sibling
                buf = BytesIO()
                img_small = img.copy()
                img_small.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
                img_small.convert("RGB").save(src, format="PNG", optimize=True)
                if src.stat().st_size > max_kb * 1024:
                    # replace png with jpeg-in-png? Better: save JPEG bytes as .png is wrong.
                    # Overwrite PNG using Pillow PNG quantization
                    quantized = img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=192)
                    quantized.save(src, format="PNG", optimize=True)
            print(f"png {src.name} {src.stat().st_size // 1024}KB")
        else:
            src.write_bytes(data)
            print(f"png {src.name} {src.stat().st_size // 1024}KB {img.size}")


def normalize_svg(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="ignore")
    if "<svg" not in text.lower():
        raise ValueError("not svg")
    text = re.sub(r'\swidth="[^"]*"', "", text, count=1)
    text = re.sub(r'\sheight="[^"]*"', "", text, count=1)
    if "fill=" not in text[:200] and "currentColor" not in text:
        text = text.replace("<svg", '<svg fill="currentColor"', 1)
    elif 'fill="currentColor"' not in text:
        # simple-icons already use fill="#000000" or similar on path
        text = re.sub(r'fill="#[0-9A-Fa-f]{3,8}"', 'fill="currentColor"', text)
        if 'fill="currentColor"' not in text:
            text = text.replace("<svg", '<svg fill="currentColor"', 1)
    return text


def download_ai_labs() -> None:
    dest = ROOT / "images" / "ai-labs"
    dest.mkdir(parents=True, exist_ok=True)
    labs = [
        ("openai", ["openai"], "OpenAI", "https://openai.com"),
        ("anthropic", ["anthropic"], "Anthropic", "https://www.anthropic.com"),
        ("google-deepmind", ["googlegemini", "google", "deepmind"], "Google DeepMind / Gemini", "https://deepmind.google"),
        ("meta", ["meta", "metaai"], "Meta", "https://ai.meta.com"),
        ("microsoft", ["microsoftazure", "windows", "microsoft"], "Microsoft", "https://www.microsoft.com"),
        ("nvidia", ["nvidia"], "NVIDIA", "https://www.nvidia.com"),
        ("xai", ["xai"], "xAI", "https://x.ai"),
        ("mistral", ["mistralai", "mistral"], "Mistral", "https://mistral.ai"),
        ("cohere", ["cohere"], "Cohere", "https://cohere.com"),
        ("hugging-face", ["huggingface"], "Hugging Face", "https://huggingface.co"),
        ("perplexity", ["perplexity"], "Perplexity", "https://www.perplexity.ai"),
        ("deepseek", ["deepseek"], "DeepSeek", "https://www.deepseek.com"),
        ("elevenlabs", ["elevenlabs"], "ElevenLabs", "https://elevenlabs.io"),
        ("stability-ai", ["stabilityai", "stability"], "Stability AI", "https://stability.ai"),
        ("amazon-aws", ["amazonwebservices", "amazonaws", "amazon"], "Amazon AWS", "https://aws.amazon.com"),
    ]
    # Custom Microsoft four-square if CDN lacks it
    microsoft_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" role="img"><title>Microsoft</title><path d="M1 1h10v10H1V1zm12 0h10v10H13V1zM1 13h10v10H1V13zm12 0h10v10H13V13z"/></svg>'''
    manifest = []
    for fname, slugs, name, url in labs:
        got = None
        source = None
        for slug in slugs:
            cdn = f"https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{slug}.svg"
            try:
                data = fetch(cdn)
                if looks_like_image(data) or b"<svg" in data[:200]:
                    text = normalize_svg(data)
                    got = text
                    source = f"simple-icons:{slug}"
                    break
            except Exception as e:
                print(f"fail {slug}: {e}")
        if fname == "microsoft" and (got is None or "azure" in (source or "")):
            got = microsoft_svg
            source = "custom-four-square"
        if got is None:
            print(f"MISSING {fname}")
            continue
        out = dest / f"{fname}.svg"
        out.write_text(got, encoding="utf-8")
        print(f"lab {fname} <- {source} {out.stat().st_size}B")
        manifest.append({"name": name, "file": f"{fname}.svg", "url": url, "source": source})
    (dest / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("wrote manifest", len(manifest))


def download_nsait() -> None:
    base = "https://portfolio.nsait.co.ke"
    html = fetch(base + "/").decode("utf-8", errors="ignore")
    js = ""
    try:
        js = fetch(base + "/assets/js/scripts.js").decode("utf-8", errors="ignore")
    except Exception as e:
        print("scripts.js", e)
    blob = html + "\n" + js
    urls = set(re.findall(r'(?:src|href|data-src|data-img)=["\']([^"\']+\.(?:png|jpg|jpeg|webp|svg|gif))', blob, re.I))
    urls |= set(re.findall(r'["\'](/?assets/[^"\']+\.(?:png|jpg|jpeg|webp|svg|gif|md|json))', blob, re.I))
    urls |= set(re.findall(r'url\(([^)]+\.(?:png|jpg|jpeg|webp))\)', blob, re.I))
    extra_guess = [
        "/assets/imgs/intro/02.png",
        "/assets/imgs/intro/01.png",
        "/assets/imgs/intro/03.png",
        "/assets/css/plugins.css",
    ]
    for g in extra_guess:
        urls.add(g)
    print("candidate urls", len(urls))
    for u in sorted(urls):
        print(" ", u)

    # Try to find detail markdown
    md_urls = set(re.findall(r'["\']([^"\']+\.md)["\']', blob, re.I))
    json_urls = set(re.findall(r'["\']([^"\']+projects?[^"\']+\.json)["\']', blob, re.I))
    print("md", md_urls, "json", json_urls)

    slugs = [
        "ai-in-mind-the-gap", "chama-collection-system", "e-fns-immigration", "escrow-platform",
        "intelligent-meetings", "kiva-insurance-voice-agent", "kra-tools", "meridian",
        "ministry-of-lands", "monetrax", "nunge-returns", "ongea-pesa", "smart-events",
        "smart-school-sentinel", "statussync", "swara", "tender-master-kenya",
    ]
    path_guesses = []
    for slug in slugs:
        for folder in ("assets/imgs/works", "assets/imgs/projects", "assets/imgs/portfolio", "assets/imgs/intro", "projects", "assets/data"):
            for ext in (".jpg", ".png", ".webp", ".md", ".json"):
                path_guesses.append(f"/{folder}/{slug}{ext}")
        path_guesses.append(f"/assets/imgs/works/{slug}.jpg")
        path_guesses.append(f"/project-details/{slug}.html")
        path_guesses.append(f"/assets/data/{slug}.md")

    # Parse work items from HTML
    titles = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.I | re.S)

    dest_root = ROOT / "images" / "nsait"
    dest_root.mkdir(parents=True, exist_ok=True)
    (dest_root / "_shared").mkdir(exist_ok=True)

    def abs_url(u: str) -> str:
        u = u.strip().strip("'\"")
        if u.startswith("http"):
            return u
        if u.startswith("//"):
            return "https:" + u
        if not u.startswith("/"):
            u = "/" + u
        return base + u

    downloaded = []
    seen = set()
    for u in list(urls) + path_guesses:
        if any(x in u.lower() for x in ("favicon", "font", ".css", ".js")):
            continue
        full = abs_url(u)
        if full in seen:
            continue
        seen.add(full)
        try:
            data = fetch(full, timeout=20)
        except Exception:
            continue
        if not looks_like_image(data) and not (full.endswith(".md") or full.endswith(".json") or full.endswith(".html")):
            continue
        if len(data) < 800:
            continue
        name = Path(u.split("?")[0]).name or "file.bin"
        # slug from filename
        slug = "shared"
        low = (u + name).lower()
        for s in slugs:
            if s.replace("-", "") in low.replace("-", "").replace("_", ""):
                slug = s
                break
            key = s.split("-")[0]
            if key in low and slug == "shared":
                slug = s
        folder = dest_root / ("_shared" if slug == "shared" else slug)
        folder.mkdir(exist_ok=True)
        out = folder / name
        if out.exists() and out.stat().st_size == len(data):
            continue
        save_bytes(out, data)
        downloaded.append(str(out.relative_to(ROOT)))
        print(f"nsait {out.relative_to(ROOT)} {len(data)//1024}KB")

    # brand logos already in images/brands — copy into nsait/_shared
    brands = ROOT / "images" / "brands"
    if brands.exists():
        for f in brands.iterdir():
            if f.is_file():
                target = dest_root / "_shared" / f.name
                if not target.exists():
                    target.write_bytes(f.read_bytes())

    print("nsait downloaded", len(downloaded))
    (dest_root / "MANIFEST.txt").write_text("\n".join(downloaded) or "(none from live site)\n", encoding="utf-8")


def render_signature_name() -> None:
    fonts_dir = Path(os.environ.get("TEMP", "/tmp")) / "sig-fonts"
    fonts_dir.mkdir(exist_ok=True)
    # Allura then Great Vibes
    urls = {
        "Allura-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/allura/Allura-Regular.ttf",
        "GreatVibes-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/greatvibes/GreatVibes-Regular.ttf",
    }
    font_path = None
    for name, url in urls.items():
        p = fonts_dir / name
        if not p.exists():
            try:
                save_bytes(p, fetch(url))
                print("font", name, p.stat().st_size)
            except Exception as e:
                print("font fail", name, e)
                continue
        if p.exists() and p.stat().st_size > 10000:
            font_path = p
            if name.startswith("Allura"):
                break
    if font_path is None:
        font_path = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "seguiemj.ttf"
    text = "James Imodoi Epale"
    font = ImageFont.truetype(str(font_path), 128)
    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((20 - bbox[0], 16 - bbox[1]), text, font=font, fill=(6, 36, 92, 255))
    # trim
    bbox2 = img.getbbox()
    img = img.crop(bbox2)
    out = ROOT / "signature" / "assets" / "signature-name.png"
    img.save(out, "PNG")
    print("name png", out, img.size, out.stat().st_size)


def compress_projects() -> None:
    folder = ROOT / "images" / "projects"
    for f in folder.glob("*"):
        if f.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        try:
            compress_image(f, max_px=1200, max_kb=250)
        except Exception as e:
            print("compress fail", f, e)
    for extra in [
        ROOT / "images" / "hero-globe.png",
        ROOT / "images" / "og-image.png",
        ROOT / "signature" / "assets" / "globe-panel.png",
    ]:
        if extra.exists() and extra.stat().st_size > 350 * 1024:
            try:
                compress_image(extra, max_px=1600, max_kb=380)
            except Exception as e:
                print("compress fail", extra, e)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("all", "labs"):
        download_ai_labs()
    if cmd in ("all", "nsait"):
        download_nsait()
    if cmd in ("all", "name"):
        render_signature_name()
    if cmd in ("all", "compress"):
        compress_projects()


if __name__ == "__main__":
    main()
