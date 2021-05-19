import json
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog
from PySide6.QtGui import QCloseEvent

_OUT_FILENAME = 'log_merged.jsonl'

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.log1_button = QPushButton('Choose Log1 File')
        self.log1_path_label = QLabel('Path to log1')
        self.log1_path = None

        self.log2_button = QPushButton('Choose Log2 File')
        self.log2_path_label = QLabel('Path to log2')
        self.log2_path = None

        self.out_button = QPushButton('Choose Output Directory')
        self.out_path_label = QLabel('Path to output dir')
        self.out_path = None

        self.merge_button = QPushButton('Merge')
        self.grid = QGridLayout()
        self.setup()

    def select_log1_file(self):
        filepath, _ = QFileDialog.getOpenFileName()
        self.log1_path_label.setText(filepath)
        self.log1_path = Path(filepath)

    def select_log2_file(self):
        filepath, _ = QFileDialog.getOpenFileName()
        self.log2_path_label.setText(filepath)
        self.log2_path = Path(filepath)

    def select_out_dir(self):
        out_dir = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.out_path_label.setText(out_dir)
        self.out_path = Path(out_dir).joinpath(_OUT_FILENAME)

    def merge_logs(self):
        log1_file, log2_file = open(self.log1_path, 'r'), open(self.log2_path, 'r')
        out_file = open(self.out_path, 'w')

        log1_lines, log2_lines = log1_file.readlines(), log2_file.readlines()
        counter1, counter2 = 0, 0

        while counter1 < len(log1_lines) and counter2 < len(log2_lines):
            line1, line2 = log1_lines[counter1], log2_lines[counter2]
            line1_json = json.loads(line1)
            line2_json = json.loads(line2)

            line1_time = datetime.strptime(line1_json['timestamp'], '%Y-%m-%d %H:%M:%S')
            line2_time = datetime.strptime(line2_json['timestamp'], '%Y-%m-%d %H:%M:%S')

            if line1_time < line2_time:
                data = line1
                counter1 += 1
            else:
                data = line2
                counter2 += 1
            out_file.write(data)

        while counter1 < len(log1_lines):  # remaining from the log1
            data = log1_lines[counter1]
            out_file.write(data)
            counter1 += 1

        while counter2 < len(log2_lines):  # remaining from the log2
            data = log2_lines[counter2]
            out_file.write(data)
            counter2 += 1

        log1_file.close()
        log2_file.close()
        out_file.close()

        msg = QMessageBox()
        msg.information(self, 'Message', 'Log files were successfully merged!')

    def setup(self):
        self.setGeometry(200, 200, 800, 450)
        self.setWindowTitle('Merge Logs')

        self.log1_button.clicked.connect(self.select_log1_file)
        self.log2_button.clicked.connect(self.select_log2_file)
        self.out_button.clicked.connect(self.select_out_dir)
        self.merge_button.clicked.connect(self.merge_logs)

        self.grid.addWidget(self.log1_button, 0, 0)
        self.grid.addWidget(self.log1_path_label, 0, 1)
        self.grid.addWidget(self.log2_button, 1, 0)
        self.grid.addWidget(self.log2_path_label, 1, 1)
        self.grid.addWidget(self.out_button, 2, 0)
        self.grid.addWidget(self.out_path_label, 2, 1)
        self.grid.addWidget(self.merge_button, 3, 0, 1, 2)
        self.setLayout(self.grid)
        self.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication([])

    wind = Window()

    app.exec()


if __name__ == '__main__':
    main()
