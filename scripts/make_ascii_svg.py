#!/usr/bin/env python3
"""
Convert prepped grayscale image to a self-typing ASCII SVG.
Each row wipes left-to-right with a small cursor block, staggered top-to-bottom.
Animation plays once and freezes (SMIL inside SVG).
"""
import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
COLS = 100
ROWS = 53
FONT_SIZE = 10
LINE_HEIGHT = 12
CHAR_WIDTH = 6.6  # approximate for monospace at 10px
WIDTH = COLS * CHAR_WIDTH
HEIGHT = ROWS * LINE_HEIGHT
FILL_COLOR = "#8b949e"  # GitHub light gray

def image_to_ascii(img_path: str) -> list[str]:
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read {img_path}")
    
    # Resize to character grid
    img = cv2.resize(img, (COLS, ROWS), interpolation=cv2.INTER_AREA)
    
    # Normalize to 0-1
    img = img.astype(float) / 255.0
    
    # Map to ramp (invert: bright -> sparse, dark -> dense)
    ascii_rows = []
    for row in img:
        line = "".join(RAMP[min(int(p * (len(RAMP) - 1)), len(RAMP) - 1)] for p in row)
        ascii_rows.append(line)
    return ascii_rows

def generate_svg(ascii_rows: list[str], output_path: str = "arghyajit18-ascii.svg"):
    # Calculate timing
    row_delay = 0.03  # seconds between row starts
    char_duration = 0.008  # seconds per character wipe
    total_duration = ROWS * row_delay + COLS * char_duration + 1
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        f'<style><![CDATA[',
        f'  .char {{ font: {FONT_SIZE}px monospace; fill: {FILL_COLOR}; }}',
        f'  .cursor {{ fill: {FILL_COLOR}; }}',
        f']]></style>',
        f'<rect width="100%" height="100%" fill="white"/>',
    ]
    
    for row_idx, line in enumerate(ascii_rows):
        y = row_idx * LINE_HEIGHT + FONT_SIZE
        row_start = row_idx * row_delay
        
        for col_idx, ch in enumerate(line):
            if ch == " ":
                continue
            x = col_idx * CHAR_WIDTH
            char_start = row_start + col_idx * char_duration
            char_end = char_start + char_duration
            
            # Clip path for horizontal wipe
            clip_id = f"clip-r{row_idx}c{col_idx}"
            svg_parts.append(f'<clipPath id="{clip_id}">')
            svg_parts.append(f'  <rect x="{x}" y="{y - FONT_SIZE}" width="{CHAR_WIDTH}" height="{LINE_HEIGHT}">')
            svg_parts.append(f'    <animate attributeName="width" from="0" to="{CHAR_WIDTH}" ')
            svg_parts.append(f'      begin="{char_start:.3f}s" dur="{char_duration:.3f}s" fill="freeze"/>')
            svg_parts.append(f'  </rect>')
            svg_parts.append(f'</clipPath>')
            
            # Character with clip
            svg_parts.append(f'<text x="{x}" y="{y}" class="char" clip-path="url(#{clip_id})">{ch}</text>')
        
        # Cursor block at end of row
        cursor_x = COLS * CHAR_WIDTH
        cursor_start = row_start + COLS * char_duration
        svg_parts.append(f'<rect x="{cursor_x}" y="{y - FONT_SIZE}" width="{CHAR_WIDTH}" height="{LINE_HEIGHT}" class="cursor">')
        svg_parts.append(f'  <animate attributeName="opacity" from="1" to="0" begin="{cursor_start:.3f}s" dur="0.1s" fill="freeze"/>')
        svg_parts.append(f'</rect>')
    
    svg_parts.append('</svg>')
    
    with open(output_path, "w") as f:
        f.write("\n".join(svg_parts))
    print(f"Saved ASCII SVG to {output_path}")

if __name__ == "__main__":
    ascii_rows = image_to_ascii("source-prepped.png")
    generate_svg(ascii_rows)