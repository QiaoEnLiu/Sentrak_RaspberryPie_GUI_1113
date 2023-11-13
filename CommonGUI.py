import sys
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
      QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
      QPushButton
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 設置主視窗的尺寸
        self.setGeometry(100, 100, 1920, 1080)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

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

        # 創建主畫面
        main_frame = QFrame(self)
        main_frame.setGeometry(0, 100, 960, 780)
        main_frame.setStyleSheet("background-color: white;")  # 主畫面背景顏色
        main_label = QLabel("O<sub>2</sub>： 12.56 ppb<br>T： 16.8 °C") # ° 為Alt 0176
        main_label.setAlignment(Qt.AlignCenter)  # 文字置中
        font.setPointSize(72)
        main_label.setFont(font)
        main_frame_layout = QVBoxLayout(main_frame)
        # main_frame_layout.setContentsMargins(0, 0, 0, 0)
        main_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        main_frame_layout.addWidget(main_label)

        # 創建子畫面
        sub_frame = QFrame(self)
        sub_frame.setGeometry(960, 100, 960, 780)
        sub_frame.setStyleSheet("background-color: lightblue;")  # 子畫面背景顏色
        sub_label = QLabel('子畫面')
        sub_label.setAlignment(Qt.AlignCenter)  # 文字置中
        font.setPointSize(72)
        sub_label.setFont(font)
        sub_frame_layout = QVBoxLayout(sub_frame)
        # sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        sub_frame_layout.setSpacing(0)  # 添加這一行以消除元素之間的間距
        sub_frame_layout.addWidget(sub_label)


        # 創建功能列
        function_bar = QFrame(self)
        function_bar.setGeometry(0, 880, 1920, 200)  # 設置功能列的尺寸
        function_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色

        # 創建一個放置元件的頂層佈局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 消除佈局的邊距
        layout.setSpacing(0)

        # 添加狀態列到佈局
        layout.addWidget(status_bar, 1)  # 狀態列佔用 1 的高度

        # 創建一個放置元件的子佈局
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(0)

        # 添加主畫面到佈局
        grid_layout.addWidget(main_frame, 1)  # 第二個參數是優先級，表示佔用100的寬度

        # 添加子畫面到佈局
        grid_layout.addWidget(sub_frame, 1)

        # 添加子佈局到佈局
        layout.addLayout(grid_layout,8)

        # 添加功能列到佈局
        layout.addWidget(function_bar, 2)  # 功能列佔用 2 的高度

        # 在功能列中添加按鈕
        save_button = QPushButton('資料儲存', function_bar)
        lock_button = QPushButton('螢幕鎖', function_bar)
        menu_button = QPushButton('選單', function_bar)

        # 設定按鈕大小
        button_width, button_height = 200, 200

        save_button.setFixedSize(button_width, button_height)
        lock_button.setFixedSize(button_width, button_height)
        menu_button.setFixedSize(button_width, button_height)

        font.setPointSize(36)
        save_button.setFont(font)
        lock_button.setFont(font)
        menu_button.setFont(font)

        # 將 SpacerItem 插入按鈕之間，靠左、置中、靠右
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        function_bar_layout = QHBoxLayout(function_bar)
        function_bar_layout.addWidget(save_button)
        function_bar_layout.addItem(spacer_left)
        function_bar_layout.addWidget(lock_button)
        function_bar_layout.addItem(spacer_right)
        function_bar_layout.addWidget(menu_button)

        # 顯示視窗
        self.show()

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        self.datetime_label.setText(formatted_datetime)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())