# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:20:12 2020

@author: wuqian
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
path_text = ''
f_name = ''

class dl_save_csv(QWidget):
    def __init__(self):
        super(dl_save_csv, self).__init__()
        self.setWindowTitle('保存路径：')
        self.resize(600, 150)
        
        self.vlt = QVBoxLayout(self)
        
        self.l = QLabel('保存路径：')
        self.le = QLineEdit()
        
        self.btn = QPushButton('确认')
        self.btn.setMaximumWidth(100)
        self.btn.clicked.connect(self.p)
        
        self.vlt.addWidget(self.l)
        self.vlt.addWidget(self.le)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)
        self.hlt.addStretch()
        self.hlt.addWidget(self.btn)
    def p(self):
        global path_text
        path_text = self.le.text()
        self.le.setText('')
        a = path_text.split('\\')
        b = '\\'.join(a)
        path_text = b
        self.close()

class dl_save_f(QWidget):
    def __init__(self):
        super(dl_save_f, self).__init__()
        self.setWindowTitle('保存指标模板')
        self.resize(350, 150)
        
        self.vlt = QVBoxLayout(self)
        
        self.l = QLabel('指标模板命名：')
        self.le = QLineEdit()
        
        self.btn = QPushButton('确认')
        self.btn.setMaximumWidth(100)
        self.btn.clicked.connect(self.p)
        
        self.vlt.addWidget(self.l)
        self.vlt.addWidget(self.le)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)
        self.hlt.addStretch()
        self.hlt.addWidget(self.btn)
    def p(self):
        global f_name
        f_name = self.le.text()
        self.close()