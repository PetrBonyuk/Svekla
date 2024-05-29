# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:07:44 2023

@author: ipnnr
"""

import csv
import numpy as np

def generate_test_data(filename, N, V, mid1 = 1.2, disp1 = 0.2, mid2=0.8, disp2=0.2):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

      
        writer.writerow(['type', '1'])

        # Записываем размер матрицы
        writer.writerow(['N', str(N)])

        # Генерируем случайный вектор из N элементов
        vector = np.random.normal(10, 1, N)  # Множим на 10 для получения значений в диапазоне [0, 10)
        writer.writerow(['{:.3f}'.format(x) for x in vector])

        # Генерируем коэффициенты в соответствии с нормальным распределением
        for i in range(N - 1):
            if i < V:
                coefficients = np.abs(np.random.normal(1.2, 0.2, N))
            else:
                coefficients = np.abs(np.random.normal(0.8, 0.2, N))
            writer.writerow(['{:.3f}'.format(x) for x in coefficients])

# Пример использования:
#generate_test_data('test_data.csv', N=10, V=4)
