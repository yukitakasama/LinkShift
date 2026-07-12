"""迁移进度对话框：进度条 + 实时速度曲线 + 日志 + 取消按钮。"""

import time

from PySide6.QtCore import QThread, Signal, QObject, Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel, QTextEdit,
    QPushButton, QMessageBox,
)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtGui import QPainter, QPen, QColor


class _Worker(QThread):
    progress = Signal(int, int)          # done_bytes, total_bytes
    speed = Signal(float, float)         # bytes_per_sec, elapsed_sec
    item_start = Signal(str)
    log = Signal(str)
    finished = Signal(int, int)          # success, errors
    cancelled = Signal(int, int)         # success, errors
    error = Signal(str)
    total = Signal(int)                  # total_bytes

    def __init__(self, task):
        super().__init__()
        self.task = task
        self._cancel = False

    def request_cancel(self):
        self._cancel = True

    def run(self):
        callbacks = {
            "on_progress": lambda d, t: self.progress.emit(d, t),
            "on_speed": lambda b, e: self.speed.emit(b, e),
            "on_item_start": lambda n: self.item_start.emit(n),
            "on_log": lambda m: self.log.emit(m),
            "on_finished": lambda s, e: self.finished.emit(s, e),
            "on_cancelled": lambda s, e: self.cancelled.emit(s, e),
            "on_error": lambda m: self.error.emit(m),
            "on_total": lambda t: self.total.emit(t),
            "should_cancel": lambda: self._cancel,
        }
        self.task(callbacks)


def _fmt_size(b: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while b >= 1024 and i < len(units) - 1:
        b /= 1024
        i += 1
    return f"{b:.2f} {units[i]}"


def _fmt_speed(bps: float) -> str:
    return f"{_fmt_size(bps)}/s"


class ProgressDialog(QDialog):
    MAX_POINTS = 600

    def __init__(self, task, total_bytes=0, title="迁移进行中", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(560)
        self.setModal(True)
        self._total = total_bytes or 0
        self._has_total = total_bytes > 0

        # 状态标签
        self.lbl_current = QLabel("准备中…")
        self.lbl_overall = QLabel("总进度：计算中…")
        self.lbl_speed = QLabel("速度：—")
        self.lbl_time = QLabel("用时：0.0s")

        self.bar = QProgressBar()
        self.bar.setValue(0)
        if not self._has_total:
            self.bar.setRange(0, 0)  # 不确定模式，直到拿到真实总量

        # 速度曲线
        self.series = QLineSeries()
        self.series.setColor(QColor("#2d8cf0"))
        self.pen = QPen(self.series.color())
        self.pen.setWidth(2)
        self.series.setPen(self.pen)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("实时传输速度 (MB/s)")
        self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        self.chart.legend().hide()

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("时间 (s)")
        self.axis_x.setLabelFormat("%.0f")
        self.axis_x.setMin(0)
        self.axis_x.setMax(10)
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("MB/s")
        self.axis_y.setMin(0)
        self.axis_y.setMax(10)
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(220)

        # 日志
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(140)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.clicked.connect(self._on_cancel_clicked)
        self.btn_close = QPushButton("关闭")
        self.btn_close.setEnabled(False)
        self.btn_close.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_current)
        layout.addWidget(self.bar)
        h = QHBoxLayout()
        h.addWidget(self.lbl_overall)
        h.addWidget(self.lbl_speed)
        h.addWidget(self.lbl_time)
        layout.addLayout(h)
        layout.addWidget(self.chart_view)
        layout.addWidget(QLabel("日志："))
        layout.addWidget(self.log_edit)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

        self._start_time = 0
        self._samples = []  # (t, mbps)
        self._cancelling = False

        self.worker = _Worker(task)
        self.worker.progress.connect(self._on_progress)
        self.worker.speed.connect(self._on_speed)
        self.worker.item_start.connect(
            lambda n: self.lbl_current.setText(f"正在处理：{n}"))
        self.worker.log.connect(self._on_log)
        self.worker.finished.connect(self._on_finished)
        self.worker.cancelled.connect(self._on_cancelled)
        self.worker.error.connect(lambda m: self._on_log(f"[错误] {m}"))
        self.worker.total.connect(self._on_total)

    def start_migration(self):
        self._start_time = time.monotonic()
        self.worker.start()

    # ---- 取消 ----
    def _on_cancel_clicked(self):
        if self._cancelling:
            return
        self._cancelling = True
        self.btn_cancel.setEnabled(False)
        self.lbl_current.setText("正在取消…（请稍候，正在安全回滚）")
        self.worker.request_cancel()

    # ---- 信号处理 ----
    def _on_total(self, total):
        self._total = total or 1
        self._has_total = True
        self.bar.setRange(0, self._total)
        if self.bar.value() > self._total:
            self.bar.setValue(self._total)

    def _on_progress(self, done, total):
        if total and total > 0:
            self._total = total
        if not self._has_total:
            self.bar.setRange(0, self._total)
            self._has_total = True
        pct = int(done / (self._total or 1) * 100)
        self.bar.setValue(min(pct, 100))
        self.lbl_overall.setText(
            f"总进度：{pct}%  ({_fmt_size(done)} / {_fmt_size(self._total)})")

    def _on_speed(self, bps, elapsed):
        mbps = bps / (1024 * 1024)
        self.lbl_speed.setText(f"速度：{_fmt_speed(bps)}")
        self.lbl_time.setText(f"用时：{elapsed:.1f}s")
        t = elapsed
        self._samples.append((t, mbps))
        if len(self._samples) > self.MAX_POINTS:
            self._samples = self._samples[-self.MAX_POINTS:]
        self._redraw_chart()

    def _redraw_chart(self):
        self.series.clear()
        if not self._samples:
            return
        max_t = max(t for t, _ in self._samples)
        max_v = max(v for _, v in self._samples)
        for t, v in self._samples:
            self.series.append(t, v)
        self.axis_x.setMax(max(10, max_t * 1.1))
        self.axis_y.setMax(max(10, max_v * 1.2))

    def _on_log(self, msg):
        self.log_edit.append(msg)

    def _on_finished(self, success, errors):
        self.lbl_current.setText("迁移完成")
        if self._has_total:
            self.bar.setValue(self._total)
        self._on_log(f"—— 完成：成功 {success} 项，失败 {errors} 项 ——")
        if errors:
            QMessageBox.warning(self, "迁移结束", f"完成，但有 {errors} 项出现问题，请查看日志。")
        self.btn_cancel.setEnabled(False)
        self.btn_close.setEnabled(True)

    def _on_cancelled(self, success, errors):
        self.lbl_current.setText("已取消")
        if self._has_total:
            self.bar.setValue(min(self.bar.value(), self._total))
        self._on_log(f"—— 已取消：已完成 {success} 项，未处理 {errors} 项 ——")
        self._on_log("（已安全回滚，原始文件保持不变）")
        self.btn_cancel.setEnabled(False)
        self.btn_close.setEnabled(True)
