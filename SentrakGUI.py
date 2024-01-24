import sys
from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QWidget, QStatusBar, QVBoxLayout,\
      QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QGridLayout,\
      QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QPixmap, QIcon

class SubFrame(QWidget):
    def __init__(self, title):
        super().__init__()

        font = QFont()
        
        sub_label = QLabel(title, self)
        sub_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        sub_label.setFont(font)
        sub_frame_layout = QVBoxLayout(self)
        sub_frame_layout.setContentsMargins(0, 0, 0, 0)
        sub_frame_layout.setSpacing(0) 
        sub_frame_layout.addWidget(sub_label)

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
        main_frame.setStyleSheet("background-color: white;")  
        main_label = QLabel("O<sub>2</sub>： 12.56 ppb<br>T： 16.8 °C") # ° 為Alt 0176
        main_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        main_label.setFont(font)
        main_frame_layout = QVBoxLayout(main_frame)
        main_frame_layout.setSpacing(0)  
        main_frame_layout.addWidget(main_label)

        # 創建子畫面1
        self.sub_frame1 = QFrame(self)
        self.sub_frame1.setGeometry(960, 100, 960, 780)
        self.sub_frame1.setStyleSheet("background-color: lightblue;")  
        self.sub_label = QLabel('子畫面')
        self.sub_label.setAlignment(Qt.AlignCenter)  
        font.setPointSize(72)
        self.sub_label.setFont(font)
        self.sub_frame_layout1 = QGridLayout(self.sub_frame1)
        self.sub_frame1.setLayout(self.sub_frame_layout1)
        self.sub_frame_layout1.setContentsMargins(0, 0, 0, 0)
        self.sub_frame_layout1.setSpacing(0) 
        self.sub_frame_layout1.addWidget(self.sub_label)

        # 創建子畫面堆疊
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(960, 100, 960, 780)


        # 創建子畫面2
        # sub_frame2 = QFrame(self)
        # sub_frame2.setStyleSheet("background-color: lightcoral;")  # 子畫面背景顏色
        # self.setup_sub_frame2(sub_frame2)  # 設置子畫面2的內容

        # 創建功能列
        function_bar = QFrame(self)
        function_bar.setGeometry(0, 880, 1920, 200)  # 設置功能列的尺寸
        function_bar.setStyleSheet("background-color: lightgray;")  # 設置背景顏色

        
        # 創建一個放置元件的頂層佈局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # 消除佈局的邊距
        layout.setSpacing(0)

        # 創建一個放置元件的子佈局
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(0)

        # 添加狀態列到佈局
        layout.addWidget(status_bar, 1)  # 狀態列佔用 1 的高度

        # 添加主畫面到佈局
        grid_layout.addWidget(main_frame, 1)  # 第二個參數是優先級，表示佔用100的寬度

        # 添加子畫面到佈局
        grid_layout.addWidget(self.sub_frame1, 1)

        # # 添加子佈局到佈局
        layout.addLayout(grid_layout, 8)

        # 添加功能列到佈局
        layout.addWidget(function_bar, 2)  # 功能列佔用 2 的高度

        # 在功能列中添加按鈕
        save_button = QPushButton('資料儲存', function_bar)
        lock_label = QLabel('螢幕鎖',function_bar)
        self.menu_button = QPushButton('選單', function_bar)
        self.return_button = QPushButton('返回', function_bar)

        self.menu_button.clicked.connect(self.show_sub_buttons)
        self.return_button.clicked.connect(self.show_previous_sub_frame)

        # 設定按鈕大小
        button_width, button_height = 200, 200

        save_button.setFixedSize(button_width, button_height)
        self.menu_button.setFixedSize(button_width, button_height)
        self.return_button.setFixedSize(button_width, button_height)

        font.setPointSize(36)
        save_button.setFont(font)
        self.menu_button.setFont(font)
        self.return_button.setFont(font)

        # 設定圖片路徑，picture資料夾和程式碼同一個資料夾中
        lock_icon_path = 'picture/lock_icon.png'
        lock_pixmap = QPixmap(lock_icon_path)
        lock_label.setPixmap(lock_pixmap.scaled(button_width, button_height, Qt.KeepAspectRatio))

        # 將 SpacerItem 插入按鈕之間，靠左、置中、靠右
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        function_bar_layout = QHBoxLayout(function_bar)
        function_bar_layout.addWidget(save_button)
        function_bar_layout.addItem(spacer_left)
        function_bar_layout.addWidget(lock_label)
        function_bar_layout.addItem(spacer_right)
        function_bar_layout.addWidget(self.menu_button)
        function_bar_layout.addWidget(self.return_button)

        self.menu_button.setVisible(True)
        self.return_button.setVisible(False)

        # 顯示視窗
        self.show()

        # 添加一個變數用於存儲原本的四個按鈕區域的內容
        # self.original_content_layout = None

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("yyyy-MM-dd hh:mm:ss")
        self.datetime_label.setText(formatted_datetime)

    def show_sub_buttons(self):
        print("show_sub_buttons is called")
        print(self.stacked_widget.count())


        # 清除堆疊中的子畫面
        # for i in reversed(range(self.stacked_widget.count())):
        #     widget = self.stacked_widget.widget(i)
        #     self.stacked_widget.removeWidget(widget)
        #     widget.setParent(None)

        # 保留原本的佈局
        # self.original_content_layout = self.sub_frame1.layout()

        # 將GridLayout設置為子畫面的佈局
        self.sub_frame1.setLayout(self.sub_frame_layout1)

        # 顯示四個按鈕
        set_button = QPushButton('設定', self.sub_frame1)
        calibrate_button = QPushButton('校正', self.sub_frame1)
        record_button = QPushButton('紀錄', self.sub_frame1)
        identify_button = QPushButton('識別', self.sub_frame1)

        # 設定按鈕大小
        button_width, button_height = 300, 300

        set_button.setFixedSize(button_width, button_height)
        calibrate_button.setFixedSize(button_width, button_height)
        record_button.setFixedSize(button_width, button_height)
        identify_button.setFixedSize(button_width, button_height)

        # 連接按鈕點擊事件
        set_button.clicked.connect(lambda: self.show_sub_frame_content('設定'))
        calibrate_button.clicked.connect(lambda: self.show_sub_frame_content('校正'))
        record_button.clicked.connect(lambda: self.show_sub_frame_content('紀錄'))
        identify_button.clicked.connect(lambda: self.show_sub_frame_content('識別'))

        # 設定按鈕的背景顏色，方便檢查它們的可見性
        set_button.setStyleSheet("background-color: red;")
        calibrate_button.setStyleSheet("background-color: green;")
        record_button.setStyleSheet("background-color: blue;")
        identify_button.setStyleSheet("background-color: yellow;")

        subFont = QFont()
        subFont.setPointSize(32)
        set_button.setFont(subFont)
        calibrate_button.setFont(subFont)
        record_button.setFont(subFont)
        identify_button.setFont(subFont)

        # 將按鈕添加到GridLayout中
        self.sub_frame_layout1.addWidget(set_button, 0, 0, 1, 1)
        self.sub_frame_layout1.addWidget(calibrate_button, 0, 1, 1, 1)
        self.sub_frame_layout1.addWidget(record_button, 1, 0, 1, 1)
        self.sub_frame_layout1.addWidget(identify_button, 1, 1, 1, 1)

        # 清除堆疊中的子畫面
        self.stacked_widget.setCurrentIndex(0)

        self.menu_button.setVisible(False)
        self.return_button.setVisible(True)

        # 設定子畫面1的位置和大小
        self.sub_frame1.setGeometry(960, 100, 960, 780)
        print("After setting geometry:", self.sub_frame1.geometry())

        # 將子畫面1添加到堆疊中
        self.stacked_widget.addWidget(self.sub_frame1)        

        print("Current stacked widget index:", self.stacked_widget.currentIndex())

    def show_sub_frame_content(self, content):
        print(f"Showing content: {content}")

        # 創建新的子畫面
        sub_frame = SubFrame(content)

        # 清除堆疊中的子畫面
        for i in reversed(range(self.stacked_widget.count())):
            widget = self.stacked_widget.widget(i)
            self.stacked_widget.removeWidget(widget)
            widget.setParent(None)

        # 將新的子畫面添加到堆疊中
        self.stacked_widget.addWidget(sub_frame)

        # 設置當前顯示的子畫面
        self.current_sub_frame = sub_frame
        self.stacked_widget.setCurrentWidget(sub_frame)

        # 設定當前顯示的子畫面索引
        self.stacked_widget.setCurrentIndex(self.stacked_widget.indexOf(self.current_sub_frame))

    def show_previous_sub_frame(self):
        # 返回上一個子畫面
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

        else:
            # 如果已經是第一個子畫面，顯示原本的四個按鈕區域的內容
            self.stacked_widget.setCurrentIndex(-1)
            # self.sub_frame_layout1 = self.original_content_layout
            self.sub_frame1.setLayout(self.sub_frame_layout1)
            self.menu_button.setVisible(True)
            self.return_button.setVisible(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())