#!/usr/bin/env python3
"""
Render contribution heatmap as SVG with diagonal slide-down animation.
Reads data/contributions.json, outputs contrib-heatmap.svg.
"""
import json
from datetime import date, timedelta

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL_SIZE = 13
CELL_GAP = 3
WEEKS = 53
DAYS = 7
WIDTH = WEEKS * (CELL_SIZE + CELL_GAP) + 50
HEIGHT = DAYS * (CELL_SIZE + CELL_GAP) + 80
LEGEND_Y = HEIGHT - 30
STATS_Y = HEIGHT - 10

def level_to_color(level: int) -> str:
    return PALETTE[min(level, len(PALETTE) - 1)]

def generate_svg():
    with open("data/contributions.json") as f:
        data = json.load(f)
    
    days = data["days"]
    stats = data["stats"]
    
    # Build a lookup: date -> level
    day_map = {d["date"]: d["level"] for d in days}
    
    # Determine date range (last 53 weeks)
    today = date.today()
    start_date = today - timedelta(weeks=WEEKS)
    
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        f'<style><![CDATA[',
        f'  .cell {{ rx: 2; ry: 2; }}',
        f'  .label {{ font: 11px system-ui; fill: #8b949e; }}',
        f'  .legend-text {{ font: 11px system-ui; fill: #8b949e; }}',
        f'  .stats-text {{ font: 12px system-ui; fill: #e6edf3; }}',
        f']]></style>',
        f'<rect width="100%" height="100%" fill="white"/>',
    ]
    
    # Day labels (Mon, Wed, Fri)
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, label in enumerate(day_labels):
        y = 40 + i * (CELL_SIZE + CELL_GAP) + CELL_SIZE
        svg_parts.append(f'<text x="30" y="{y}" class="label" text-anchor="end" dominant-baseline="middle">{label[:3]}</text>')
    
    # Month labels
    month_positions = {}
    current = start_date
    for week in range(WEEKS):
        week_start = current + timedelta(weeks=week)
        if week_start.day <= 7:
            month_name = week_start.strftime("%b")
            x = 50 + week * (CELL_SIZE + CELL_GAP)
            if month_name not in month_positions:
                month_positions[month_name] = x
    
    for month, x in month_positions.items():
        svg_parts.append(f'<text x="{x}" y="25" class="label" text-anchor="middle">{month}</text>')
    
    # Cells with diagonal animation
    for week in range(WEEKS):
        for day in range(DAYS):
            cell_date = start_date + timedelta(weeks=week, days=day)
            date_str = cell_date.isoformat()
            level = day_map.get(date_str, 0)
            color = level_to_color(level)
            
            x = 50 + week * (CELL_SIZE + CELL_GAP)
            y = 40 + day * (CELL_SIZE + CELL_GAP)
            
            # Diagonal delay: week * 0.02 + day * 0.01
            delay = (week + day) * 0.015
            
            svg_parts.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" class="cell" fill="{color}">')
            svg_parts.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.3s" fill="freeze"/>')
            svg_parts.append(f'  <animate attributeName="transform" from="translate(0,-10)" to="translate(0,0)" begin="{delay:.3f}s" dur="0.3s" fill="freeze" type="translate"/>')
            svg_parts.append(f'  <title>{date_str}: {days[0]["count"] if days else 0} contributions</title>')
            svg_parts.append(f'</rect>')
    
    # Legend
    svg_parts.append(f'<text x="50" y="{LEGEND_Y}" class="legend-text">Less</text>')
    for i, color in enumerate(PALETTE):
        x = 100 + i * 24
        svg_parts.append(f'<rect x="{x}" y="{LEGEND_Y - 10}" width="10" height="10" rx="2" fill="{color}"/>')
    svg_parts.append(f'<text x="{100 + len(PALETTE) * 24 + 10}" y="{LEGEND_Y}" class="legend-text">More</text>')
    
    # Stats footer
    total = stats["total_last_year"]
    streak = stats["current_streak"]
    longest = stats["longest_streak"]
    svg_parts.append(f'<text x="{WIDTH - 50}" y="{STATS_Y}" class="stats-text" text-anchor="end">{total:,} contributions in the last year • {streak} day streak • longest: {longest} days</text>')
    
    svg_parts.append('</svg>')
    
    with open("contrib-heatmap.svg", "w") as f:
        f.write("\n".join(svg_parts))
    print("Saved contribution heatmap to contrib-heatmap.svg")

if __name__ == "__main__":
    generate_svg()