# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:10:41 2020

@author: wuqian
"""
from random import normalvariate

class model:
    def __init__(self, lenth, sigma = 1, w = [0.5, 1.5], r = 1):
        self.lenth = lenth
        self.sigma = sigma
        self.w = w
        self.r = r
    
    def generate_t_series(self):
        t = []
        for i in range(self.lenth):
            r = normalvariate(self.r/21, self.sigma)
            r = 1 + r/100
            t.append(r)
        self.t = t
        
    def test(self, time):
        A = []
        B = []
        C = []
        for i in range(time):
            self.generate_t_series()
            a0, b0 ,c0 = self.cycle()
            A.append(a0)
            B.append(b0)
            C.append(c0)
        print('max_b: ', sum(A)/len(A))
        print('净收益: ', sum(B)/len(B))
        print('套牢部分：', sum(C)/len(C))
        print('收益率', ((sum(B)/len(B))/(sum(A)/len(A)))*100, '%')
    
    def cycle(self):
        a = [99.85] #每日买入保留净值
        n = [1] #每日份额
        nav = [1] #每日净值
        for i in range(self.lenth):
            nav.append(nav[-1]*self.t[i])
        b = 100 #支出款项
        max_b = 100
        for i in range(self.lenth):
            #更新净值
            a = [j*self.t[i] for j in a]
            #若下跌则买入
            if self.t[i] < 1:
                #确认份额
                n0 = 1
                for m in range(i):
                    if self.t[i-m] < 1:
                        n0+=1
                    else:
                        break
                n.append(n0)
                #申购
                a.append(99.85*n0)
                b += 100*n0
                if max_b <= b:
                    max_b = b
            #持平
            elif self.t[i] == 1:
                a.append(0)
                n.append(0)
            #若上涨不买入
            elif self.t[i] > 1 :
                a.append(0)
                n.append(0)
                #前七天不卖出
                if i <= 7:
                    pass
                else:
                    #确认份额
                    n_max = 1
                    for m in range(i):
                        if self.t[i-m] > 1:
                            n_max += 1
                        else:
                            break
                    #对之前每个份额确认是否卖出
                    n0 = 0
                    for j in range(len(a)):
                        while n[j] !=0 :
                            if n0 == n_max:
                                break
                            #对比是否盈利
                            if (i - j) >= 6:
                                if (nav[i+1]/nav[j]-self.w[0]/100)>1:
                                    b -= a[j]/n[j]
                                    a[j] -= a[j]/n[j]
                                    n[j] -= 1
                                    n0 += 1
                                else:
                                    break
                            else:
                                if (nav[i+1]/nav[j]-self.w[1]/100)>1:
                                    b -= a[j]/n[j]
                                    a[j] -= a[j]/n[j]
                                    n[j] -= 1
                                    n0 += 1
                                else:
                                    break
                            
        return max_b, sum(a)-b, sum(a)
      
if __name__ == '__main__':
    m = model(21)
    m.test(2000)
