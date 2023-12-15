import random
import numpy as np
import pandas as pd

N = int(input())

def generate_matrix():
    matrix = []
    for _ in range(N):
        row = []
        for _ in range(N):
            value = np.random.normal(9, 5)
            row.append(abs(value))
        matrix.append(row)
    return matrix

matrix = generate_matrix()
print(matrix)

df = pd.DataFrame(matrix)
df.to_csv ("matrix", index= False, header = False)