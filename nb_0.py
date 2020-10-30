# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:14:15 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import nb_dl_0, nb_dl_02, nb_dl_03, nb_dl_04, nb_dl_05, nb_dl_06, settings, math
from settings import pandasModel, f_settings, init_l
import pandas as pd
from WindPy import w
w.start()
dict_f_z_l1 = {}
dict_f_z_l2 = {}
dict_f_z_l3 = {}
f = f_settings()
d_f = f.data()
l_f_z = f.l_f()
print(d_f)
#列标签
l00 = init_l()
l1,l2,l3 = l00.data_init()
df = pd.DataFrame({'': [],
                   '基金简称': [],
                   '基金代码': [],
                   '类别': []})
dl_f = None
flag_dl_fund = True
dl_add_row = None
num_save_f_z = 0
class window2(QWidget):
    def __init__(self):
        super(window2,self).__init__()
        self.load_f()
        self.setWindowTitle("同业分析")
        self.resize(1700, 800)
        self.vlt0 = QVBoxLayout(self)
        self.sub_top()
        self.mainWindow()
        self.set_contextMenu()
    def sub_top(self):
        self.hlt1 = QHBoxLayout()
        self.vlt0.addLayout(self.hlt1)
        
        self.btn11 = QPushButton('获取数据')
        self.btn11.clicked.connect(self.get_data)
        self.btn12 = QPushButton('隐藏指标参数')
        self.btn12.clicked.connect(self.para_hide)
        self.btn13 = QPushButton('修改指标参数')
        self.btn13.clicked.connect(self.para_mod)
        self.btn16 = QPushButton('导出数据')
        self.btn16.clicked.connect(self.to_csv)
        
        self.line1 = QFrame(self)
        self.line1.setFrameShape(QFrame.VLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line2 = QFrame(self)
        self.line2.setFrameShape(QFrame.VLine)
        self.line2.setFrameShadow(QFrame.Sunken)

        self.vlt_out = QVBoxLayout()
        self.l_out = QLabel('     保存模板  ')
        self.btn14 = QPushButton('保存基金类别模板')
        self.btn14.clicked.connect(self.save_fund)
        self.btn15 = QPushButton('保存指标模板')
        self.btn15.clicked.connect(self.pre_save_f_z)
        self.vlt_out.addWidget(self.l_out)
        self.vlt_out.addWidget(self.btn14)
        self.vlt_out.addWidget(self.btn15)
        
        self.hlt1.addWidget(self.btn11)
        self.hlt1.addWidget(self.btn12)
        self.hlt1.addWidget(self.btn13)
        self.hlt1.addWidget(self.line1)
        self.hlt1.addLayout(self.vlt_out)
        self.hlt1.addWidget(self.line2)
        self.hlt1.addWidget(self.btn16)
        self.hlt1.addStretch()
    def mainWindow(self):
        self.hlt_main = QHBoxLayout()
        self.vlt0.addLayout(self.hlt_main)
        self.leftBar()
        self.tableView()
    def leftBar(self):
        self.spl_left = QSplitter(Qt.Vertical)
        self.spl_left.setMaximumWidth(370)
        self.spl_left.setMinimumWidth(360)
        self.hlt_main.addWidget(self.spl_left)
        self.featureBox()
        self.fundBox()
    def featureBox(self):
        self.tree1 = QTreeWidget(self.spl_left)
        self.tree1.setHeaderLabel('指标列表')
        self.plot_tree1()
    def fundBox(self):
        self.tree2 = QTreeWidget(self.spl_left)
        self.tree2.setHeaderLabel('已选基金')
        
        self.btn_fundBox = QPushButton('展开选择栏')
        self.btn_fundBox.setMaximumHeight(40)
        self.btn_fundBox.clicked.connect(self.fund_sel)
        
        self.spl_left.addWidget(self.btn_fundBox)
    def tableView(self):
        self.model = pandasModel(df)
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.ExtendedSelection)
        self.hlt_main.addWidget(self.view)
    def set_contextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
    
    def show_menu(self, point):
        menu = QMenu(self)
        
        del_col = QAction("删除所选列", menu)
        del_col.triggered.connect(self.del_col)
        
        del_row = QAction("删除所选行", menu)
        del_row.triggered.connect(self.del_row)
        
        add_row = QAction("增加基金行", menu)
        add_row.triggered.connect(self.add_row)
        
        rank = QMenu("列数据处理")
        rank_col = QAction("依照所选列排序/筛选", menu)
        rank_col.triggered.connect(self.pre_rank)
        pic = QAction("依照所选列绘图", menu)
        pic.triggered.connect(self.pic)
        rank.addAction(rank_col)
        rank.addAction(pic)
                
        fund_detail = QAction("基金详情", menu)
        fund_detail.triggered.connect(self.fund_dt)
        
        menu.addAction(del_col)
        menu.addAction(del_row)
        menu.addSeparator()
        menu.addAction(add_row)
        menu.addSeparator()
        menu.addMenu(rank)
        menu.addSeparator()
        menu.addAction(fund_detail)
        
        dest_point = self.mapToGlobal(point)
        menu.exec_(dest_point)
    def pre_rank(self):
        global dl_rank
        dl_rank = nb_dl_05.ranking()
        dl_rank.show()
        try:
            dl_rank.exec_()
        except:
            pass
        dl_rank.btn.clicked.connect(self._rank)
    def _rank(self):
        #获取所选列数
        global df, l1, l2, l3, dl_rank
        index= self.view.selectionModel().selectedIndexes()
        list1 = list(set([i.column() for i in index]))
        list1.sort(key=int, reverse=False)
        for i in list1:
            if i >= 4:
                col_index = i
                break
        #排序
        p = dl_rank.proportion
        ascend_flag = (p < 0)
        if dl_rank.ckeck_state:
            df = df.sort_values(by=['类别', l2[col_index]] , axis=0 , ascending = ascend_flag)
        else:
            df = df.sort_values(by=l2[col_index] , axis=0 , ascending = ascend_flag)
        #选取
        if dl_rank.ckeck_state:
            l = list(set(df['类别'].tolist()))
            df0 = df[df['类别']==l[0]]
            df0 = df0.iloc[:math.ceil((len(df0)*abs(p)/100))]
            for i in range(1,len(l)):
                df_temp = df[df['类别']==l[i]]
                df_temp = df_temp.iloc[:math.ceil((len(df_temp)*abs(p)/100))]
                df0 = pd.concat([df0, df_temp])
            df = df0
        else:
            df = df.iloc[:int(len(df)*abs(p)/100)]
        df[''] = list(range(len(df)))
        df.reset_index(drop=True, inplace=True)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
    def del_col(self):
        global df, l1, l2, l3
        index= self.view.selectionModel().selectedIndexes()
        list1 = list(set([i.column() for i in index]))
        list1.sort(key=int, reverse=True)
        print('list1: ', list1)
        for i in list1:
            if i not in [0,1,2,3]:
                df = df.drop(columns = list(df)[i], axis = 1)
                del l1[i], l2[i], l3[i]
        df.reset_index(drop=True, inplace=True)
        print(df)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
        print(l1,l2,l3)
    def del_row(self):
        global df
        index= self.view.selectionModel().selectedIndexes()
        list1 = list(set([i.row() for i in index]))
        list1.sort(key=int, reverse=True)
        print('list1: ', list1)
        for i in list1:
            df = df.drop(index = i)
        df[''] = range(len(df))
        df.reset_index(drop=True, inplace=True)
        print(df)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
    def add_row(self):
        global dl_add_row
        dl_add_row = nb_dl_0.dl_fund()
        dl_add_row.show()
        dl_add_row.btn2.clicked.connect(self.add_row_show)
        try:
            dl_add_row.exec_()
        except:
            pass
    def add_row_show(self):
        global df, dl_add_row
        df0 = dl_add_row.df0
        print(df)
        df = pd.concat([df, df0])
        df[''] = range(0,len(df))
        df.reset_index(drop=True, inplace=True)
        print(df)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
        
        self.plot_tree2()
    def pic(self):
        global df, l1, l2, l3, dl_pic
        index= self.view.selectionModel().selectedIndexes()
        list1 = list(set([i.column() for i in index]))
        list1.sort(key=int, reverse=False)
        l_pic = []
        for i in list1:
            if i >= 4:
                l_pic.append(l3[i])
        list2 = list(set([i.row() for i in index]))
        list2.sort(key=int, reverse=False)
        list2 = df.iloc[list2]['基金代码'].tolist()
        print(l_pic, list2)
        dl_pic = nb_dl_06.w_pic(list2, l_pic)
        dl_pic.show()
        try:
            dl_pic.exec_()
        except:
            pass
    def fund_dt(self):
        pass
    
    def f(self):
        text = self.sender().objectName()
        global dl
        if text in l_f_z:
            print(text)
            self.f_add_z(text)
        else:
            if text == '单位净值':
                dl = nb_dl_02.dl_1(text)
            elif (text == '收益率') or (text == '最大回撤'):
                dl = nb_dl_02.dl_2(text)
            elif text == '换手率':
                dl = nb_dl_02.dl_3(text)
            dl.show()
            try:
                dl.exec_()
            except:
                pass
            dl.btn.clicked.connect(self.f_add)
    def f_add(self):
        global dl, l1, l2, l3
        l1.append(dl.t1)
        l2.append(dl.t2)
        l3.append(dl.t3)
        print(l1,l2,l3)
        self.set_col()
    def set_col(self):
        global l1, l2, df
        flag = False
        if self.btn12.text() == '显示指标参数':
            df.columns = l2[:df.shape[1]]
            flag = True
        for i in l2:
            if i not in df.columns.tolist():
                df[i] = None
        for i in df.columns.tolist():
            if i not in l2:
                df = df.drop(columns = i, axis = 1)
        #print('l2:', l2, '\ncolumn:', df.columns.tolist(), '\nl1:', l1)
        if flag:
            df.columns = l1
        print(df)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
    def f_add_z(self, text):
        global l1, l2, l3
        for i in range(len(dict_f_z_l1[text])):
            if dict_f_z_l2[text][i] not in l2:
                l1.append(dict_f_z_l1[text][i])
                l2.append(dict_f_z_l2[text][i])
                l3.append(dict_f_z_l3[text][i])
        self.set_col()
    def pre_save_f_z(self):
        dl_f_z = nb_dl_04.dl_save_f()
        dl_f_z.show()
        dl_f_z.btn.clicked.connect(self.save_f_z)
        dl_f_z.exec_()
    def save_f_z(self):
        global l1, l2, l3, num_save_f_z
        i = nb_dl_04.f_name
        f.l_f_update(i)
        fi = open(i + ".txt", "w")
        print('ll1 =', l1, file=fi)
        print('ll2 =', l2, file=fi)
        print('ll3 =', l3, file=fi)
        fi.close()
        exec('''l1_{0} = l1.copy()
l2_{0} = l2.copy()
l3_{0} = l3.copy()
dict_f_z_l1[i] = l1_{0}
dict_f_z_l2[i] = l2_{0}
dict_f_z_l3[i] = l3_{0}'''.format(str(num_save_f_z)))
        num_save_f_z += 1
        self.plot_tree1()
    def load_f(self):
        import os
        #path = os.path.abspath('..')+'\w.bat'
        path = 'C:\\Users/19749/Desktop/Qt5/半成品/演示/w.bat'
        os.system(path)
        fi = open('LIST.TXT')
        a = fi.read()
        filename_list = a.split('\n')
        fi.close()
        for title in filename_list:
            if '.txt' in title:
                m = open(title)
                m_r = m.read()
                print(m_r)
                exec('''ll1,ll2,ll3 = [],[],[]
'''+m_r+'''
dict_f_z_l1[title] = ll1
dict_f_z_l2[title] = ll2
dict_f_z_l3[title] = ll3
f.l_f_update(title)''')
        print(dict_f_z_l1)
        
    def get_data(self):
        global l3
        code_list = df['基金代码'].tolist()
        code_str = ','.join(code_list)
        if self.btn12.text() == '显示指标参数':
            self.para_hide()
        for i in range(4, len(l3)):
            if l3[i][0] == '单位净值':
                d = w.wsd(code_str, "nav", l3[i][1], l3[i][1])
                df[l2[i]] = d.Data[0]
            elif l3[i][0] == '收益率':
                d1 = w.wsd(code_str, "nav", l3[i][1], l3[i][1]).Data[0]
                d2 = w.wsd(code_str, "nav", l3[i][2], l3[i][2]).Data[0]
                d = [(i-j)/j for i, j in zip(d2, d1)]
                df[l2[i]] = d
            elif l3[i][0] == '最大回撤':
                d = w.wsd(code_str, "risk_maxdownside", l3[i][1], l3[i][2])
                print(d.Data)
                df[l2[i]] = [i[0] for i in d.Data]
            elif l3[i][0] == '换手率':
                d = w.wsd(code_str,'style_rpt_turn', '2020-07-27',
                          '2020-07-27', 'year={0};Intervaltype={1}'.format(l3[i][1], l3[i][2]))
                print(d.Data)
                df[l2[i]] = d.Data[0]
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
    def para_hide(self):
        global l1, l2, df
        if self.btn12.text() == '隐藏指标参数':
            df.columns = l1
            self.btn12.setText('显示指标参数')
            self.model = pandasModel(df)
            self.view.setModel(self.model)
            self.view.updateEditorData()
        else:
            df.columns = l2
            self.btn12.setText('隐藏指标参数')
            self.model = pandasModel(df)
            self.view.setModel(self.model)
            self.view.updateEditorData()
    def para_mod(self):
        global l1, l2, l3, dl_para
        print('l1:',l1,'l2:',l2,'l3:',l3)
        dl_para = nb_dl_03.window(l1, l2, l3)
        dl_para.show()
        dl_para.btn3.clicked.connect(self.para_change)
        dl_para.exec_()
    def para_change(self):
        global l1, l2, l3, dl_para
        l1 = dl_para.l1
        l2 = dl_para.l2
        l3 = dl_para.l3
        print(l1, l2, l3)
        self.set_col()
    
    def fund_sel(self):
        global dl_f, flag_dl_fund
        if flag_dl_fund:
            flag_dl_fund = False
            dl_f = nb_dl_0.dl_fund()
            dl_f.show()
            dl_f.btn2.clicked.connect(self.fund_show)
            try:
                dl_f.exec_()
            except:
                pass
        else:
            dl_f.show()
    def fund_show(self):
        global df, dl_f
        df0 = dl_f.df0
        df = pd.DataFrame(data = None, columns = df.columns.tolist())
        print(df)

        df = pd.concat([df, df0])
        df.drop_duplicates(subset=['基金代码'], keep='last', inplace=True)
        df[''] = range(0,len(df))
        df.reset_index(drop=True, inplace=True)
        print(df)
        self.model = pandasModel(df)
        self.view.setModel(self.model)
        self.view.updateEditorData()
        
        self.plot_tree2()
        
    def plot_tree2(self):
        global dl_f, dl_add_row
        self.tree2.clear()
        #类别基金
        try:
            dict_sel = dl_f.dict_sel
            for i in dict_sel.keys():
                self.root1 = QTreeWidgetItem(self.tree2)
                self.root1.setText(0, i)
                for j in dict_sel[i]:
                    self.child1 = QTreeWidgetItem(self.root1)
                    self.child1.setText(0, j)
        except:
            pass
        try:
            dict_sel2 = dl_add_row.dict_sel
            for i in dict_sel2.keys():
                self.root1 = QTreeWidgetItem(self.tree2)
                self.root1.setText(0, i)
                for j in dict_sel2[i]:
                    self.child1 = QTreeWidgetItem(self.root1)
                    self.child1.setText(0, j)
        except:
            pass
        #自定义类别
        self.root2 = QTreeWidgetItem(self.tree2)
        self.root2.setText(0, '自定义基金类别')
        for i in nb_dl_0.list_add3:
            self.child2 = QTreeWidgetItem(self.root2)
            self.child2.setText(0, i)
        self.root3 = QTreeWidgetItem(self.tree2)
        self.root3.setText(0, '单只基金')
        for i in nb_dl_0.list_add2:
            self.child3 = QTreeWidgetItem(self.root3)
            self.child3.setText(0, i)
        self.tree2.expandAll()
    def plot_tree1(self):
        self.tree1.clear()
        self.plot_tree1_cycle(d_f, self.tree1)
    def plot_tree1_cycle(self, d, rootBase):
        for i in d.keys():
            root = QTreeWidgetItem(rootBase)
            root.setText(0, i)
            if type(d[i]) == type([]):
                for j in d[i]:
                    child = QTreeWidgetItem(root)
                    child.setText(0, j)
                    btn = QPushButton(j)
                    btn.setObjectName(j)
                    btn.setMaximumWidth(140)
                    self.tree1.setItemWidget(child, 0, btn)
                    btn.clicked.connect(self.f)
            else:
                self.plot_tree1_cycle(d[i], root)
    def save_fund(self):
        dl_save_fund = nb_dl_0.dl_save_fund()
        dl_save_fund.btn.clicked.connect(self.save_fund2)
        dl_save_fund.show()
        dl_save_fund.exec_()
    def save_fund2(self):
        global dl_f
        dl_f.save_fund()
        
    def to_csv(self):
        global dl_save_csv
        dl_save_csv = nb_dl_04.dl_save_csv()
        dl_save_csv.show()
        dl_save_csv.btn.clicked.connect(self.save_csv)
        dl_save_csv.exce_()
    def save_csv(self):
        global df
        path = nb_dl_04.path_text
        print('path: ', path)
        df.to_csv(path, header=True, index=True, encoding = "gb2312")
        print('done')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w2 = window2()
    w2.show()
    sys.exit(app.exec_())
