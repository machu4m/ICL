"""Builds icl-s2-logo-launch.svg: native SVG ground + inline logo paths + outlined text.

Text layers are glyph outlines, so the SVG needs no fonts:
  node export-text-layers.js num.pdf rest.pdf
  pdftocairo -svg num.pdf num.svg && pdftocairo -svg rest.pdf rest.svg
  python3 build_svg.py num.svg rest.svg
"""
import re, sys

RED, BLUE, NAVY, WHITE = '#E92D3C', '#1234F9', '#061433', '#FFFFFF'

def inner(svg, prefix):
    """Body of a pdftocairo SVG with ids made unique."""
    body = re.sub(r'^.*?<svg[^>]*>', '', svg, flags=re.S).rsplit('</svg>', 1)[0]
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}{m.group(1)}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{prefix}{m.group(1)})', body)
    body = re.sub(r'xlink:href="#([^"]+)"', lambda m: f'xlink:href="#{prefix}{m.group(1)}"', body)
    return body

def logo(colour, prefix, dx):
    s = open('assets/icl-s2-logo-white.svg').read()
    body = re.sub(r'^.*?<svg[^>]*>', '', s, flags=re.S).rsplit('</svg>', 1)[0]
    body = body.replace('#FFFFFF', colour)
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}{m.group(1)}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{prefix}{m.group(1)})', body)
    op = '' if colour == WHITE else ' opacity=".9"'
    return f'<svg x="{220+dx}" y="268" width="640" height="538" viewBox="140 300 690 580"{op}>{body}</svg>'

num, rest = (open(p).read() for p in sys.argv[1:3])
pt = 'transform="scale(1.3333333)"'  # pdftocairo output is in pt (0.75 px)

out = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1350" viewBox="0 0 1080 1350">
<title>ICL Season 2 Official Logo Launch</title>
<defs>
  <radialGradient id="glow-blue" gradientUnits="userSpaceOnUse" cx="540" cy="520" r="620" gradientTransform="translate(540 520) scale(1 0.8387) translate(-540 -520)">
    <stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset=".7" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow-red" gradientUnits="userSpaceOnUse" cx="540" cy="1420" r="900" gradientTransform="translate(540 1420) scale(1 0.4) translate(-540 -1420)">
    <stop offset="0" stop-color="{RED}" stop-opacity=".38"/><stop offset=".7" stop-color="{RED}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="scan" width="1080" height="6" patternUnits="userSpaceOnUse">
    <rect y="4" width="1080" height="2" fill="{NAVY}" fill-opacity=".38"/>
  </pattern>
</defs>
<g id="ground">
  <rect width="1080" height="1350" fill="{NAVY}"/>
  <rect width="1080" height="1350" fill="url(#glow-blue)"/>
  <rect width="1080" height="1350" fill="url(#glow-red)"/>
</g>
<g id="numeral" {pt}>{inner(num, 'n-')}</g>
<g id="beams" fill="{WHITE}" opacity=".07">
  <polygon points="540,540 -200,120 -200,300"/><polygon points="540,540 1280,120 1280,300"/>
  <polygon points="540,540 -200,760 -200,900"/><polygon points="540,540 1280,760 1280,900"/>
</g>
<rect id="scanlines" width="1080" height="1350" fill="url(#scan)"/>
<g id="logo">
  {logo(RED, 'lr-', -7)}
  {logo(BLUE, 'lb-', 7)}
  {logo(WHITE, 'lw-', 0)}
</g>
<g id="type" {pt}>{inner(rest, 't-')}</g>
</svg>
'''
open('icl-s2-logo-launch.svg', 'w').write(out)
print('wrote icl-s2-logo-launch.svg', len(out))
