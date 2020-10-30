# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 15:46:57 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import nb_0, w1_fin
tree_dict = {'风险': [['流动性风险'], ['市场风险'], ['信用风险']],
             '业绩': [['公司产品业绩'], ['各经理业绩'], ['市场业绩']],
             '归因': [['绝对收益'], ['相对收益']]}
class Demo(QWidget):
    def __init__(self):
        super(Demo,self).__init__()
        widget = QWidget()
        self.stacked_layout = QStackedLayout()
        widget.setLayout(self.stacked_layout)
        
        hlt = QHBoxLayout(self)
        self.vlt = QVBoxLayout()
        hlt.addLayout(self.vlt)
        self.set_forms()
        self.vlt.addStretch()
        
        hlt.addWidget(widget)

    def set_forms(self):
        self.form1 = w1_fin.window1()
        self.stacked_layout.addWidget(self.form1)
        self.btn1 = QPushButton("市场宏观指标")
        self.vlt.addWidget(self.btn1)
        self.btn1.clicked.connect(self.btn1_Clicked)
        
        self.form2 = nb_0.window2()
        self.stacked_layout.addWidget(self.form2)
        self.btn2 = QPushButton("同业业绩比较")
        self.vlt.addWidget(self.btn2)
        self.btn2.clicked.connect(self.btn2_Clicked)
        
        
    def btn1_Clicked(self):
        self.stacked_layout.setCurrentIndex(0)

    def btn2_Clicked(self):
        self.stacked_layout.setCurrentIndex(1)
        
class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setWindowTitle("系统框架")
        #exit_menu
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu('&App')
        fileMenu.addAction(exitAct)
        
        self.set_check_menu()
        self.demo = Demo()
        self.setCentralWidget(self.demo)
    def set_check_menu(self):
        menu = self.menubar.addMenu('View')
        self.set_check_menu_cycle(menu, tree_dict)
    def set_check_menu_cycle(self, root, d):
        for i in d.keys():
            submenu = root.addMenu(i)
            if type(d[i]) == type([]):
                for j in d[i]:
                    if type(j) == type(''):
                        submenu.addAction(j)
                    elif type(j) == type([]):
                        act = QAction(j[0], self, checkable=True)
                        act.setChecked(False)
                        submenu.addAction(act)
            else:
                self.set_check_menu_cycle(submenu, d[i])

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Main()
    w.showMaximized()
    #w.showFullScreen()
    sys.exit(app.exec_())