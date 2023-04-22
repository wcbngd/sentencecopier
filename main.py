import sys
import json, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QPlainTextEdit
from PyQt5.QtCore import Qt, QSettings

class LineEntryWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.copy_button = QPushButton("复制")
        self.copy_button.clicked.connect(self.copy_text)
        self.layout.addWidget(self.copy_button)

    def set_text(self, text):
        self.label.setText(text)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.label.text())

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'PyQt5 UI程序'
        self.filename = 'data.json'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # self.add_line_button = QPushButton("添加行")
        # self.add_line_button.clicked.connect(self.add_line)
        # self.layout.addWidget(self.add_line_button)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_text)
        self.layout.addWidget(self.save_button)

        self.entries_layout = QVBoxLayout()
        self.layout.addLayout(self.entries_layout)

        self.load_data()

    def add_line(self):
        entry_widget = LineEntryWidget()
        self.entries_layout.addWidget(entry_widget)

        text = self.input_line.text()
        if text:
            entry_widget.set_text(text)
            self.input_line.clear()

        self.save_data()

    def save_text(self):
        text = self.input_line.text()
        if text:
            entry_widget = LineEntryWidget()
            entry_widget.set_text(text)
            self.entries_layout.addWidget(entry_widget)
            self.input_line.clear()

            self.save_data()

    def save_data(self):
        data = []
        for i in range(self.entries_layout.count()):
            entry_widget = self.entries_layout.itemAt(i).widget()
            if isinstance(entry_widget, LineEntryWidget):
                text = entry_widget.label.text()
                data.append(text)

        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for text in data:
                    entry_widget = LineEntryWidget()
                    entry_widget.set_text(text)
                    self.entries_layout.addWidget(entry_widget)
        except FileNotFoundError:
            pass


def delete_empty_json_file(file_name):
    # 如果file_name不存在，返回None
    if not os.path.exists(file_name):
        return None
    
    with open(file_name, 'r') as f:
        try:
            content = json.load(f)
            if not content:
                os.remove(file_name)
        except json.decoder.JSONDecodeError:
            # JSON解析失败，可能是因为文件为空或格式错误
            os.remove(file_name)

if __name__ == '__main__':
    delete_empty_json_file(file_name='data.json')
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
