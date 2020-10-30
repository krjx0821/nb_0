# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 09:37:35 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from settings import data, fund_settings
d = data().data_all()
f = fund_settings()
dict_0, list_0 = f.data_init()

list_add1, list_add2, list_add3 = [], [], []
d_text = ''
dict_save = {}
s_text = ''
def getKey(dic,value):
    result = []
    for key in dic:
        if dic[key] == value:
            result.append(key)
    return result

class dl_fund(QWidget):
    global list_add1, list_add2, list_add3
    def __init__(self):
        super(dl_fund, self).__init__()
        self.setWindowTitle('单只基金选择')
        self.resize(900, 750)
        self.list_add = []
        self.dict_sel = {}
        self.df0 = None
        
        self.hlt = QHBoxLayout(self)
        self.left()
        self.mid()
        self.right()
        self.plot_tree1()
    def left(self):
        self.vlt1 = QSplitter(orientation=Qt.Vertical)
        self.vlt1.setFixedWidth(300)
        self.hlt.addWidget(self.vlt1)
        
        self.tree1 = QTreeWidget(self.vlt1)
        self.tree1.setHeaderLabel('可选基金类别：')
        
        self.l1 = QLabel('单只基金选择：\n输入Wind基金代码：')
        self.l1.setFixedHeight(45)
        
        self.le = QLineEdit()
        self.le.setFixedHeight(35)
        self.le.textChanged.connect(self.in_put)
                
        self.l3 = QLabel('')
        self.l3.setFixedHeight(17)
        
        self.btn = QPushButton('选择 >>')
        self.btn.setFixedHeight(35)
        self.btn.clicked.connect(self.sel)
        
        self.vlt1.addWidget(self.l1)
        self.vlt1.addWidget(self.le) 
        self.vlt1.addWidget(self.l3)
        self.vlt1.addWidget(self.btn)
    def mid(self):
        self.vlt = QVBoxLayout()
        self.hlt.addLayout(self.vlt)

        self.btn01 = QPushButton('>')
        self.btn01.setFixedSize(40, 40)
        self.btn01.clicked.connect(self.add)
        self.btn04 = QPushButton('<<')
        self.btn04.setFixedSize(40, 40)
        self.btn04.clicked.connect(self.clear_all)
        
        self.vlt.addStretch()
        self.vlt.addWidget(self.btn01)
        self.vlt.addStretch()
        self.vlt.addWidget(self.btn04)
        self.vlt.addStretch()
    def right(self):
        self.vlt2 = QVBoxLayout()
        self.hlt.addLayout(self.vlt2)
        
        self.tree2 = QTreeWidget()
        self.tree2.setColumnCount(2)
        self.tree2.setHeaderLabels(['已选基金：','数量'])
        self.tree2.setColumnWidth(0,200)
        
        self.tree3 = QTreeWidget()
        self.tree3.setColumnCount(3)
        self.tree3.setHeaderLabels(['基金名称', '基金代码',''])
        self.tree3.setColumnWidth(0,250)
        
        self.btn2 = QPushButton('确认')
        self.btn2.clicked.connect(self.end)
        
        self.vlt2.addWidget(self.tree2)
        self.vlt2.addWidget(self.tree3)
        self.vlt2.addWidget(self.btn2)

    def plot_tree1(self):
        global dict_save
        self.tree1.clear()
        self.root1 = QTreeWidgetItem(self.tree1)
        self.root1.setText(0,'海通基金分类')
        for i in dict_0.keys():
            child11 = QTreeWidgetItem(self.root1)
            child11.setText(0,i)
            child11.setCheckState(0, not Qt.CheckState) 
            for j in dict_0[i]:
                self.child12 = QTreeWidgetItem(child11)
                self.child12.setText(0,j)             
                self.child12.setCheckState(0, not Qt.CheckState) 
        self.root2 = QTreeWidgetItem(self.tree1)
        self.root2.setText(0,'自定义基金类别')
        for i in dict_save:
            self.child21 = QTreeWidgetItem(self.root2)
            self.child21.setText(0, i)
            self.child21.setCheckState(0, not Qt.CheckState)
        self.tree1.itemChanged.connect(self.onclick)
        self.onclick_flag = True
    def onclick(self,item,cloumn):
        if self.onclick_flag == True:
            if item.checkState(cloumn) == Qt.Checked:
                self.list_add.append(item.text(0))
                print("checked", item.text(0))
                self.list_add = list(set(self.list_add))
            if item.checkState(cloumn) == Qt.Unchecked:
                self.list_add.remove(item.text(0))
                print("unchecked", item.text(0))
                self.list_add = list(set(self.list_add))
        else:
            pass
        print(self.list_add)
    def add(self):
        global dict_save, list_add3
        list_temp = []
        self.dict_sel = {}
        for i in self.list_add:
            try:
                for j in dict_0[i]:
                    list_temp.append(j)
                self.dict_sel[i] = list_temp
                list_temp = []
            except:
                for j in list_0:
                    try:
                        print(j[i])
                        try:
                            self.dict_sel[getKey(dict_0, j)[0]].append(i)
                            self.dict_sel[getKey(dict_0, j)[0]] = list(set(self.dict_sel[getKey(dict_0, j)[0]]))
                        except:
                            self.dict_sel[getKey(dict_0, j)[0]] = [i]
                    except:
                        pass
        print(self.dict_sel)
        #构建树以及获取基金数据
        self.df0 = pd.DataFrame({'基金代码': [], '基金简称': [], '类别': []})
        self.tree2.clear()
        #类别基金
        for i in self.dict_sel.keys():
            self.root1 = QTreeWidgetItem(self.tree2)
            self.root1.setText(0, i)
            for j in self.dict_sel[i]:
                self.child1 = QTreeWidgetItem(self.root1)
                self.child1.setText(0, j)
                a = dict_0[i][j]
                l = str(len(a))
                self.child1.setText(1, l)
                self.df0 = pd.concat([self.df0, a])
        #自定义类别
        self.root2 = QTreeWidgetItem(self.tree2)
        self.root2.setText(0, '自定义基金类别')
        for i in self.list_add:
            try:
                a = dict_save[i]
                print(a)
                try:
                    a.insert(2, '类别', i)
                except:
                    pass
                list_add3.append(i)
                self.child2 = QTreeWidgetItem(self.root2)
                self.child2.setText(0, i)
                self.child2.setText(1, str(len(a)))
                self.df0 = pd.concat([self.df0, a])
            except:
                pass
        self.tree2.expandAll()
    
    def in_put(self, text):
        global d, d_text
        d_text = text
        try:
            a = d.loc[d['基金代码'] == text]['基金简称'].to_string().split('    ')
            self.l3.setText(a[1])
        except:
            if text == '':
                self.l3.setText('')
            else:
                self.l3.setText('该基金不存在')
    def sel(self):
        global list_add1, list_add2
        if (self.l3.text() == '') or (self.l3.text() == '该基金不存在') or (self.l3.text() == '该基金已存在'):
        #if list_add1 == [1]:
            print(self.l3.text())
        else:
            if d_text in list_add1:
                self.l3.setText('该基金已存在')
            else:
                print('fuck')
                list_add1.append(d_text)
                list_add2.append(self.l3.text())
                self.tree3.clear()
                root = QTreeWidgetItem(self.tree3)
                root.setText(0, '已选单只基金')
                for i in range(len(list_add1)):
                    child = QTreeWidgetItem(root)
                    child.setText(0, list_add2[i])
                    child.setText(1, list_add1[i])
                    btn = QPushButton('移除')
                    btn.setFixedWidth(50)
                    btn.clicked.connect(self.del_sgl)
                    self.tree3.setItemWidget(child, 2, btn)
                self.le.setText('')
                print(list_add1, list_add2)
                self.tree3.expandAll()
    def del_sgl(self):
        global list_add1, list_add2
        item = self.tree3.currentItem()
        list_add1.remove(item.text(1))
        list_add2.remove(item.text(0))
        print(list_add1, list_add2)
        item.parent().removeChild(item)
        
    def clear_all(self):
        global list_add1, list_add2
        list_add1, list_add2 = [], []
        self.dict_sel = {} 
        self.tree2.clear()
        self.tree3.clear()
        self.df0 = pd.DataFrame({'基金简称': [],
                            '基金代码': [],
                            '类别': []})
        
    def end(self):
        global list_add1, list_add2
        a = pd.DataFrame({'基金简称': list_add2,
                          '基金代码': list_add1})
        a['类别'] = '单只基金'
        try:
            self.df0 = pd.concat([self.df0, a])
        except:
            self.df0 = a
        self.hide()    

    def save_fund(self):
        global df0, dict_save, list_add3
        self.sf_flag = 0
        self.onclick_flag = False
        self.tree2.clear()
        self.df0 = self.df0.drop_duplicates(['基金代码'])
        exec('''global df_{0}
df_{0} = self.df0[['基金代码', '基金简称']]
dict_save[s_text] = df_{0}
print(df_{0})'''.format(str(self.sf_flag)))
        list_add3 = []
        self.list_add = []
        self.dict_sel = {}
        self.plot_tree1()
        self.sf_flag += 1
        print(dict_save)  

class dl_save_fund(QDialog):
    def __init__(self):
        super(dl_save_fund, self).__init__()
        self.setWindowTitle('命名自定义基金类别')
        self.resize(230, 150)
        
        self.vlt = QVBoxLayout(self)
        
        self.l = QLabel('命名自定义基金类别：')
        self.le = QLineEdit()
        self.btn = QPushButton('确认')
        self.btn.clicked.connect(self.p)
        
        self.vlt.addWidget(self.l)
        self.vlt.addWidget(self.le)
        self.vlt.addWidget(self.btn)
    def p(self):
        global s_text
        s_text = self.le.text()
        self.le.setText('')
        self.hide()
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w1 = dl_fund()
    w1.show()
    #w1.btn2.clicked.connect(w1.close)
    sys.exit(app.exec())
    