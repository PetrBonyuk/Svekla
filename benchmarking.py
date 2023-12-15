import tkinter as tk
from tkinter import ttk
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

    res1, res2, res3, res4 = 0, 0, 0, 0

    for i in range(count):
        print(i)
        csv_generate.generate_test_data(
            "test", Nsize, V, mid1, disp1, mid2, disp2)
        w = alg.worker("test")
        res1 += w.calculate(_maximize=True, _algorythm=1)[0]
        res2 += w.calculate(_maximize=False, _algorythm=1)[0]
        res3 += w.calculate(_maximize=True, _algorythm=2)[0]
        res4 += w.calculate(_maximize=False, _algorythm=2)[0]

    res1 /= count
    res2 /= count
    res3 /= count
    res4 /= count

    results = [res1, res2, res3, res4]
    algorithms = ['Венгерский (макс)', 'Венгерский (мин)', 'Жадный', 'Бережливый']

    # Очистка предыдущего графика (если есть)
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Создание нового графика
    fig = Figure(figsize=(8, 5), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.bar(algorithms, results, color=['blue', 'orange', 'green', 'red'] )
    plot.set_xlabel('Алгоритмы')
    plot.set_ylabel('Среднее значение')
    plot.set_title('Сравнение результатов алгоритмов')

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
