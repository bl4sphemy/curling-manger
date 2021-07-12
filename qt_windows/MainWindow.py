import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from app.league_database import LeagueDatabase
from qt_windows.LeagueEditor import LeagueEditor
from app.CurlingLeagueManager import League

UI_MainWindow, QtBaseWindow = uic.loadUiType('MainWindow.ui')

""" Class to auto-generate the python UI files for MainWindow"""


class MainWindow(QtBaseWindow, UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_oid = 0
        self.setupUi(self)
        self.db1 = LeagueDatabase()
        self.main_load_button.clicked.connect(self.load_button_clicked)
        self.main_save_button.clicked.connect(self.save_button_clicked)
        self.main_import_button.clicked.connect(self.import_button_clicked)
        self.main_export_button.clicked.connect(self.export_button_clicked)
        self.main_delete_button.clicked.connect(self.delete_button_clicked)
        self.main_edit_button.clicked.connect(self.edit_button_clicked)
        self.main_add_button.clicked.connect(self.add_button_clicked)

    def load_button_clicked(self):
        dialog = QFileDialog()
        filename = str(dialog.getOpenFileName(filter="*.dat")[0])
        self.db1.load(filename)
        print(self.db1.leagues)
        self.update_ui()

    def save_button_clicked(self):
        dialog = QFileDialog()
        filename = str(dialog.getOpenFileName(filter="*.dat")[0])
        self.db1.save(filename)

    def import_button_clicked(self):
        row = self.main_list_widget.currentRow()
        league_name = self.db1.leagues[row].name
        dialog = QFileDialog()
        filename = str(dialog.getOpenFileName(filter="*.csv")[0])
        self.db1.import_league(league_name, filename)
        self.update_ui()

    def export_button_clicked(self):
        pass

    def delete_button_clicked(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setWindowTitle("Delete League")
        dialog.setText("Are you sure you want to delete this item?")
        yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        dialog.addButton("No", QMessageBox.ButtonRole.NoRole)
        current = self.main_list_widget.currentRow()
        # current = self.main_list_widget.currentItem()
        dialog.exec()
        if dialog.clickedButton() == yes_button:
            del self.db1.leagues[current]
            self.update_ui()
        else:
            dialog.close()

    def edit_button_clicked(self):
        row = self.main_list_widget.currentRow()
        edit_window = LeagueEditor(self.db1.leagues[row], self.db1)
        edit_window.exec()

    def add_button_clicked(self):
        new_league = League(self.db1.next_oid(), self.name_line_edit.text())
        self.db1.add_league(new_league)
        self.update_ui()

    def update_ui(self):
        self.main_list_widget.clear()
        for l in self.db1.leagues:
            self.main_list_widget.addItem(l.name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
