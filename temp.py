import sys
import os
import zipfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QLabel, QProgressBar,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal


# 解压线程（避免UI卡顿）
class UnzipThread(QThread):
    # 定义信号：进度更新、解压完成、出错提示
    progress_signal = pyqtSignal(int)
    finish_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, zip_path, extract_path):
        super().__init__()
        self.zip_path = zip_path  # ZIP文件路径
        self.extract_path = extract_path  # 解压目标路径

    def run(self):
        try:
            # 检查ZIP文件是否有效
            if not zipfile.is_zipfile(self.zip_path):
                self.error_signal.emit("所选文件不是有效的ZIP压缩包！")
                return

            # 打开ZIP文件
            with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
                file_list = zip_file.namelist()
                total_files = len(file_list)
                processed = 0

                # 遍历所有文件并解压
                for file_name in file_list:
                    # 处理中文路径/文件名编码问题
                    file_name = file_name.encode('cp437').decode('gbk')
                    extract_file_path = os.path.join(self.extract_path, file_name)
                    
                    # 创建父目录（避免文件路径不存在）
                    extract_dir = os.path.dirname(extract_file_path)
                    if not os.path.exists(extract_dir):
                        os.makedirs(extract_dir)
                    
                    # 解压文件
                    zip_file.extract(file_name, self.extract_path)
                    
                    # 更新进度
                    processed += 1
                    progress = int((processed / total_files) * 100)
                    self.progress_signal.emit(progress)

            self.finish_signal.emit(f"解压完成！\n文件已解压至：{self.extract_path}")

        except Exception as e:
            self.error_signal.emit(f"解压失败：{str(e)}")


# 主窗口
class UnzipWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZIP解压工具")
        self.setFixedSize(500, 200)

        # 初始化变量
        self.zip_path = ""
        self.extract_path = ""

        # 构建UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 选择ZIP文件
        zip_layout = QHBoxLayout()
        zip_layout.addWidget(QLabel("压缩包："))
        self.zip_label = QLabel("未选择")
        zip_layout.addWidget(self.zip_label)
        self.zip_btn = QPushButton("选择文件")
        self.zip_btn.clicked.connect(self.select_zip_file)
        zip_layout.addWidget(self.zip_btn)
        layout.addLayout(zip_layout)

        # 选择解压路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("解压至："))
        self.path_label = QLabel("未选择")
        path_layout.addWidget(self.path_label)
        self.path_btn = QPushButton("选择路径")
        self.path_btn.clicked.connect(self.select_extract_path)
        path_layout.addWidget(self.path_btn)
        layout.addLayout(path_layout)

        # 解压按钮
        self.unzip_btn = QPushButton("开始解压")
        self.unzip_btn.clicked.connect(self.start_unzip)
        self.unzip_btn.setEnabled(False)  # 初始禁用
        layout.addWidget(self.unzip_btn)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

    def select_zip_file(self):
        """选择ZIP压缩包"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择ZIP压缩包", "", "ZIP文件 (*.zip)"
        )
        if file_path:
            self.zip_path = file_path
            self.zip_label.setText(os.path.basename(file_path))
            # 检查是否已选择解压路径，启用解压按钮
            self.check_enable_unzip()

    def select_extract_path(self):
        """选择解压目标路径"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择解压路径")
        if dir_path:
            self.extract_path = dir_path
            self.path_label.setText(dir_path)
            # 检查是否已选择压缩包，启用解压按钮
            self.check_enable_unzip()

    def check_enable_unzip(self):
        """检查是否满足解压条件，启用/禁用解压按钮"""
        if self.zip_path and self.extract_path:
            self.unzip_btn.setEnabled(True)
        else:
            self.unzip_btn.setEnabled(False)

    def start_unzip(self):
        """启动解压线程"""
        # 禁用按钮，防止重复点击
        self.unzip_btn.setEnabled(False)
        self.zip_btn.setEnabled(False)
        self.path_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        # 创建并启动解压线程
        self.unzip_thread = UnzipThread(self.zip_path, self.extract_path)
        self.unzip_thread.progress_signal.connect(self.progress_bar.setValue)
        self.unzip_thread.finish_signal.connect(self.on_unzip_finish)
        self.unzip_thread.error_signal.connect(self.on_unzip_error)
        self.unzip_thread.start()

    def on_unzip_finish(self, msg):
        """解压完成回调"""
        QMessageBox.information(self, "成功", msg)
        # 恢复按钮状态
        self.reset_ui()

    def on_unzip_error(self, msg):
        """解压出错回调"""
        QMessageBox.critical(self, "错误", msg)
        # 恢复按钮状态
        self.reset_ui()

    def reset_ui(self):
        """重置UI状态"""
        self.progress_bar.setValue(0)
        self.zip_btn.setEnabled(True)
        self.path_btn.setEnabled(True)
        self.check_enable_unzip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnzipWindow()
    window.show()
    sys.exit(app.exec_())