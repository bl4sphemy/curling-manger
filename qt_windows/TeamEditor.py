import sys
from PyQt5 import uic, QtWidgets

UI_MainWindow, QtBaseWindow = uic.loadUiType('TeamEditor.ui')

class TeamEditor(QtBaseWindow, UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.team_delete_btn.clicked.connect(self.delete_button_clicked)
        self.team_update_btn.clicked.connect(self.update_button_clicked)
        self.team_add_btn.clicked.connect(self.add_button_clicked)


    def delete_button_clicked(self):
        pass

    def update_button_clicked(self):
        pass
    
    def add_button_clicked(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec())
