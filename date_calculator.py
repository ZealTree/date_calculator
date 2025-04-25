import sys
from dateutil.relativedelta import relativedelta
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                            QDateEdit, QTimeEdit, QPushButton, QHBoxLayout,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import QDate, QTime, Qt
from PyQt6.QtGui import QIcon
from datetime import datetime

class DateTimeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор времени')
        self.setGeometry(300, 300, 700, 300)
        # Set the window icon
        self.setWindowIcon(QIcon('assets/icon.ico'))

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Начало отсчета
        start_layout = QHBoxLayout()
        start_label = QLabel('Начало отсчета:')
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm")
        self.start_time_edit.setTime(QTime.currentTime())
        
        start_now_btn = QPushButton('Сейчас')
        start_now_btn.clicked.connect(lambda: self.set_current_datetime(self.start_date_edit, self.start_time_edit))
        
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_date_edit)
        start_layout.addWidget(self.start_time_edit)
        start_layout.addWidget(start_now_btn)

        # Конец отсчета
        end_layout = QHBoxLayout()
        end_label = QLabel('Конец отсчета:')
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm")
        self.end_time_edit.setTime(QTime.currentTime())
        
        end_now_btn = QPushButton('Сейчас')
        end_now_btn.clicked.connect(lambda: self.set_current_datetime(self.end_date_edit, self.end_time_edit))
        
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.end_date_edit)
        end_layout.addWidget(self.end_time_edit)
        end_layout.addWidget(end_now_btn)

        # Кнопка расчета
        calculate_btn = QPushButton('Рассчитать разницу')
        calculate_btn.clicked.connect(self.calculate_difference)

        # Таблица результатов
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['Годы', 'Месяцы', 'Дни', 'Часы', 'Минуты', 'Секунды'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.result_table.setRowCount(1)
        self.result_table.verticalHeader().setVisible(False)
        
        # Настраиваем стиль таблицы
        self.result_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: none;
            }
        """)

        # Добавляем все в основной layout
        main_layout.addLayout(start_layout)
        main_layout.addLayout(end_layout)
        main_layout.addWidget(calculate_btn)
        main_layout.addWidget(QLabel('Результат:'))
        main_layout.addWidget(self.result_table)

        self.setLayout(main_layout)

    def set_current_datetime(self, date_edit, time_edit):
        date_edit.setDate(QDate.currentDate())
        time_edit.setTime(QTime.currentTime())

    def calculate_difference(self):
        try:
            # Получаем начальную дату и время
            start_qdate = self.start_date_edit.date()
            start_qtime = self.start_time_edit.time()
            start_datetime = datetime(
                start_qdate.year(), start_qdate.month(), start_qdate.day(),
                start_qtime.hour(), start_qtime.minute()
            )

            # Получаем конечную дату и время
            end_qdate = self.end_date_edit.date()
            end_qtime = self.end_time_edit.time()
            end_datetime = datetime(
                end_qdate.year(), end_qdate.month(), end_qdate.day(),
                end_qtime.hour(), end_qtime.minute()
            )

            # Для удобства: всегда считаем от меньшей даты к большей
            if start_datetime > end_datetime:
                start_datetime, end_datetime = end_datetime, start_datetime

            # Вычисляем точную разницу с помощью relativedelta
            delta = relativedelta(end_datetime, start_datetime)

            # Обновляем таблицу результатов
            self.update_table_cell(0, 0, str(delta.years))
            self.update_table_cell(0, 1, str(delta.months))
            self.update_table_cell(0, 2, str(delta.days))
            self.update_table_cell(0, 3, str(delta.hours))
            self.update_table_cell(0, 4, str(delta.minutes))
            self.update_table_cell(0, 5, str(delta.seconds))

        except Exception as e:
            print(f"Ошибка при расчете: {e}")

    def update_table_cell(self, row, col, value):
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_table.setItem(row, col, item)

def main():
    app = QApplication(sys.argv)
    window = DateTimeCalculator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()