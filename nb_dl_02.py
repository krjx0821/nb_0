# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:56:01 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class dl_1(QWidget):
    def __init__(self, text, in_mod = False, in_data = None):
        super(dl_1, self).__init__()
        self.setWindowTitle(text)
        self.t = text
        self.setGeometry(700, 400, 500, 100)
        self.vlt = QVBoxLayout(self)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)
        
        self.btn_nav = QPushButton('选择日期')
        self.btn_nav.setFixedSize(80, 40)
        self.btn_nav.clicked.connect(self.show_cal)
        
        self.l_nav1 = QLabel('')
        self.l_nav1.setMaximumSize(170 , 40)

        self.btn = QPushButton('确认')
        self.btn.clicked.connect(self.out_put)

        self.hlt.addWidget(self.btn_nav)
        self.hlt.addWidget(self.l_nav1)
        self.hlt.addStretch()
        self.hlt.addWidget(self.btn)
        
        self.l = QLabel()
        self.l.setFixedHeight(300)
        self.l.setVisible(False)
        self.vlt.addWidget(self.l)

        self.cal()
        if in_mod:
            self.t3 = in_data
            self.l_nav1.setText(self.t3[1])
    def cal(self):
        #日历控件 
        self.cal1 = QCalendarWidget(self)
        self.cal1.setMinimumSize(390, 280)
        self.cal1.setMaximumSize(390, 280)
        self.cal1.setVisible(False)
        date = self.cal1.selectedDate()
        self.l_nav1.setText(date.toString('yyyy-MM-dd dddd'))
        self.t_date = self.cal1.selectedDate().toString('yyyy-MM-dd')
        self.cal1.clicked.connect(self.showDate)
    def showDate(self):
        a = self.cal1.selectedDate().toString('yyyy-MM-dd dddd')
        self.l_nav1.setText(a)
        self.t_date = self.cal1.selectedDate().toString('yyyy-MM-dd')
        print(self.t_date)
    def show_cal(self):
        if self.btn_nav.text() == '选择日期':
            self.cal1.move(15 , 70)
            self.cal1.raise_()
            self.cal1.setVisible(True)
            self.l.setVisible(True)
            self.btn_nav.setText('确认')
            self.resize(500, 400)
        else:
            self.cal1.setVisible(False)
            self.l.setVisible(False)
            self.btn_nav.setText('选择日期')
            self.resize(500, 100)
            self.setGeometry(700, 400, 500, 100)
    def out_put(self):
        self.t1 = self.t
        self.t2 = self.t +'\n'+ self.t_date
        self.t3 = [self.t, self.t_date]
        self.close()
        

