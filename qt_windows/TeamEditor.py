import sys
from PyQt5 import uic, QtWidgets
from app.CurlingLeagueManager import TeamMember

UI_MainWindow, QtBaseWindow = uic.loadUiType('TeamEditor.ui')

class TeamEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, db_obj, l_row, t_row, parent=None):
        super().__init__(parent)
        self._last_oid = 0
        self.setupUi(self)
        #self.tmp_team = team_object
        self.db = db_obj
        self.league_row = l_row
        self.team_row = t_row
        self.team_delete_btn.clicked.connect(self.delete_button_clicked)
        self.team_update_btn.clicked.connect(self.update_button_clicked)
        self.team_add_btn.clicked.connect(self.add_button_clicked)
        self.update_ui()


    def delete_button_clicked(self):
        row = self.team_list_widget.currentRow()
        del self.db.leagues[self.league_row]._teams[self.team_row]._team_members[row]
        self.update_ui()

    def update_button_clicked(self):
        row = self.team_list_widget.currentRow()
        self.db.leagues[self.league_row]._teams[self.team_row]._team_members[row].name(self.member_name_line.text())
        self.db.leagues[self.league_row]._teams[self.team_row]._team_members[row].email(self.member_email_line.text())
        #del self.db.leagues[self.league_row]._teams[self.team_row]._team_members[row]
        #self.tmp_team.add_member(self.member_name_line.text(), self.member_email_line.text())
        self.update_ui()

    def add_button_clicked(self):
        tm = TeamMember(self.db.next_oid(), self.member_name_line.text(), self.member_email_line.text())
        self.db.leagues[self.league_row]._teams[self.team_row].add_member(tm)
        self.update_ui()

    def update_ui(self):
        self.team_list_widget.clear()
        #print(self.tmp_team._team_members)
        for tm in self.db.leagues[self.league_row]._teams[self.team_row]._team_members:
            self.team_list_widget.addItem(tm._name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec())
