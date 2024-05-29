import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import algorythm as alg  

alg_dict={"Венгерский алгоритм":1, "Жадный/Бережливый алгоритм":2, "Gk":3, "TKG":4, "CTG":5 }


class LinearOptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Optimization Solver")
        self.root.geometry('800x500')

        self.create_widgets()

    def create_widgets(self):
        # Frame для ввода файла
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(file_frame, text="Filename:").grid(row=0, column=0)
        self.filename_entry = ttk.Entry(file_frame, width=20)
        self.filename_entry.grid(row=0, column=1)

        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5)
        
        # Frame для выбора оптимизации
        optimize_frame = ttk.Frame(self.root, padding="10")
        optimize_frame.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Label(optimize_frame, text="Optimization:").grid(row=0, column=0)
        self.optimize_combobox = ttk.Combobox(optimize_frame, values=["Maximize", "Minimize"])
        self.optimize_combobox.grid(row=0, column=1, padx=5)
        self.optimize_combobox.current(0)

        # Frame для выбора алгоритма
        algorithm_frame = ttk.Frame(self.root, padding="10")
        algorithm_frame.grid(row=1, column=3, columnspan=2, pady=10)

        ttk.Label(algorithm_frame, text="Algorithm:").grid(row=0, column=0)
        self.algorithm_combobox = ttk.Combobox(algorithm_frame, values=["Венгерский алгоритм", "Жадный/Бережливый алгоритм", "Gk", "TKG", "CTG"])
        self.algorithm_combobox.grid(row=0, column=1)
        self.algorithm_combobox.current(0)

        # Кнопка для запуска расчетов
        ttk.Button(self.root, text="Calculate", command=self.calculate).grid(row=2, column=0, pady=10)

        # Frame для вывода результата
        result_frame = ttk.Frame(self.root, padding="10")
        result_frame.grid(row=3, column=0, columnspan=3, pady=10)

        ttk.Label(result_frame, text="Result:").grid(row=0, column=0)
        self.result_text = tk.Text(result_frame, height=3, width=60)
        self.result_text.grid(row=0, column=1)
        
        self.param = "1"
        ttk.Spinbox(result_frame, from_= 0,textvariable=self.param, to= 15).grid(row=1, column=2)
        

        # Frame для отображения матрицы
        matrix_frame = ttk.Frame(self.root, padding="10")
        matrix_frame.grid(row=4, column=0, columnspan=3, pady=10)

        self.matrix_table = Table(matrix_frame)
        self.matrix_table.grid(row=0, column=0)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, file_path)

    def calculate(self):
        filename = self.filename_entry.get()
        option = self.optimize_combobox.get()
        algorithm = self.algorithm_combobox.get()

        w = alg.worker(filename)
        res, rows, columns, P = w.calculate(option == "Maximize", _algorythm=alg_dict[algorithm], param = int(self.param))
        P = [["{:.3f}".format(xi) for xi in x] for x in P]
        for i in range(len(rows)):
            P[rows[i]][columns[i]] = "[" + P[rows[i]][columns[i]] + "]"

        result_text = f"{'Максимальный' if option == 'Maximize' else 'Минимальный'} объем сахара: {res}\nОптимальный план " \
                      f"с использованием {algorithm}: "

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result_text)

        self.matrix_table.update_table(P)


class Table(tk.Frame):
    """2D matrix of Entry widgets"""

    def __init__(self, parent):
        super().__init__(parent)

        self.cells = []
        self.values = []

    def update_table(self, data):
        for widget in self.winfo_children():
            widget.destroy()

        rows = len(data)
        columns = len(data[0])
        self.cells = []
        self.values = []

        for row in range(rows):
            for col in range(columns):
                var = tk.StringVar()
                cell = ttk.Entry(self, width=16, textvariable=var)
                cell.grid(row=row, column=col)
                self.cells.append(cell)
                self.values.append(var)
                var.set(data[row][col])


if __name__ == "__main__":
    root = tk.Tk()
    app = LinearOptimizationApp(root)
    root.mainloop()