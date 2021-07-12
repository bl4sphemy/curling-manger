import sys
from PyQt5 import uic, QtWidgets

UI_MainWindow, QtBaseWindow = uic.loadUiType('LeagueEditor.ui')
from qt_windows.TeamEditor import TeamEditor

class LeagueEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.league_import_btn.clicked.connect(self.import_button_clicked)
        self.league_export_btn.clicked.connect(self.export_button_clicked)
        self.league_delete_btn.clicked.connect(self.delete_button_clicked)
        self.league_edit_btn.clicked.connect(self.edit_button_clicked)
        self.league_add_btn.clicked.connect(self.add_button_clicked)

    def import_button_clicked(self):
        pass

    def export_button_clicked(self):
        pass

    def delete_button_clicked(self):
        pass

    def edit_button_clicked(self):
        #row = self.league_list_widget.currentRow()
        #league = self.database.leagues[row]
        edit_window = TeamEditor()
        edit_window.exec()
        #print(league)

    def add_button_clicked(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec())
