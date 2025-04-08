import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                            QDateEdit, QTimeEdit, QPushButton, QHBoxLayout,
                            QCheckBox, QTabWidget)
from PyQt6.QtCore import QDate, QTime, Qt
from datetime import datetime

class DateDifferenceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор времени')
        self.setGeometry(300, 300, 450, 400)

        # Создание вкладок
        tabs = QTabWidget()
        self.tab_countdown = QWidget()
        self.tab_elapsed = QWidget()
        tabs.addTab(self.tab_countdown, "До события")
        tabs.addTab(self.tab_elapsed, "Прошедшее время")

        # Вкладка "До события"
        self.setup_countdown_tab()

        # Вкладка "Прошедшее время"
        self.setup_elapsed_tab()

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def setup_countdown_tab(self):
        layout = QVBoxLayout()

        # Дата
        self.countdown_date_label = QLabel('Выберите дату:')
        self.countdown_date_edit = QDateEdit()
        self.countdown_date_edit.setCalendarPopup(True)
        self.countdown_date_edit.setDate(QDate.currentDate())
        self.countdown_date_edit.setMinimumDate(QDate.currentDate())

        # Время
        self.countdown_time_label = QLabel('Выберите время:')
        self.countdown_time_edit = QTimeEdit()
        self.countdown_time_edit.setDisplayFormat("HH:mm")
        self.countdown_time_edit.setTime(QTime.currentTime())

        datetime_layout = QHBoxLayout()
        datetime_layout.addWidget(self.countdown_date_edit)
        datetime_layout.addWidget(self.countdown_time_edit)

        self.countdown_button = QPushButton('Рассчитать')
        self.countdown_button.clicked.connect(self.calculate_countdown)

        self.countdown_result = QLabel('Результат появится здесь')
        self.countdown_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.countdown_date_label)
        layout.addLayout(datetime_layout)
        layout.addWidget(self.countdown_time_label)
        layout.addWidget(self.countdown_button)
        layout.addWidget(self.countdown_result)
        layout.addStretch()

        self.tab_countdown.setLayout(layout)

    def setup_elapsed_tab(self):
        layout = QVBoxLayout()

        # Начальная дата
        self.start_date_label = QLabel('Начальная дата:')
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())

        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm")
        self.start_time_edit.setTime(QTime.currentTime())

        start_datetime_layout = QHBoxLayout()
        start_datetime_layout.addWidget(self.start_date_edit)
        start_datetime_layout.addWidget(self.start_time_edit)

        # Конечная дата
        self.end_date_label = QLabel('Конечная дата:')
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm")
        self.end_time_edit.setTime(QTime.currentTime())

        self.use_current_checkbox = QCheckBox('Использовать текущее время как конечное')
        self.use_current_checkbox.stateChanged.connect(self.toggle_end_datetime)

        end_datetime_layout = QHBoxLayout()
        end_datetime_layout.addWidget(self.end_date_edit)
        end_datetime_layout.addWidget(self.end_time_edit)

        self.elapsed_button = QPushButton('Рассчитать')
        self.elapsed_button.clicked.connect(self.calculate_elapsed)

        self.elapsed_result = QLabel('Результат появится здесь')
        self.elapsed_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.start_date_label)
        layout.addLayout(start_datetime_layout)
        layout.addWidget(self.end_date_label)
        layout.addLayout(end_datetime_layout)
        layout.addWidget(self.use_current_checkbox)
        layout.addWidget(self.elapsed_button)
        layout.addWidget(self.elapsed_result)
        layout.addStretch()

        self.tab_elapsed.setLayout(layout)

    def toggle_end_datetime(self, state):
        # Включение/отключение полей конечной даты и времени
        self.end_date_edit.setEnabled(not state)
        self.end_time_edit.setEnabled(not state)

    def calculate_countdown(self):
        qdate = self.countdown_date_edit.date()
        qtime = self.countdown_time_edit.time()
        selected_datetime = datetime(
            qdate.year(), qdate.month(), qdate.day(),
            qtime.hour(), qtime.minute()
        )
        current_datetime = datetime.now()

        if selected_datetime <= current_datetime:
            self.countdown_result.setText('Пожалуйста, выберите дату и время в будущем!')
            return

        difference = selected_datetime - current_datetime
        self.display_result(difference, selected_datetime, self.countdown_result, "До")

    def calculate_elapsed(self):
        # Начальная дата и время
        start_qdate = self.start_date_edit.date()
        start_qtime = self.start_time_edit.time()
        start_datetime = datetime(
            start_qdate.year(), start_qdate.month(), start_qdate.day(),
            start_qtime.hour(), start_qtime.minute()
        )

        # Конечная дата и время
        if self.use_current_checkbox.isChecked():
            end_datetime = datetime.now()
        else:
            end_qdate = self.end_date_edit.date()
            end_qtime = self.end_time_edit.time()
            end_datetime = datetime(
                end_qdate.year(), end_qdate.month(), end_qdate.day(),
                end_qtime.hour(), end_qtime.minute()
            )

        if end_datetime <= start_datetime:
            self.elapsed_result.setText('Конечная дата должна быть позже начальной!')
            return

        difference = end_datetime - start_datetime
        self.display_result(difference, end_datetime, self.elapsed_result, "Между", start_datetime)

    def display_result(self, difference, end_datetime, result_label, prefix, start_datetime=None):
        total_seconds = int(difference.total_seconds())
        years = difference.days // 365
        months = difference.days // 30
        days = difference.days
        hours = total_seconds // 3600
        minutes = total_seconds // 60
        seconds = total_seconds

        if start_datetime:
            result_text = (f'{prefix} {start_datetime.strftime("%d.%m.%Y %H:%M")} и '
                          f'{end_datetime.strftime("%d.%m.%Y %H:%M")} прошло:\n')
        else:
            result_text = f'{prefix} {end_datetime.strftime("%d.%m.%Y %H:%M")} осталось:\n'

        result_text += (f'Лет: {years}\n'
                       f'Месяцев: {months}\n'
                       f'Дней: {days}\n'
                       f'Часов: {hours}\n'
                       f'Минут: {minutes}\n'
                       f'Секунд: {seconds}')

        result_label.setText(result_text)

def main():
    app = QApplication(sys.argv)
    window = DateDifferenceCalculator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
