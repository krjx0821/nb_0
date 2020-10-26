# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:36:29 2020

@author: 19749
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
class data:
    def data11(self):
        a = pd.read_csv('指数股票型.csv', encoding = "gb2312").T.reset_index(drop=False)
        a.insert(2, '类别', '指数股票型')
        a.columns = ['基金代码', '基金简称', '类别']
        return a
    def data12(self):
        a = pd.read_csv('主动股票开放型.csv', encoding = "gb2312").T.reset_index(drop=False)
        a.insert(2, '类别', '主动股票开放型')
        a.columns = ['基金代码', '基金简称', '类别']
        return a
    def data21(self):
        a = pd.read_csv('主动混合封闭型.csv', encoding = "gb2312").T.reset_index(drop=False)
        a.insert(2, '类别', '主动混合封闭型')
        a.columns = ['基金代码', '基金简称', '类别']
        return a
    def data22(self):
        a = pd.read_csv('主动混合开放型.csv', encoding = "gb2312").T.reset_index(drop=False)
        a.insert(2, '类别', '主动混合开放型')
        a.columns = ['基金代码', '基金简称', '类别']
        return a
    def data_all(self):
        a = pd.DataFrame({'基金代码': [], '基金简称': [], '类别': []})
        for i in range(1,4):
            for j in range(1,4):
                try:
                    exec('global b\nb = self.data' + str(i) + str(j) + '()')
                    a = pd.concat([a, b])
                except:
                    pass
        return a
    
class f_settings:
    def __init__(self):
        self.l_f_z = []
        self.d_311 = {'国债': [],
                      '信用债': []}
        self.d_31 = {'固收类': self.d_311,
                     '权益类': ['持仓行业']}
        self.d_1 = {'流动性风险': [],
                    '市场风险': [],
                    '信用风险': []}
        self.d_2 = {'市场总体业绩': ['单位净值', '收益率', '最大回撤', '换手率'],
                    '公司业绩': [],
                    '各基金经理业绩': []}
        self.d_3 = {'绝对收益': self.d_31,
                    '相对收益': ['超额收益来源']}
        self.d = {'风险': self.d_1,
                  '业绩': self.d_2,
                  '归因': self.d_3,
                  '自定义模板': self.l_f_z}
    def data(self):
        return self.d
    def l_f(self):
        return self.l_f_z
    def l_f_update(self, name):
        self.l_f_z.append(name)
   
class fund_settings:
    dict_1 = {'指数股票型': data().data11(), 
          '主动股票开放型': data().data12()} 
    dict_2 = {'主动混合封闭型': data().data21(), 
          '主动混合开放型': data().data22()}
    def __init__(self):
        self.dict_0 = {'股票型基金': self.dict_1,
                  '混合型基金': self.dict_2}
        self.list_0 = [self.dict_1,
                  self.dict_2]
    def data_init(self):
        return self.dict_0, self.list_0
    
class init_l:
    l1 = ['', '基金简称', '基金代码', '类别']
    l2 = ['', '基金简称', '基金代码', '类别']
    l3 = ['', '', '', '']
    def data_init(self):
        return self.l1, self.l2, self.l3