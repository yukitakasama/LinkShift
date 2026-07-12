"""实时速度曲线：用 QPainter 自绘，兼容 PySide6 / PyQt5（无需 QtCharts）。"""

from .qt_compat import QWidget, QPainter, QPen, QColor, Qt


class SpeedChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._samples = []          # (t, mbps)
        self._max_points = 600
        self._line_color = QColor("#2d8cf0")
        self._grid_color = QColor("#e0e0e0")
        self._text_color = QColor("#666666")
        self.setMinimumHeight(220)

    def clear(self):
        self._samples = []
        self.update()

    def set_samples(self, samples):
        self._samples = list(samples)[-self._max_points:]
        self.update()

    def add_sample(self, t, mbps):
        self._samples.append((t, mbps))
        if len(self._samples) > self._max_points:
            self._samples = self._samples[-self._max_points:]
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()
        pad_l, pad_r, pad_t, pad_b = 38, 10, 10, 22
        plot_w = max(1, w - pad_l - pad_r)
        plot_h = max(1, h - pad_t - pad_b)

        p.fillRect(self.rect(), QColor("#ffffff"))

        if not self._samples:
            p.setPen(self._text_color)
            p.drawText(pad_l, pad_t + plot_h // 2, "等待数据…")
            return

        max_t = max(t for t, _ in self._samples)
        max_v = max(v for _, v in self._samples)
        max_t = max(max_t, 10.0)
        max_v = max(max_v, 10.0) * 1.2

        # 网格 + Y 轴刻度
        p.setPen(self._grid_color)
        for i in range(5):
            y = pad_t + plot_h * i / 4
            p.drawLine(pad_l, y, pad_l + plot_w, y)
            val = max_v * (1 - i / 4)
            p.setPen(self._text_color)
            p.drawText(2, int(y) + 4, f"{val:.1f}")
            p.setPen(self._grid_color)

        # X 轴刻度（时间）
        p.setPen(self._text_color)
        p.drawText(pad_l, h - 6, "0s")
        p.drawText(pad_l + plot_w - 24, h - 6, f"{max_t:.0f}s")

        # 折线
        pen = QPen(self._line_color)
        pen.setWidth(2)
        p.setPen(pen)
        pts = []
        for t, v in self._samples:
            x = pad_l + plot_w * (t / max_t) if max_t > 0 else pad_l
            yv = pad_t + plot_h * (1 - v / max_v) if max_v > 0 else pad_t
            pts.append((x, yv))
        for i in range(1, len(pts)):
            p.drawLine(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1])

        # 当前速度标注
        cur_t, cur_v = self._samples[-1]
        p.setPen(self._line_color)
        p.drawText(pad_l + 4, pad_t + 14, f"{cur_v:.2f} MB/s")