class dl_2(QWidget):
    def __init__(self, text, in_mod = False, in_data = None):
        super(dl_2, self).__init__()
        self.setWindowTitle(text)
        self.t = text
        self.setGeometry(700, 400, 500, 200)
        self.vlt = QVBoxLayout(self)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)
        
        self.btn_nav = QPushButton('选择起始日期')
        self.btn_nav.setFixedSize(140, 40)
        self.btn_nav.clicked.connect(self.show_cal1)
        
        self.l_nav1 = QLabel('')
        self.l_nav1.setMaximumSize(170 , 40)

        self.hlt.addWidget(self.btn_nav)
        self.hlt.addWidget(self.l_nav1)
        self.hlt.addStretch()
        
        self.hlt2 = QHBoxLayout()
        self.vlt.addLayout(self.hlt2)
        
        self.btn_nav2 = QPushButton('选择结束日期')
        self.btn_nav2.setFixedSize(140, 40)
        self.btn_nav2.clicked.connect(self.show_cal2)
        
        self.l_nav2 = QLabel('')
        self.l_nav2.setMaximumSize(170 , 40)

        self.btn = QPushButton('确认')
        self.btn.clicked.connect(self.out_put)

        self.hlt2.addWidget(self.btn_nav2)
        self.hlt2.addWidget(self.l_nav2)
        self.hlt2.addStretch()
        self.hlt2.addWidget(self.btn)
        
        self.l = QLabel()
        self.l.setFixedHeight(300)
        self.l.setVisible(False)
        self.vlt.addWidget(self.l)

        self.cal()
        if in_mod:
            self.t3 = in_data
            self.l_nav1.setText(self.t3[1])
            self.l_nav2.setText(self.t3[2])
    def cal(self):
        #日历控件 
        self.cal1 = QCalendarWidget(self)
        self.cal1.setMinimumSize(390, 280)
        self.cal1.setMaximumSize(390, 280)
        self.cal1.setVisible(False)
        date = self.cal1.selectedDate()
        self.l_nav1.setText(date.toString('yyyy-MM-dd dddd'))
        self.cal1.clicked.connect(self.showDate1)
        
        self.cal2 = QCalendarWidget(self)
        self.cal2.setMinimumSize(390, 280)
        self.cal2.setMaximumSize(390, 280)
        self.cal2.setVisible(False)
        date = self.cal2.selectedDate()
        self.l_nav2.setText(date.toString('yyyy-MM-dd dddd'))
        self.cal2.clicked.connect(self.showDate2)
        self.list_date = [self.cal1.selectedDate().toString('yyyy-MM-dd'),
                          self.cal2.selectedDate().toString('yyyy-MM-dd')]
    def showDate1(self):
        a = self.cal1.selectedDate().toString('yyyy-MM-dd dddd')
        self.l_nav1.setText(a)
        self.list_date[0] = self.cal1.selectedDate().toString('yyyy-MM-dd')
        print(self.list_date)
    def showDate2(self):
        b = self.cal2.selectedDate().toString('yyyy-MM-dd dddd')
        self.l_nav2.setText(b)
        self.list_date[1] = self.cal2.selectedDate().toString('yyyy-MM-dd')
        print(self.list_date)
    def show_cal1(self):
        if self.btn_nav.text() == '选择起始日期':
            self.cal1.move(15 , 80)
            self.cal1.raise_()
            self.cal1.setVisible(True)
            self.l.setVisible(True)
            self.btn_nav.setText('确认')
            self.resize(500, 500)
        else:
            self.cal1.setVisible(False)
            self.l.setVisible(False)
            self.btn_nav.setText('选择起始日期')
            self.resize(500, 200)
            self.setGeometry(700, 400, 500, 200)
    def show_cal2(self):
        if self.btn_nav2.text() == '选择结束日期':
            self.cal2.move(15 , 150)
            self.cal2.raise_()
            self.cal2.setVisible(True)
            self.l.setVisible(True)
            self.btn_nav2.setText('确认')
            self.resize(500, 500)
        else:
            self.cal2.setVisible(False)
            self.l.setVisible(False)
            self.btn_nav2.setText('选择结束日期')
            self.resize(500, 200)
            self.setGeometry(700, 400, 500, 200)
    def out_put(self):
        self.t1 = self.t
        self.t2 = self.t +'\n'+\
                  '起始时间：'+ self.list_date[0] +'\n'+\
                  '起始时间：'+ self.list_date[1]
        self.t3 = [self.t, self.list_date[0], self.list_date[1]]
        self.close()
        
class dl_3(QWidget):
    item_list = ['上半年','下半年', '全年']
    item_dict = {1:'上半年',2:'下半年', 3:'全年'}
    def __init__(self, text, in_mod = False, in_data = None):
        super(dl_3, self).__init__()
        self.setWindowTitle(text)
        self.t = text
        self.setGeometry(700, 400, 500, 200)
        self.vlt = QVBoxLayout(self)
        self.hlt = QHBoxLayout()
        self.vlt.addLayout(self.hlt)
        
        self.l_nav1 = QLabel('输入年份：')
        self.l_nav1.setMaximumSize(170 , 40)

        self.le = QLineEdit()
        


        self.hlt.addWidget(self.l_nav1)
        self.hlt.addWidget(self.le)
        self.hlt.addStretch()
        
        self.hlt2 = QHBoxLayout()
        self.vlt.addLayout(self.hlt2)
        
        self.cbx = QComboBox()
        self.cbx.addItems(self.item_list)
        
        self.l_nav2 = QLabel('选择季度：')
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

        if in_mod:
            self.t3 = in_data
            self.le.setText(self.t3[1])
            self.cbx.setCurrentIndex(int(self.t3[2]))
    def out_put(self):
        self.t1 = self.t
        self.t2 = self.t +'\n'+\
                  '年份：'+ self.le.text() +'\n'+\
                  '季度：'+ self.item_dict[self.cbx.currentIndex()+1]
        self.t3 = [self.t, self.le.text(), str(self.cbx.currentIndex()+1)]
        print(self.t1,self.t2,self.t3)
        self.close()
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    c=dl_3('jhierghi')
    c.show()
    sys.exit(app.exec_())