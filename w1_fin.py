# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 10:51:38 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

from WindPy import w
w.start()

import math

dict_1 = {'GDP现价': 'M5567876', 
          '第一产业': 'M5567877', 
          '第二产业': 'M5567878', 
          '第三产业': 'M5567879'} 
dict_0 = {'国内生产总值': dict_1}
list_add = {}
w1_flag0 = True
w1_flag1 = True

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=70):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

class window1(QWidget):
    def __init__(self):
        super(window1,self).__init__()
        self.setWindowTitle("宏观经济指标")
        self.resize(1500, 900)
        self.vlt0 = QVBoxLayout(self)

        #下层布局
        self.hlt1 = QHBoxLayout(self)
        self.vlt0.addLayout(self.hlt1)
        #左侧选择栏        
        self.tree1 = QTreeWidget()
        self.tree1.setMaximumWidth(320)
        self.tree1.setColumnCount(2)
        self.tree1.setHeaderLabels(['可选指标','代码'])
        self.tree1.setMinimumWidth(270)
        self.tree1.setColumnWidth(0,200)
        self.root=QTreeWidgetItem(self.tree1)
        self.root.setText(0,"宏观经济指标")
        for i in dict_0.keys():
            child1 = QTreeWidgetItem(self.root)
            child1.setText(0,i)
            for j in dict_0[i]:
                self.child2 = QTreeWidgetItem(child1)
                self.child2.setText(0,j)
                self.child2.setText(1,dict_0[i][j])              
                self.child2.setCheckState(0, not Qt.CheckState)            
        self.tree1.expandAll()
        self.tree1.itemChanged.connect(self.onclick)
        
        self.btn1 = QPushButton('选择')
        self.btn1.setMinimumHeight(35)
        self.btn1.setMaximumHeight(35)
        self.btn1.clicked.connect(self.add)
        
        self.tree2 = QTreeWidget()
        self.tree2.setHeaderLabels(['已选指标：'])
        self.tree2.setMinimumWidth(270)
        self.tree2.setMaximumWidth(320)
        
        self.spl1 = QSplitter(self)
        self.spl1.addWidget(self.tree1)
        self.spl1.addWidget(self.btn1)
        self.spl1.addWidget(self.tree2)
        self.spl1.setOrientation(Qt.Vertical)
        self.hlt1.addWidget(self.spl1)

        
        self.btn2 = QPushButton()
        self.btn2.setText('<<')
        self.btn2.setMaximumHeight(50)
        self.btn2.setMaximumWidth(30)
        self.hlt1.addWidget(self.btn2)
        self.btn2.clicked.connect(self.sh1)
        
        #右侧布局
        self.vlt2 = QVBoxLayout()
        self.hlt1.addLayout(self.vlt2)
        #顶部选项框
        self.hlt2 = QHBoxLayout()
        self.vlt2.addLayout(self.hlt2)
        
        self.btn_cal1 = QPushButton('选择起始日期')
        self.btn_cal1.setMaximumSize(170, 40)
        self.btn_cal1.clicked.connect(self.show_cal1)
        self.hlt2.addWidget(self.btn_cal1)
        self.l1 = QLabel(self)
        self.hlt2.addWidget(self.l1)
        self.l1.setMaximumSize(170 , 40)
        
        self.btn_cal2 = QPushButton('选择结束日期')
        self.btn_cal2.setMaximumSize(170, 40)
        self.btn_cal2.clicked.connect(self.show_cal2)
        self.hlt2.addWidget(self.btn_cal2)
        self.l2 = QLabel(self)
        self.hlt2.addWidget(self.l2)
        self.l2.setMaximumSize(170 , 40)
        
        self.vlt3 = QVBoxLayout(self)
        self.hlt2.addLayout(self.vlt3)
        
        self.cbx1 = QCheckBox(self)
        self.vlt3.addWidget(self.cbx1)
        self.cbx1.setText('叠加')
        self.cbx1.setMaximumWidth(100)
        self.cbx1.setToolTip('将所选指标显示在同一张图表中')
        
        self.cbx2 = QCheckBox(self)
        self.vlt3.addWidget(self.cbx2)
        self.cbx2.setText('批量')
        self.cbx2.setMaximumWidth(100)
        self.cbx2.setToolTip('每个选中的指标分别输出对应图表')
        
        self.btn4 = QPushButton(self)
        self.hlt2.addWidget(self.btn4)
        self.btn4.setText('显示图像')
        self.btn4.setMaximumWidth(140)
        self.btn4.clicked.connect(self.getData)
        self.btn4.clicked.connect(self.plotFig)
                        
        self.btn_op2 = QPushButton()
        self.hlt2.addWidget(self.btn_op2)
        op2 = QGraphicsOpacityEffect()
        op2.setOpacity(0)
        self.btn_op2.setGraphicsEffect(op2)
        
        self.btn5 = QPushButton(self)
        self.hlt2.addWidget(self.btn5)
        self.btn5.setText('导出数据')
        self.btn5.setMaximumWidth(100)
        
        self.btn6 = QPushButton(self)
        self.hlt2.addWidget(self.btn6)
        self.btn6.setText('导出图像')
        self.btn6.setMaximumWidth(100)
        #图片显示区     
        self.gbx = QGroupBox(self)
        self.vlt2.addWidget(self.gbx)
        self.gridlayout = QGridLayout(self.gbx)
        #日历控件 
        self.cal1 = QCalendarWidget(self)
        self.cal1.setMinimumSize(390, 280)
        self.cal1.setMaximumSize(390, 280)
        self.cal1.setVisible(False)
        self.cal1.clicked.connect(self.showDate)
        date = self.cal1.selectedDate()
        self.l1.setText(date.toString('yyyy-MM-dd dddd'))
 
        self.cal2 = QCalendarWidget(self)
        self.cal2.setMinimumSize(390, 280)
        self.cal2.setMaximumSize(390, 280)
        self.cal2.setVisible(False)
        self.cal2.clicked.connect(self.showDate)
        date = self.cal2.selectedDate()
        self.l2.setText(date.toString('yyyy-MM-dd dddd'))
        
    def sh1(self):
        global w1_flag0
        if w1_flag0 == False:
            self.spl1.setHidden(False)
            self.btn2.setText('<<')
            w1_flag0 = True
        else:
            self.spl1.setHidden(True)
            self.btn2.setText('>>')
            w1_flag0 = False

    def onclick(self,item,cloumn):
        global list_add
        if item.checkState(cloumn) == Qt.Checked:
            print("checked", item.text(0),item.text(1))
            list_add[item.text(0)]=item.text(1)
        if item.checkState(cloumn) == Qt.Unchecked:
            del list_add[item.text(0)]
            print("unchecked", item.text(0))
        print(list_add)
    def add(self):
        global list_add
        self.tree2.clear()
        self.tree2.setColumnCount(1)
        for i in list_add:
            child1 = QTreeWidgetItem(self.tree2)
            child1.setText(0, i)
        self.tree2.expandAll()
        print(list_add)
        
    def show_cal1(self):
        if self.btn_cal1.text() == '选择起始日期':
            self.cal1.move(self.btn_cal1.geometry().x(), self.btn_cal1.geometry().y()+55)
            self.cal1.raise_()
            self.cal1.setVisible(True)
            self.btn_cal1.setText('确认')
        else:
            self.cal1.setVisible(False)
            self.btn_cal1.setText('选择起始日期')
    def show_cal2(self):
        if self.btn_cal2.text() == '选择结束日期':
            self.cal2.move(self.btn_cal2.geometry().x(), self.btn_cal2.geometry().y()+55)
            self.cal2.raise_()
            self.cal2.setVisible(True)
            self.btn_cal2.setText('确认')
        else:
            self.cal2.setVisible(False)
            self.btn_cal2.setText('选择结束日期')
    def showDate(self):
        global list_date
        a = self.cal1.selectedDate().toString('yyyy-MM-dd dddd')
        b = self.cal2.selectedDate().toString('yyyy-MM-dd dddd')
        self.l1.setText(a)
        self.l2.setText(b)
        list_date = [self.cal1.selectedDate().toString('yyyy-MM-dd'), 
                     self.cal2.selectedDate().toString('yyyy-MM-dd')]
        print(list_date)
        
    def getData(self):
        global list_name, list_code, list_date, data
        list_name = []
        list_code = []
        data = None
        for key in list_add:
            list_code.append(list_add[key])
            list_name.append(key)
        code = ','.join(list_code)
        print([code],list_name)
        data = w.edb(code,self.cal1.selectedDate().toString('yyyy-MM-dd'),
                     self.cal2.selectedDate().toString('yyyy-MM-dd'),'Fill=Previous')
        print(data)
    
    def plotFig(self):
        global list_name, data
        if self.cbx1.isChecked() == True:
            print('叠加')
            self.F = MyFigure(width=3, height=2, dpi=70)
            self.F.axes = self.F.fig.add_subplot(111)
            for i in range(len(list_name)):
                self.plot1(i)
            self.F.axes.legend(loc = 1)
            self.gridlayout.addWidget(self.F, 0, 0)
            flag = True
        else:
            flag = False
        if self.cbx2.isChecked() == True:
            print('批量')
            #批量
            if flag == False:
                lenth = math.ceil(math.sqrt(len(list_name)))
                print('lenth:'+str(lenth))
                for i in range(len(list_code)):
                    j = i // lenth
                    k = i - j*lenth
                    self.plot2(i, j, k)
                
            else:
                lenth = math.ceil(math.sqrt(len(list_name)))
                print('lenth:'+str(lenth))
                for i in range(len(list_code)):
                    j = (i+1) // lenth
                    k = (i+1) - j*lenth
                    self.plot2(i, j, k)
    def plot1(self, i):
        global list_name, data
        t = data.Times
        s = data.Data[i]
        self.F.axes.plot(t, s, marker = 'o', label = list_name[i])
    def plot2(self, i, j, k):
        global list_name, data
        self.f = MyFigure(width=3, height=2, dpi=70)
        self.f.axes = self.f.fig.add_subplot(111)
        t = data.Times
        s = data.Data[i]
        self.f.axes.plot(t, s, marker = 'o')
        self.f.axes.set_title(list_name[i])
        self.gridlayout.addWidget(self.f, j, k)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m1 = window1()
    m1.show()
    sys.exit(app.exec())    
