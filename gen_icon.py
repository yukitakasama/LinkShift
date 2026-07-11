"""生成应用图标 app_icon.ico（多尺寸，蓝底 + 双卡片 + 迁移箭头）。"""

import math
import os

from PIL import Image, ImageDraw


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def v_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGBA", size)
    r1, g1, b1 = top
    r2, g2, b2 = bottom
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        for x in range(w):
            px[x, y] = (r, g, b, 255)
    return img


def draw_arrow(draw, cx, cy, scale, color):
    # 一个从左侧卡片指向右侧卡片的箭头
    x1 = cx - 0.42 * scale
    x2 = cx + 0.42 * scale
    y = cy
    lw = max(2, int(0.07 * scale))
    draw.line([(x1, y), (x2 - lw, y)], fill=color, width=lw)
    # 箭头头部（三角形）
    ah = 0.16 * scale
    draw.polygon(
        [(x2, y), (x2 - ah, y - ah * 0.7), (x2 - ah, y + ah * 0.7)],
        fill=color,
    )


def make_icon(size):
    s = size
    img = v_gradient((s, s), (90, 175, 245), (38, 130, 225))
    d = ImageDraw.Draw(img)
    pad = s * 0.16
    card = s * 0.40
    radius = s * 0.10
    # 左侧卡片（稍上）
    lx0, ly0 = pad, pad + s * 0.02
    lx1, ly1 = lx0 + card, ly0 + card
    # 右侧卡片（稍下）
    rx0, ry0 = s - pad - card, s - pad - card * 0.98 - s * 0.02
    rx1, ry1 = rx0 + card, ry0 + card
    white = (255, 255, 255, 235)
    rounded_rect(d, [lx0, ly0, lx1, ly1], radius, white)
    rounded_rect(d, [rx0, ry0, rx1, ry1], radius, white)
    # 卡片内简单横线纹理
    line_c = (120, 170, 220, 255)
    for i, (x0, y0, x1_, y1_) in enumerate(
        [(lx0, ly0, lx1, ly1), (rx0, ry0, rx1, ry1)]
    ):
        for k in range(1, 3):
            yy = y0 + (y1_ - y0) * (k / 3.2)
            d.line([(x0 + s * 0.06, yy), (x1_ - s * 0.06, yy)], fill=line_c, width=max(1, int(s * 0.018)))
    # 迁移箭头（沿两卡片中心连线）
    arrow_col = (255, 255, 255, 255)
    cxs = (lx0 + lx1) / 2
    cys = (ly0 + ly1) / 2
    cxe = (rx0 + rx1) / 2
    cye = (ry0 + ry1) / 2
    lw = max(2, int(s * 0.045))
    d.line([(cxs, cys), (cxe, cye)], fill=arrow_col, width=lw)
    # 箭头头部
    ang = math.atan2(cye - cys, cxe - cxs)
    ah = s * 0.11
    a1 = (cxe, cye)
    a2 = (cxe - ah * math.cos(ang - 0.5), cye - ah * math.sin(ang - 0.5))
    a3 = (cxe - ah * math.cos(ang + 0.5), cye - ah * math.sin(ang + 0.5))
    d.polygon([a1, a2, a3], fill=arrow_col)
    return img


def main():
    import io
    import struct

    sizes = [256, 128, 64, 48, 32, 24, 16]
    imgs = [make_icon(s).convert("RGBA") for s in sizes]

    def png_bytes(im):
        b = io.BytesIO()
        im.save(b, format="PNG")
        return b.getvalue()

    pngs = [png_bytes(im) for im in imgs]
    icondir = struct.pack("<HHH", 0, 1, len(pngs))
    entries = b""
    data = b""
    offset = 6 + 16 * len(pngs)
    for im, png in zip(imgs, pngs):
        w, h = im.size
        bw = 0 if w >= 256 else w
        bh = 0 if h >= 256 else h
        entries += struct.pack("<BBBBHHII", bw, bh, 0, 0, 1, 32, len(png), offset)
        data += png
        offset += len(png)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")
    with open(out, "wb") as f:
        f.write(icondir + entries + data)
    print("saved", out, "frames:", len(pngs))


if __name__ == "__main__":
    main()
