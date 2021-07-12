import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from app.CurlingLeagueManager import League

UI_MainWindow, QtBaseWindow = uic.loadUiType('LeagueEditor.ui')
from qt_windows.TeamEditor import TeamEditor


class LeagueEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, league_obj, db_obj, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tmp_league = league_obj
        self.db = db_obj
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
        print(self.tmp_league._teams[current])
        dialog.exec()
        if dialog.clickedButton() == yes_button:
            del self.tmp_league._teams[current]
            self.update_ui()
        else:
            dialog.close()

    def edit_button_clicked(self):
        print(self.tmp_league)
        print(self.db)
        #row = self.league_list_widget.currentRow()
        #for i in self.db.leagues:
        #   if i.name == self.league:
        #team_obj = self.league_holder._teams[row]
        #team_obj.members()
        #edit_window = TeamEditor(team_obj)
        #edit_window.exec()
        # print(league)

    def add_button_clicked(self):
        self.tmp_league.add_team(self.team_name_line.text())
        self.update_ui()

    def update_ui(self):
        self.league_list_widget.clear()
        for t in self.tmp_league._teams:
            self.league_list_widget.addItem(t)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec())
