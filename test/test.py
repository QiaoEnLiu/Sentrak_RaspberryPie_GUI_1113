import sys
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
      QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
      QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QPixmap, QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 設置主視窗的尺寸
        self.setGeometry(100, 100, 1920, 1080)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        font = self.setup_status_bar()
        self.setup_main_frame(font)
        self.setup_function_bar()

        # 顯示視窗
        self.show()

    def setup_status_bar(self):
        font = QFont()

        # 創建狀態列
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        status_bar.setGeometry(0, 0, 1920, 100)  # 設置狀態列的尺寸
        status_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色
        status_bar.setSizeGripEnabled(False)  # 隱藏右下角的調整大小的三角形

        # 在狀態列中央加入日期時間
        self.datetime_label = QLabel(self)
        status_bar.addWidget(self.datetime_label, 1)  # 將 QLabel 加入狀態列，並指定伸縮因子為1
        self.datetime_label.setAlignment(Qt.AlignCenter)  # 文字置中
        font.setPointSize(36)
        self.datetime_label.setFont(font)

        # 更新日期時間的 QTimer
        self.update_datetime_timer = QTimer(self)
        self.update_datetime_timer.timeout.connect(self.update_datetime)
        self.update_datetime_timer.start(1000)  # 每秒更新一次

        # 更新一次日期時間，避免一開始顯示空白
        self.update_datetime()

        return font

    def setup_main_frame(self, font):
        # 創建主畫面
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 100, 960, 780)
        self.main_frame.setStyleSheet("background-color: white;")  # 主畫面背景顏色
        main_label = QLabel("O<sub>2</sub>： 12.56 ppb<br>T： 16.8 °C")  # ° 為Alt 0176
        main_label.setAlignment(Qt.AlignCenter)  # 文字置中
        font.setPointSize(72)
        main_label.setFont(font)
        main_frame_layout = QVBoxLayout(self.main_frame)
        main_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        main_frame_layout.addWidget(main_label)

        # 創建子畫面堆疊
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(960, 100, 960, 780)

        # 創建子畫面1
        self.sub_frame1 = QFrame(self)
        self.sub_frame1.setStyleSheet("background-color: lightblue;")  # 子畫面背景顏色
        self.setup_sub_frame1()
        self.stacked_widget.addWidget(self.sub_frame1)

        # 創建子畫面2
        self.sub_frame2 = QFrame(self)
        self.sub_frame2.setStyleSheet("background-color: lightcoral;")  # 子畫面背景顏色
        self.setup_sub_frame2(self.sub_frame2)  # 設置子畫面2的內容
        self.stacked_widget.addWidget(self.sub_frame2)

        main_frame_layout.addWidget(self.stacked_widget, 1)  # 子畫面堆疊佔用 1 的高度

    def setup_function_bar(self):
        # 創建功能列
        function_bar = QFrame(self)
        function_bar.setGeometry(0, 880, 1920, 200)  # 設置功能列的尺寸
        function_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色

        # 創建一個放置元件的頂層佈局
        layout = QVBoxLayout(self.centralWidget())
        layout.setContentsMargins(0, 0, 0, 0)  # 消除佈局的邊距
        layout.setSpacing(0)

        # 添加狀態列到佈局
        layout.addWidget(self.statusBar(), 1)  # 狀態列佔用 1 的高度

        # 創建一個放置元件的子佈局
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(0)

        # 添加主畫面到佈局
        grid_layout.addWidget(self.main_frame, 1)  # 主畫面佔用 1 的寬度

        # 添加子佈局到佈局
        layout.addLayout(grid_layout, 8)

        # 添加功能列到佈局
        layout.addWidget(function_bar, 2)  # 功能列佔用 2 的高度

        # 在功能列中添加按鈕
        self.menu_button = QPushButton('選單', function_bar)
        self.menu_button.clicked.connect(self.toggle_sub_frame)

    def setup_sub_frame1(self):
        self.sub_label1 = QLabel('子畫面1', self.sub_frame1)
        self.sub_label1.setAlignment(Qt.AlignCenter)  # 文字置中
        font = QFont()
        font.setPointSize(72)
        self.sub_label1.setFont(font)
        self.sub_frame_layout1 = QGridLayout(self.sub_frame1)
        self.sub_frame_layout1.setContentsMargins(0, 0, 0, 0)
        self.sub_frame_layout1.setSpacing(0)  # 添加這一行以消除元素之間的間距
        self.sub_frame_layout1.addWidget(self.sub_label1)

    def setup_sub_frame2(self, frame):
        sub_label2 = QLabel('子畫面2', frame)
        sub_label2.setAlignment(Qt.AlignCenter)  # 文字置中
        font = QFont()
        font.setPointSize(72)
        sub_label2.setFont(font)
        sub_frame_layout2 = QVBoxLayout(frame)
        sub_frame_layout2.setContentsMargins(0, 0, 0, 0)
        sub_frame_layout2.setSpacing(0)  # 添加這一行以消除元素之間的間距
        sub_frame_layout2.addWidget(sub_label2)

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        self.datetime_label.setText(formatted_datetime)

    def toggle_sub_frame(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.menu_button.setText('反回')
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.menu_button.setText('選單')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
