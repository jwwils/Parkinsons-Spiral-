import sys
import time
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtCore import Qt

class DrawingCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.pen = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.path = None
        self.pen_lift_count = 0
        self.points = []
        self.pressure = 1.0
        self.start_time = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.start_time is None:
                self.start_time = time.time()
            self.path = QPainterPath()
            self.path.moveTo(event.pos())
            self.scene().addPath(self.path, self.pen)
            elapsed_time = round(time.time() - self.start_time)
            elapsed_time = max(1, elapsed_time)  # Exclude 0
            self.points.append((event.pos().x(), event.pos().y(), self.pressure, elapsed_time))

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.path is not None:
            self.path.lineTo(event.pos())
            self.scene().addPath(self.path, self.pen)
            self.path = QPainterPath()
            self.path.moveTo(event.pos())
            elapsed_time = round(time.time() - self.start_time)
            elapsed_time = max(1, elapsed_time)  # Exclude 0
            self.points.append((event.pos().x(), event.pos().y(), self.pressure, elapsed_time))

    def mouseReleaseEvent(self, event):
        self.path = None
        self.pen_lift_count += 1

class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = DrawingCanvas()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.canvas.scene().clear)
        layout.addWidget(clear_button)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_drawing)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Drawing App')
        self.setGeometry(100, 100, 800, 600)

    def save_drawing(self):
        total_time = time.time() - self.canvas.start_time

        # Save data
        with open('drawing_data.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['x', 'y', 'total_lifts', 'total_time'])
            for idx, point in enumerate(self.canvas.points[:-1]):
                csv_writer.writerow(point[:2])
            last_point = self.canvas.points[-1]
            csv_writer.writerow(last_point[:2] + (self.canvas.pen_lift_count, total_time))

        print(f"Pen lifted {self.canvas.pen_lift_count} times")
        print(f"Total drawing time: {total_time:.2f} seconds")

        # Reset
        self.canvas.scene().clear()
        self.canvas.points = []
        self.canvas.pen_lift_count = 0
        self.canvas.start_time = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    drawing_app = DrawingApp()
    drawing_app.show()
    sys.exit(app.exec_())
