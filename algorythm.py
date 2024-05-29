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

    def GkStrategy(self):
        # Преобразование списка списков P в numpy массив
        matrix = np.array(self.P)
        batchCount, processingCount = matrix.shape
        
        # Инициализация переменных для хранения максимальной суммы и значений колонок
        maxSum = 0
        maxCol_val = []
        maxBatches = []
    
        # Перебор значений для параметра k от 1 до 5
        for k in range(1, 6):
            selected_rows = [False] * batchCount  # Инициализация списка для отслеживания выбранных строк
            col_values = []  # Инициализация списка для хранения значений колонок
            batches = [None] * processingCount  # Инициализация списка для хранения номеров партий
            summa = 0  # Инициализация суммы для текущей итерации
    
            # Перебор колонок матрицы с шагом k
            for col in range(0, processingCount, k):
                # Создание и сортировка списка значений для текущей колонки
                col_elements = [(matrix[row][col], row) for row in range(batchCount) if not selected_rows[row]]
                col_elements.sort(reverse=True)
                
                # Если оставшихся колонок меньше, чем k, уменьшаем k до оставшегося количества колонок
                if (processingCount - col < k):
                    k = processingCount - col
    
                # Выбор k элементов из текущей колонки
                for i in range(k):
                    value = matrix[col_elements[i][1], col + i]
                    col_values.append(value)
                    batches[col + i] = col_elements[i][1]  # Запоминаем номер партии
                    selected_rows[col_elements[i][1]] = True
                    summa += value
    
            # Обновление максимальной суммы и соответствующих значений колонок
            if (maxSum < summa):
                maxSum = summa
                maxCol_val = col_values
                maxBatches = batches
    
        # Возвращение максимальной суммы, номеров дней, номеров оптимальных партий и исходной матрицы
        return maxSum, range(batchCount), maxBatches, self.P
    
    def TKGStrategy(self, nu):
        # Преобразование списка списков P в numpy массив
        matrix = np.array(self.P)
        batchCount, processingCount = matrix.shape
        results = []
    
        # Перебор значений для параметра k от 1 до (batchCount - nu + 2)
        for k in range(1, (batchCount - nu + 2)):
            selected_rows = [False] * batchCount  # Инициализация списка для отслеживания выбранных строк
            col_values = []  # Инициализация списка для хранения значений колонок
            batches = [None] * processingCount  # Инициализация списка для хранения номеров партий
            total_sum = 0  # Инициализация суммы для текущей итерации
    
            # Перебор колонок матрицы
            for col in range(processingCount):
                if col <= nu - 1:
                    col_elements = [(matrix[row][col], row) for row in range(batchCount) if not selected_rows[row]]
                    col_elements.sort()
                    value, remove_row = col_elements[k - 1]
                else:
                    max_value = float('-inf')
                    for row in range(batchCount):
                        if not selected_rows[row] and matrix[row][col] > max_value:
                            max_value = matrix[row][col]
                            remove_row = row
                    value = max_value
                selected_rows[remove_row] = True
                col_values.append(value)
                batches[col] = remove_row  # Запоминаем номер партии
                total_sum += value
    
            results.append((total_sum, col_values, batches))
    
        # Находим результат с максимальной суммой
        max_result = max(results, key=lambda x: x[0])
        summa = max_result[0]
        col_val = max_result[1]
        batches = max_result[2]
    
        # Возвращение максимальной суммы, номеров дней, номеров оптимальных партий и исходной матрицы
        return summa, range(batchCount), batches, self.P
    
    def CTGStrategy(self, nu):
        matrix = np.array(self.P)
        batchCount, processingCount = matrix.shape
    
        k = np.arange(1, nu)
        g = batchCount - 2 * nu + 2 * k + 1
        arrIndexes = g
    
        k = np.arange(nu, 2 * nu)
        g = batchCount + 2 * nu - 2 * k
        arrIndexes = np.append(arrIndexes, g)
    
        k = np.arange(2 * nu, batchCount + 1)
        g = batchCount - k + 1
        arrIndexes = np.append(arrIndexes, g) - 1
    
        sortedMatrix = matrix[matrix[:, 0].argsort()]
    
        arrBatchC = np.arange(batchCount)
        resArr = []
        batches = [None] * processingCount
        for i, j in zip(arrBatchC, arrIndexes):
            col_elements = [sortedMatrix[row, i] for row in range(batchCount)]
            resArr.append(col_elements[j])
            batches[i] = j
    
        summa = sum(resArr)
    
        return summa, range(batchCount), batches, self.P


    
    def calculate(self, _maximize=True, _algorythm=1, param  = 1):
        match _algorythm:
            case 1:
                return self.base_case(_maximize)
            case 2:
                return self.greedy_case(_maximize)
            case 3:
                return self.GkStrategy()
            case 4:
                return self.TKGStrategy(param)
            case 5:
                return self.CTGStrategy(param)
                
    
