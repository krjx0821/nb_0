# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:34:26 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import nb_dl_02

class window(QWidget):
    def __init__(self, l1, l2, l3):
        super(window,self).__init__()
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.setWindowTitle("修改指标参数")
        self.resize(750, 600)
        self.hlt = QHBoxLayout(self)
        self.tree = QListWidget()
        self.tree.setMaximumWidth(450)
        self.hlt.addWidget(self.tree)
        self.vlt = QVBoxLayout()
        self.hlt.addLayout(self.vlt)
        self.btn0 = QPushButton('清空指标')
        self.btn0.setMinimumHeight(50)
        self.btn0.clicked.connect(self.clear_f)
        self.btn1 = QPushButton('删除指标')
        self.btn1.setMinimumHeight(50)
        self.btn1.clicked.connect(self.del_f)
        self.btn2 = QPushButton('修改参数')
        self.btn2.setMinimumHeight(50)
        self.btn2.clicked.connect(self.mod)
        self.btn3 = QPushButton('确认')
        self.btn3.setMinimumHeight(50)
        self.btn3.clicked.connect(self.close)
        self.vlt.addWidget(self.btn0)
        self.vlt.addWidget(self.btn1)
        self.vlt.addWidget(self.btn2)
        self.vlt.addStretch()
        self.vlt.addWidget(self.btn3)
        self.plot_tree()
    def plot_tree(self):
        self.tree.clear()
        for i in range(len(self.l1))[4:]:
            item = QListWidgetItem()
            item.setText(self.l2[i])
            #label = QLabel(self.l2[i])
            self.tree.addItem(item)
            #self.tree.setItemWidget(item, label)
            item.setSizeHint(QSize(80,80))
        self.tree.setSelectionMode(QTableView.ExtendedSelection)
    def clear_f(self):
        l = list(range(4,len(self.l1)))
        l.sort(key=int, reverse=True)
        for i in l:
            del self.l1[i]
            del self.l2[i]
            del self.l3[i]
        self.plot_tree()
    def del_f(self):
        index= self.tree.selectionModel().selectedIndexes()
        l = []
        for i in index:
            print(i.row())
            i = int(i.row()) + 4
            l.append(i)
        l.sort(key=int, reverse=True)
        print(l)
        for i in l:
            del self.l1[i]
            del self.l2[i]
            del self.l3[i]
        self.plot_tree()
    def mod(self):
        index= self.tree.selectionModel().selectedIndexes()
        l = []
        for i in index:
            i = int(i.row())
            l.append(i)
        l.sort(key=int, reverse=False)
        text = self.tree.item(l[0]).text().split('\n')[0]
        global indec
        indec = l[0] + 4
        global dl_m
        if text == '单位净值':
            dl_m = nb_dl_02.dl_1(text,True,self.l3[indec])
        elif text == '收益率' or '最大回撤':
            dl_m = nb_dl_02.dl_2(text,True,self.l3[indec])
        dl_m.show()
        try:
            dl_m.exec_()
        except:
            pass
        dl_m.btn.clicked.connect(self.f_mod)
    def f_mod(self):
        global dl_m, indec
        self.l1[indec] = dl_m.t1
        self.l2[indec] = dl_m.t2
        self.l3[indec] = dl_m.t3
        self.plot_tree()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w1 = window()
    w1.show()
    sys.exit(app.exec())
