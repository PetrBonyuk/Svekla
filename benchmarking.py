import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv_generate
import algorythm as alg


def run_experiment():
    count = int(count_entry.get())
    Nsize = int(Nsize_entry.get())
    V = float(V_entry.get())
    mid1 = float(mid1_entry.get())
    disp1 = float(disp1_entry.get())
    mid2 = float(mid2_entry.get())
    disp2 = float(disp2_entry.get())

    arrayres1 = []
    arrayres2 = []
    arrayres3 = []
    arrayres4 = []
    arrayres5 = []
    arrayres6 = []
    arrayres7 = []



    for N in range(1, Nsize + 1):
        print(N)
        res1, res2, res3, res4, res5, res6, res7 = 0, 0, 0, 0,0,0,0

        for i in range(count):
            csv_generate.generate_test_data(
                "test", N, V, mid1, disp1, mid2, disp2)
            w = alg.worker("test")
            res1 += w.calculate(_maximize=True, _algorythm=1)[0]
            res2 += w.calculate(_maximize=False, _algorythm=1)[0]
            res3 += w.calculate(_maximize=True, _algorythm=2)[0]
            res4 += w.calculate(_maximize=False, _algorythm=2)[0]
            res5 += w.calculate(_maximize=False, _algorythm=3)[0]
            res6 += w.calculate(_maximize=False, _algorythm=4)[0]
            res7 += w.calculate(_maximize=False, _algorythm=5)[0]

        arrayres1.append(res1 / count)
        arrayres2.append(res2 / count)
        arrayres3.append(res3 / count)
        arrayres4.append(res4 / count)
        arrayres5.append(res5 / count)
        arrayres6.append(res6 / count)
        arrayres7.append(res7 / count)


    for widget in result_frame.winfo_children():
        widget.destroy()

    # Создание графика
    fig = Figure(figsize=(12, 7), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    
    ax.plot(range(1, Nsize + 1), arrayres1, label='Венгерский (макс)')
    ax.plot(range(1, Nsize + 1), arrayres2, label='Венгерский (мин)')
    ax.plot(range(1, Nsize + 1), arrayres3, label='Жадный')
    ax.plot(range(1, Nsize + 1), arrayres4, label='Бережливый')
    ax.plot(range(1, Nsize + 1), arrayres5, label='Gk')
    ax.plot(range(1, Nsize + 1), arrayres6, label='TGK')
    ax.plot(range(1, Nsize + 1), arrayres7, label='CTG')

    # Настройка графика
    ax.set_xlabel('Размер матрицы')
    ax.set_ylabel('Среднее значение')
    ax.set_title('Динамика алгоритмов при разных размерах матрицы')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Создание основного окна
root = tk.Tk()
root.title("Графический интерфейс для алгоритмов")

# Создание и расположение элементов интерфейса
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Количество экспериментов:").grid(row=0, column=0, padx=5, pady=5)
count_entry = ttk.Entry(frame)
count_entry.grid(row=0, column=1, padx=5, pady=5)


ttk.Label(frame, text="Размер матрицы:").grid(row=1, column=0, padx=5, pady=5)
Nsize_entry = ttk.Entry(frame)
Nsize_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Дозаривание (V):").grid(row=2, column=0, padx=5, pady=5)
V_entry = ttk.Entry(frame)
V_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="mid1:").grid(row=3, column=0, padx=5, pady=5)
mid1_entry = ttk.Entry(frame)
mid1_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="disp1:").grid(row=4, column=0, padx=5, pady=5)
disp1_entry = ttk.Entry(frame)
disp1_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(frame, text="mid2:").grid(row=5, column=0, padx=5, pady=5)
mid2_entry = ttk.Entry(frame)
mid2_entry.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(frame, text="disp2:").grid(row=6, column=0, padx=5, pady=5)
disp2_entry = ttk.Entry(frame)
disp2_entry.grid(row=6, column=1, padx=5, pady=5)

ttk.Button(frame, text="Запустить эксперимент", command=run_experiment).grid(row=7, column=0, columnspan=2, pady=10)

result_frame = ttk.Frame(root, padding="10")
result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Запуск главного цикла
root.mainloop()
