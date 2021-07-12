import sys
from PyQt5 import uic, QtWidgets
from app.CurlingLeagueManager import Team, TeamMember

UI_MainWindow, QtBaseWindow = uic.loadUiType('TeamEditor.ui')

class TeamEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, team_object, db_obj, parent=None):
        super().__init__(parent)
        self._last_oid = 0
        self.setupUi(self)
        self.tmp_team = team_object
        self.tmp_db = db_obj
        self.team_delete_btn.clicked.connect(self.delete_button_clicked)
        self.team_update_btn.clicked.connect(self.update_button_clicked)
        self.team_add_btn.clicked.connect(self.add_button_clicked)
        #self.update_ui()


    def delete_button_clicked(self):
        row = self.team_list_widget.currentRow()
        self.tmp_team._team_members.remove(row)
        self.update_ui()

    def update_button_clicked(self):
        row = self.team_list_widget.currentRow()
        self.tmp_team.members.remove(row)
        self.tmp_team.add_member(self.member_name_line.text(), self.member_email_line.text())
        self.update_ui()

    def add_button_clicked(self):
        self.tmp_team.add_member(self.member_name_line.text(), self.member_email_line.text())
        self.update_ui()

    def update_ui(self):
        self.team_list_widget.clear()
        print(self.tmp_team._team_members)
        #for tm in self.tmp_team._team_members:
        #    self.team_list_widget.addItem(tm)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec())
