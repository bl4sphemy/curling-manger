import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from app.league_database import LeagueDatabase
from qt_windows.LeagueEditor import LeagueEditor

UI_MainWindow, QtBaseWindow = uic.loadUiType('MainWindow.ui')

""" Class to auto-generate the python UI files for MainWindow"""


class MainWindow(QtBaseWindow, UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.database = LeagueDatabase()
        self.main_load_button.clicked.connect(self.load_button_clicked)
        self.main_save_button.clicked.connect(self.save_button_clicked)
        self.main_delete_button.clicked.connect(self.delete_button_clicked)
        self.main_edit_button.clicked.connect(self.edit_button_clicked)
        self.main_add_button.clicked.connect(self.add_button_clicked)

    # loading the dat file, but it's currently empty
    def load_button_clicked(self):
        dialog = QFileDialog()
        # filename = str(dialog.getOpenFileName(parent=None, '.'))
        filename = str(dialog.getOpenFileName(filter="*.dat")[0])
        self.database.load(filename)
        print(self.database.leagues)
        # self.main_list_widget.addItem(filename)

    def save_button_clicked(self):
        pass

    def delete_button_clicked(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setWindowTitle("Delete League")
        dialog.setText("Are you sure you want to delete this item?")
        yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        dialog.addButton("No", QMessageBox.ButtonRole.NoRole)
        #current = self.main_list_widget.currentRow()
        current = self.main_list_widget.currentItem().text()
        dialog.exec()
        if dialog.clickedButton() == yes_button:
            print(current)
            self.database.leagues.remove(current)
            self.update_ui()
            #self.main_list_widget.takeItem(current)
            # self.main_list_widget.removeItemWidget(current)
        else:
            dialog.close()

    def edit_button_clicked(self):
        row = self.main_list_widget.currentRow()
        league = self.database.leagues[row]
        edit_window = LeagueEditor()
        edit_window.exec()
        print(league)

    def add_button_clicked(self):
        self.database.add_league(self.name_line_edit.text())
        self.update_ui()

    def update_ui(self):
        self.main_list_widget.clear()
        for l in self.database.leagues:
            self.main_list_widget.addItem(l)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
