import os
import sys
#import qdarkstyle
import pdf_add_mark
from ui_pdf_mark_create_MainWindow import Ui_pdf_mark_create_MainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu, QWidget, QApplication, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QObject, Qt

system_file_path, system_file_name = os.path.split(os.path.abspath(sys.argv[0]))

def add_parent_number(csv_reader_list):
    new_csv_read_list = []
    for i, element in enumerate(csv_reader_list):
        if len(element) < 3:
            page_title = element[0]
            parent_number = page_title.count('.')
            if parent_number > 2:
                parent_number = 2
            new_element = list(str(parent_number + 1)) + element
            new_csv_read_list.append(new_element)
    return new_csv_read_list


class pdf_create_mainwindow(QMainWindow, Ui_pdf_mark_create_MainWindow):

    def __init__(self):
        super(pdf_create_mainwindow, self).__init__()
        self.setupUi(self)
        self.mark_table_list = []
        self.mark_table_output_list = []
        self.csv_file_path = ''
        self.pdf_file_path = ''
        self.csv_reader_list = []
        self.page_tolerance = ''
        self.content_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.content_tableWidget.setRowCount(1)
        self.content_tableWidget.setColumnCount(3)
        self.content_tableWidget.setHorizontalHeaderLabels(['大纲级别', '标题', '页码'])
        self.open_file_pushButton.clicked.connect(self.open_csv_file_to_tablewidget_slot)
        self.pdf_open_pushButton.clicked.connect(self.open_pdf_file_slot)
        self.start_pushButton.clicked.connect(self.get_table_widget)
        self.clear_table_pushButton.clicked.connect(self.content_tableWidget.clearContents)
        self.help_action.triggered.connect(self.go_help_document)
        self.content_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.content_tableWidget.customContextMenuRequested.connect(self.right_key_menu)

        #添加软件logo
        ico_filename = 'ico/wwq_logo.ico'
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ico_filename), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)



    def open_csv_file_to_tablewidget_slot(self):
        self.csv_file_path, file_type = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',
                                                                "csv (*.csv);;All files (*.*)")
        if file_type:
            self.path_lineEdit.setText(self.csv_file_path)
            self.csv_reader_list = pdf_add_mark.read_csv_mark(self.csv_file_path)

            check_row_length = self.csv_reader_list[1]
            while '' in check_row_length:
                check_row_length.remove('')
            if len(check_row_length) < 3:
                self.csv_reader_list = add_parent_number(self.csv_reader_list)
                #csv_reader_list_add_first_line = []
                #for line in self.csv_reader_list:
                #    csv_reader_list_add_first_line.append(['1', line[0], line[1]])
                #self.csv_reader_list = csv_reader_list_add_first_line
            print(self.csv_reader_list)
            self.add_table_widget()
            self.statusbar.showMessage('打开' + str(self.csv_file_path))

    def add_table_widget(self):
        self.content_tableWidget.setRowCount(len(self.csv_reader_list))
        self.content_tableWidget.setColumnCount(3)
        self.content_tableWidget.setHorizontalHeaderLabels(['大纲级别', '标题', '页码'])

        for i, elem in enumerate(self.csv_reader_list):
            new_item = QTableWidgetItem(elem[0])
            self.content_tableWidget.setItem(i, 0, new_item)
            new_item = QTableWidgetItem(elem[1])
            self.content_tableWidget.setItem(i, 1, new_item)
            new_item = QTableWidgetItem(elem[2])
            self.content_tableWidget.setItem(i, 2, new_item)
        self.statusbar.showMessage('目录信息已导入')

    def open_pdf_file_slot(self):
        self.pdf_file_path, file_type = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',
                                                              "pdf (*.pdf);;All files (*.*)")
        if file_type:
            self.pdf_path_lineEdit.setText(self.pdf_file_path)
        self.statusbar.showMessage('打开' + str(self.pdf_file_path))

    def get_table_widget(self):

        self.page_tolerance = self.tolerance_lineEdit.text()
        table_row = self.content_tableWidget.rowCount()
        table_column = self.content_tableWidget.columnCount()
        self.mark_table_output_list = []
        for i in range(table_row):
            if bool(self.content_tableWidget.item(i, 0)) is False or bool(
                    self.content_tableWidget.item(i, 1)) is False or bool(self.content_tableWidget.item(i, 2)) is False:
                continue
            table_output_row = []
            for j in range(table_column):
                table_output_row.append(self.content_tableWidget.item(i, j).text())
            self.mark_table_output_list.append(table_output_row)
        pdf_add_mark.create_pdf_mark_csv(self.pdf_file_path, self.mark_table_output_list, int(self.page_tolerance))
        self.statusbar.showMessage('目录导入已完成，查看pdf所在文件夹')

    def right_key_menu(self, pos):
        # rint( pos)
        row_num = -1
        column_num = -1
        for i in self.content_tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
            column_num = i.column()

        menu = QMenu()
        item1 = menu.addAction(u"删除行")
        item2 = menu.addAction(u"插入行")
        item3 = menu.addAction(u"清空行")
        item4 = menu.addAction(u"清空列")

        action = menu.exec_(self.content_tableWidget.mapToGlobal(pos))
        if action == item1:
            self.content_tableWidget.removeRow(row_num)
        elif action == item2:
            self.content_tableWidget.insertRow(row_num)
        elif action == item3:
            for i in range(self.content_tableWidget.columnCount()):
                null_item = QTableWidgetItem('')
                self.content_tableWidget.setItem(row_num, i, null_item)
        elif action == item4:
            for i in range(self.content_tableWidget.rowCount()):
                null_item = QTableWidgetItem('')
                self.content_tableWidget.setItem(i, column_num, null_item)
        else:
            return

    def print_item(self):
        print(self.content_tableWidget.selectedItems())

    def go_help_document(self):
            self.statusbar.showMessage('查看帮助...')
            path = system_file_path + r'\help\html'
            os.system('explorer %s' %path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = pdf_create_mainwindow()
    window.show()
    sys.exit(app.exec_())



