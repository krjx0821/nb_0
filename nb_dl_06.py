# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 10:51:38 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import nb_dl_02

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

from WindPy import w
w.start()

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=70):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

class sub(QWidget):
    colour_list = ['red', 'orangered', 'chocolate',
              'orange', 'gold', 'yellow',
              'yellowgreen', 'palegreen', 'green',
              'springgreen','aqua','deepskyblue',
              'royalblue', 'blueviolet', 'violet',
              'hotpink', 'crimson']
    colour_dict = {}
    #data_dict = {}
    def __init__(self, text, code_list):
        super(sub,self).__init__()
        self.t = text
        self.l = code_list
        self.vlt0 = QVBoxLayout(self)
        
        self.hlt_top = QHBoxLayout()
        self.vlt0.addLayout(self.hlt_top)
        btn_para = QPushButton('选择参数')
        self.hlt_top.addWidget(btn_para)
        btn_para.clicked.connect(self.set_para)
        self.set_top()
        self.hlt_top.addStretch()
        
        self.hlt = QHBoxLayout()
        self.vlt0.addLayout(self.hlt)
        
        self.vlt = QVBoxLayout()
        self.hlt.addLayout(self.vlt)
        self.set_colour()
        self.set_checkbox()
        self.vlt.addStretch()
        
        self.gbx = QGroupBox(self)
        self.hlt.addWidget(self.gbx)
        self.gridlayout = QGridLayout(self.gbx)
    def set_top(self):
        if self.t == '单位净值（归一化）':
            self.l1 = QLabel('起始日期：')
            self.l2 = QLabel('')
            self.l3 = QLabel('结束日期：')
            self.l4 = QLabel('')
            self.hlt_top.addWidget(self.l1)
            self.hlt_top.addWidget(self.l2)
            self.hlt_top.addWidget(self.l3)
            self.hlt_top.addWidget(self.l4)
    def set_para(self):
        global dl
        if self.t == '单位净值（归一化）':
            dl = nb_dl_02.dl_2('设置参数')
            dl.btn.clicked.connect(self.get_para)
            dl.show()
            try:
                dl.exec_()
            except:
                pass
    def get_para(self):
        global dl
        if self.t == '单位净值（归一化）':
            self.para = dl.t3
        self.l2.setText(self.para[1])
        self.l4.setText(self.para[2])
        self.get_data()
        
    def get_data(self):
        self.data_dict = {}
        if self.t == '单位净值（归一化）':
            data = w.wsd(self.l, "nav", self.para[1], self.para[2])
            self.data_dict['time'] = data.Times
            for i in range(len(self.l)):
                n = data.Data[i][0]
                self.data_dict[self.l[i]] = [j/n for j in data.Data[i]]
        self.plot()
    def plot(self):
        print('plot')
        if self.t == '单位净值（归一化）':
            print('mid')
            self.F = MyFigure(width=3, height=2, dpi=70)
            self.F.axes = self.F.fig.add_subplot(111)
            for i in range(len(self.l)):
                if self.l_plot[i] == True:
                    x = self.data_dict['time']
                    y = self.data_dict[self.l[i]]
                    self.F.axes.plot(x, y, marker = 'o', label = self.l[i])
            self.F.axes.grid(True)
            self.F.axes.legend(loc = 1)
            self.gridlayout.addWidget(self.F, 0, 0)
        print('done')
    def set_colour(self):
        for i in range(len(self.l)):
            self.colour_dict[self.l[i]] = self.colour_list[(i*2) % len(self.colour_list)]
        self.l_plot = [True for i in self.l]
    def set_checkbox(self):
        for i in range(len(self.l)):
            exec('''self.cbx{0} = QPushButton(self.l[i])
self.cbx{0}.setObjectName(str(i))
self.cbx{0}.setMaximumWidth(150)
self.cbx{0}.setStyleSheet("background-color: rgb(29,191,151)")
self.cbx{0}.clicked.connect(self.on_click)
self.vlt.addWidget(self.cbx{0})'''.format(i))
    def on_click(self):
        index = int(self.sender().objectName())
        if self.l_plot[index]:
            self.l_plot[index] = False
            exec('self.cbx{0}.setStyleSheet("background-color: rgb(113,150,159)")'.format(str(index)))
            print(self.l_plot)
        else:
            self.l_plot[index] = True
            exec('self.cbx{0}.setStyleSheet("background-color: rgb(29,191,151)")'.format(str(index)))
            print(self.l_plot)
        self.plot()
       
class w_pic(QWidget):
    dict0 = {'单位净值': '单位净值（归一化）',
             '最大回撤': '最大回撤'}
    dict_stacked_layout = {}
    def __init__(self, fund_code, feature_list):
        super(w_pic,self).__init__()
        self.code = fund_code
        self.f_list = feature_list
        self.setWindowTitle("指标对比")
        self.resize(1100, 700)
        self.vlt0 = QVBoxLayout(self)
        #上层布局
        self.hlt0 = QHBoxLayout(self)
        self.vlt0.addLayout(self.hlt0)
        #下层布局
        widget = QWidget()
        self.stacked_layout = QStackedLayout()
        widget.setLayout(self.stacked_layout)
        self.vlt0.addWidget(widget)
        
        self.set_ui()
    def set_ui(self):
        l = []
        for i in self.f_list:
            if i[0] in self.dict0.keys():
                l.append(self.dict0[i[0]])
        for i in range(len(l)):
            btn = QPushButton(l[i])
            self.hlt0.addWidget(btn)
            btn.setObjectName(l[i])
            self.dict_stacked_layout[l[i]] = i
            btn.clicked.connect(self.btn_clicked)
            form = sub(l[i], self.code)
            self.stacked_layout.addWidget(form)
        self.hlt0.addStretch()
        
    def btn_clicked(self):
        i = self.dict_stacked_layout[self.sender().objectName()]
        self.stacked_layout.setCurrentIndex(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m1 = w_pic(['720001.OF','008314.OF'],[['单位净值'], ['最大回撤']])
    m1.show()
    sys.exit(app.exec())    
