# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 22:12:05 2023

@author: ipnnr
"""
import scipy
from scipy import linalg, optimize
import csv
import numpy as np

#rows, columns = scipy.optimize.linear_sum_assignment(cost_matrix=costs, maximize=False)

class worker(object):
    task=1          #task type
    N = 0
    P = []          #sugar amount matrix
    A = []          #initial sugar amount
    B = []          #degradation coefficient
    def __init__(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=';', dialect='excel')
            self.task = int(next(reader)[1])
            self.N = int(next(reader)[1])
            A_str = (next(reader))
            B_str = []
            for i in range(self.N-1):
                B_str.append(next(reader))
            self.A = [float(x.replace(',', '.')) for x in A_str]    
            
            self.B = [[float(xi.replace(',', '.')) for xi in x] for x in B_str]
            
            Pt = [self.A]
            for i in range(self.N-1):
                Pt.append(np.multiply(Pt[i],self.B[i]))
            
            #Transpose
            array = np.array(Pt)
            transposed_array = array.T
            self.P = transposed_array.tolist()
            if self.task==1:
                return
    
    
    def base_case(self, _maximize):
        rows, columns = scipy.optimize.linear_sum_assignment(cost_matrix=self.P, maximize=_maximize)
        res = [self.P[rows[i]][columns[i]] for i in range(self.N)]
        return sum(res), rows, columns, self.P
    
    def greedy_case(self, _maximize):
        if _maximize:
            max_sum = 0
            columns = list(range(self.N))
            rows = []
    
            for i in columns:
                max_elem = 0
                cur_j = (set(range(self.N)) - set(rows)).pop()
    
                for j in set(range(self.N)) - set(rows):
                    #print(self.P[j][i],":", max_elem)
                    if self.P[j][i] > max_elem:
                        cur_j = j
                        max_elem = self.P[j][i]
    
                rows.append(cur_j)
                max_sum += max_elem
    
            return max_sum, rows, columns, self.P
        else:
            min_sum = 0
            columns = list(range(self.N))
            rows = []
    
            for i in columns:
                min_elem = float('inf')
                cur_j = (set(range(self.N)) - set(rows)).pop()
    
                for j in set(range(self.N)) - set(rows):
                    if self.P[j][i] < min_elem:
                        cur_j = j
                        min_elem = self.P[j][i]
    
                rows.append(cur_j)
                min_sum += min_elem
    
            return min_sum, rows, columns, self.P
            
                    
                
    
    def calculate(self, _maximize=True, _algorythm=1):
        match _algorythm:
            case 1:
                return self.base_case(_maximize)
            case 2:
                return self.greedy_case(_maximize)
                
    
