# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 16:14:51 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ranking(QWidget):
    item_list = ['不筛选','前1%','前5%','前20%','后5%']
    item_dict = {0:100, 1:1, 2:5, 3:20, 4:-5}
    def __init__(self):
        super(ranking, self).__init__()
        self.setWindowTitle('依照所选列排序/筛选')
        self.setGeometry(700, 400, 500, 200)
        self.vlt = QVBoxLayout(self)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)

        self.cx = QCheckBox('按类别分别排序')
        self.cx.setMaximumSize(170 , 40)

        self.hlt.addWidget(self.cx)
        self.hlt.addStretch()
        
        self.hlt2 = QHBoxLayout()
        self.vlt.addLayout(self.hlt2)
        
        self.cbx = QComboBox()
        self.cbx.addItems(self.item_list)
        
        self.l_nav2 = QLabel('选择季度')
        self.l_nav2.setMaximumSize(170 , 40)

        self.btn = QPushButton('确认')
        self.btn.clicked.connect(self.out_put)

        self.hlt2.addWidget(self.l_nav2)
        self.hlt2.addWidget(self.cbx)
        self.hlt2.addStretch()
        self.hlt2.addWidget(self.btn)
        
        self.l = QLabel()
        self.l.setFixedHeight(300)
        self.l.setVisible(False)
        self.vlt.addWidget(self.l)
    def out_put(self):
        self.ckeck_state = self.cx.isChecked()
        self.proportion = self.item_dict[self.cbx.currentIndex()]
        print(self.ckeck_state,self.proportion)
        self.close()
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ranking()
    w.show()
    sys.exit(app.exec_())