#!/usr/bin/env python3
"""
Generate a neofetch-style info card SVG.
Each line fades and slides in on a stagger. STATIC=1 env var emits frozen frame.
"""
import os
import sys

STATIC = os.environ.get("STATIC") == "1"

WIDTH = 490
HEIGHT = 280
PADDING = 20
LINE_HEIGHT = 28
TITLE_BAR_HEIGHT = 36
FONT_SIZE = 13
FONT_FAMILY = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"
BG_COLOR = "#161b22"
TITLE_BG = "#21262d"
TITLE_FG = "#e6edf3"
TEXT_FG = "#8b949e"
ACCENT = "#58a6ff"
KEY_COLOR = "#79c0ff"
VAL_COLOR = "#c9d1d9"
BORDER_COLOR = "#30363d"

INFO = {
    "Now": "Building developer tools @Microsoft",
    "Prev": "Open source contributor, security researcher",
    "Stack": "TypeScript, Rust, Python, Go, PostgreSQL",
    "Highlights": "12k+ stars across projects • GitHub Star • 500+ PRs merged",
}

def generate_svg(output_path: str = "info-card.svg"):
    lines = []
    y = PADDING + TITLE_BAR_HEIGHT + PADDING
    
    for i, (key, val) in enumerate(INFO.items()):
        delay = i * 0.12
        if STATIC:
            delay = 0
        
        lines.append(f'<g opacity="0">')
        lines.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>')
        lines.append(f'  <animate attributeName="transform" from="translate(20,0)" to="translate(0,0)" begin="{delay:.2f}s" dur="0.3s" fill="freeze" type="translate"/>')
        lines.append(f'  <text x="{PADDING + 10}" y="{y}" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" fill="{KEY_COLOR}">{key}</text>')
        lines.append(f'  <text x="{PADDING + 100}" y="{y}" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" fill="{VAL_COLOR}">{val}</text>')
        lines.append(f'</g>')
        y += LINE_HEIGHT
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
<style><![CDATA[
  text {{ font-family: {FONT_FAMILY}; font-size: {FONT_SIZE}px; }}
]]></style>
<rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{BG_COLOR}"/>
<rect width="{WIDTH}" height="{TITLE_BAR_HEIGHT}" rx="8" ry="0" fill="{TITLE_BG}"/>
<text x="{PADDING}" y="{PADDING + 20}" font-family="{FONT_FAMILY}" font-size="14" fill="{TITLE_FG}" font-weight="600">arghyajit18@github</text>
<text x="{WIDTH - PADDING - 80}" y="{PADDING + 20}" font-family="{FONT_FAMILY}" font-size="12" fill="{TEXT_FG}">~/profile</text>
<line x1="{PADDING}" y1="{PADDING + TITLE_BAR_HEIGHT}" x2="{WIDTH - PADDING}" y2="{PADDING + TITLE_BAR_HEIGHT}" stroke="{BORDER_COLOR}" stroke-width="1"/>
{"".join(lines)}
</svg>'''
    
    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Saved info card to {output_path}")

if __name__ == "__main__":
    generate_svg()