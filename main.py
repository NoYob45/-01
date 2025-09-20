import sys, cv2, numpy as np
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QListWidget, QLabel, QStatusBar, QAction,
                             QFileDialog, QMessageBox, QScrollArea)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont, QColor
from PyQt5.QtCore import Qt
from seg1 import process

DATA_DIR   = Path('data')
RESULT_DIR = Path('result')
RESULT_DIR.mkdir(exist_ok=True)

def cv2qt(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    return QPixmap.fromImage(QImage(rgb.data, w, h, w * ch, QImage.Format_RGB888))

class ImageLabel(QLabel):
    """原尺寸 + 顶部文字"""
    def __init__(self, title=''):
        super().__init__()
        self.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setStyleSheet("border:1px solid gray;")
        self._title = title
        self._pix   = QPixmap()

    def set_cv_image(self, bgr, fname=''):
        self._pix   = cv2qt(bgr)
        self._title = fname
        h_img = self._pix.height()
        w_img = self._pix.width()
        h_total = h_img + 30
        canvas = QPixmap(w_img, h_total)
        canvas.fill(QColor(240, 240, 240))
        painter = QPainter(canvas)
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont('Microsoft YaHei', 10))
        painter.drawText(0, 0, w_img, 30, Qt.AlignCenter, self._title)
        painter.drawPixmap(0, 30, self._pix)
        painter.end()
        self.setPixmap(canvas)
        # 关键：让 QLabel 大小 = 图像大小（不缩小）
        self.resize(canvas.size())

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('燕窝杂质分割  ‹‹‹  横纵滚动条版')
        self.resize(1400, 800)
        self.build_ui()
        self.build_menu()
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.current_bgr = None
        self.populate_list()

    # ---------------- UI ----------------
    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_split = QHBoxLayout(central)

        # 左侧列表
        self.list_w = QListWidget()
        self.list_w.setFixedWidth(200)
        self.list_w.itemDoubleClicked.connect(self.open_item)
        main_split.addWidget(self.list_w)

        # 右侧三图横向
        self.hbox_pics = QHBoxLayout()
        self.lbls = []
        titles = ['原图', '分割图', '轮廓叠加']
        for t in titles:
            scroll = QScrollArea()
            # 关键：横纵滚动条始终显示
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setWidgetResizable(False)
            lbl = ImageLabel(t)
            scroll.setWidget(lbl)
            self.lbls.append(lbl)
            self.hbox_pics.addWidget(scroll, stretch=1)
        main_split.addLayout(self.hbox_pics, stretch=3)

    # ---------------- 菜单 ----------------
    def build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        open_dir = QAction('打开目录', self)
        open_dir.triggered.connect(self.choose_dir)
        file_menu.addAction(open_dir)

        proc_menu = menubar.addMenu('处理')
        batch_act = QAction('批量处理当前目录', self)
        batch_act.triggered.connect(self.batch_process)
        proc_menu.addAction(batch_act)

    # ---------------- 功能 ----------------
    def populate_list(self):
        self.list_w.clear()
        for p in DATA_DIR.glob('*.bmp'):
            self.list_w.addItem(p.name)

    def choose_dir(self):
        global DATA_DIR
        dir_path = QFileDialog.getExistingDirectory(self, "选择 BMP 目录", str(DATA_DIR))
        if dir_path:
            DATA_DIR = Path(dir_path)
            self.populate_list()

    def open_item(self, item):
        fname = DATA_DIR / item.text()
        bgr = cv2.imread(str(fname))
        if bgr is None:
            QMessageBox.critical(self, '错误', '无法读取图片')
            return
        self.current_bgr = bgr
        gray, seg, clean, overlay, cnt = process(bgr)
        # 原尺寸显示
        self.lbls[0].set_cv_image(gray, f'原图   ({fname.name})')
        self.lbls[1].set_cv_image(cv2.cvtColor(seg, cv2.COLOR_GRAY2BGR), f'分割图 ({fname.name})')
        self.lbls[2].set_cv_image(overlay, f'叠加   ({fname.name})')
        self.status.showMessage(f'当前：{fname.name}   检出杂质：{cnt} 个')

    def batch_process(self):
        if not DATA_DIR.exists():
            QMessageBox.warning(self, '提示', '请先设置正确目录')
            return
        for p in DATA_DIR.glob('*.bmp'):
            bgr = cv2.imread(str(p))
            if bgr is None: continue
            _, _, _, overlay, _ = process(bgr)
            out = RESULT_DIR / f'{p.stem}_overlay.png'
            cv2.imwrite(str(out), overlay)
        QMessageBox.information(self, '完成', f'批量处理完毕，结果保存在 {RESULT_DIR}')

# ---------------- 启动 ----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
# ---------------- 启动 ----------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
