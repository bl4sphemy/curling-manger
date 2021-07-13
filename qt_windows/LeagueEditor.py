import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from app.CurlingLeagueManager import Team

UI_MainWindow, QtBaseWindow = uic.loadUiType('LeagueEditor.ui')
from qt_windows.TeamEditor import TeamEditor


class LeagueEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, db_obj, l_row, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = db_obj
        self.league_row = l_row
        self.league_delete_btn.clicked.connect(self.delete_button_clicked)
        self.league_edit_btn.clicked.connect(self.edit_button_clicked)
        self.league_add_btn.clicked.connect(self.add_button_clicked)
        self.update_ui()

    def delete_button_clicked(self):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setWindowTitle("Delete Team")
        dialog.setText("Are you sure you want to delete this item?")
        yes_button = dialog.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        dialog.addButton("No", QMessageBox.ButtonRole.NoRole)
        current = self.league_list_widget.currentRow()
        dialog.exec()
        if dialog.clickedButton() == yes_button:
            del self.db.leagues[self.league_row]._teams[current]
            self.update_ui()
        else:
            dialog.close()

    def edit_button_clicked(self):
        row = self.league_list_widget.currentRow()
        edit_window = TeamEditor(self.db, self.league_row, row)
        edit_window.exec()

    def add_button_clicked(self):
        t = Team(self.db.next_oid(), self.team_name_line.text())
        self.db.leagues[self.league_row].add_team(t)
        self.update_ui()

    def update_ui(self):
        self.league_list_widget.clear()
        for t in self.db.leagues[self.league_row]._teams:
            self.league_list_widget.addItem(t.name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec())
