#!/usr/bin/env python3
"""Generate GitHub-safe SVG ASCII portrait cards from assets/portrait.png."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets' / 'portrait.png'
OUT = ROOT / 'assets'
CHARS = '@%#*+=-:. '
COLS, ROWS = 43, 39


def ascii_portrait():
    im = Image.open(SOURCE).convert('RGB')
    # Crop to upper portrait: hair, face, collar; reduce empty background.
    w, h = im.size
    im = im.crop((int(w*.17), int(h*.10), int(w*.85), int(h*.82)))
    im = ImageOps.fit(im, (COLS, ROWS), method=Image.Resampling.LANCZOS)
    im = ImageOps.grayscale(im)
    im = ImageEnhance.Contrast(im).enhance(1.65)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=130))
    pixels = list(im.getdata())
    lines = []
    for y in range(ROWS):
        line = ''.join(CHARS[min(len(CHARS)-1, p*(len(CHARS)-1)//256)] for p in pixels[y*COLS:(y+1)*COLS])
        lines.append(line.rstrip())
    return lines


def render(dark, lines):
    bg = '#0d1117' if dark else '#f6f8fa'
    panel = '#161b22' if dark else '#ffffff'
    border = '#30363d' if dark else '#d0d7de'
    primary = '#e6edf3' if dark else '#1f2328'
    muted = '#8b949e' if dark else '#59636e'
    accent = '#5DCAA5' if dark else '#096b50'
    art = '#80d6b7' if dark else '#176e56'
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600" role="img" aria-label="ASCII portrait of Farhan and developer profile">
<rect width="1000" height="600" rx="18" fill="{bg}"/>
<rect x="14" y="14" width="972" height="572" rx="14" fill="{panel}" stroke="{border}"/>
<circle cx="43" cy="42" r="7" fill="#ff5f57"/><circle cx="66" cy="42" r="7" fill="#febc2e"/><circle cx="89" cy="42" r="7" fill="#28c840"/>
<text x="125" y="47" fill="{muted}" font-family="monospace" font-size="15">farhan@github: ~/profile</text>
<line x1="28" y1="65" x2="972" y2="65" stroke="{border}"/>
<text x="42" y="96" fill="{accent}" font-family="monospace" font-size="16">$ ./introduce --ascii</text>
<line x1="525" y1="115" x2="525" y2="532" stroke="{border}"/>
''']
    # Use individual lines rather than SVG foreignObject for GitHub compatibility.
    for i, line in enumerate(lines):
        svg.append(f'<text x="42" y="{128+i*10.4:.1f}" fill="{art}" font-family="monospace" font-size="11.2" xml:space="preserve">{escape(line)}</text>')
    content = [
        (140,'MUHAMMAD FARHAN',24,primary,'bold'),
        (170,'FATHURROHMAN',24,primary,'bold'),
        (207,'Software Engineer  /  Android Engineer',15,accent,'normal'),
        (257,'LOCATION',13,muted,'bold'),
        (281,'Jakarta, Indonesia',17,primary,'normal'),
        (324,'SPECIALIZATION',13,muted,'bold'),
        (348,'Kotlin  /  Jetpack Compose  /  Android',15,primary,'normal'),
        (391,'ALSO BUILDING',13,muted,'bold'),
        (415,'Backend  /  Developer Tools  /  AI',15,primary,'normal'),
        (457,'BACKGROUND',13,muted,'bold'),
        (481,'B.Sc. Informatics  /  Bangkit 2024',15,primary,'normal'),
    ]
    for y, txt, size, color, weight in content:
        svg.append(f'<text x="554" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" font-weight="{weight}">{escape(txt)}</text>')
    svg.append(f'<line x1="28" y1="545" x2="972" y2="545" stroke="{border}"/>')
    svg.append(f'<text x="42" y="568" fill="{muted}" font-family="monospace" font-size="14">KOTLIN  •  COMPOSE  •  FIREBASE  •  GO  •  TYPESCRIPT  •  DOCKER</text>')
    svg.append('</svg>')
    return '\n'.join(svg)+'\n'

if __name__ == '__main__':
    lines = ascii_portrait()
    for filename, dark in [('dark_mode.svg', True), ('light_mode.svg', False)]:
        (OUT / filename).write_text(render(dark, lines), encoding='utf-8')
        print('Generated', OUT / filename)
