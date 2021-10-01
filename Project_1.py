# Программа анализа .csv файлов

import tkinter as tk
from tkinter.scrolledtext import ScrolledText as st
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import os
import pandas as pd

# Создание главного окна
window=tk.Tk()
window.geometry("550x550")
window.title("Программа анализа .csv файлов")

# Создание меток вывода
label_00 = tk.Label(text = "Файл:")
label_00.grid(row=0, column=0, padx=10, pady=10, sticky="e")

label_01 = tk.Label(text = "")
label_01.grid(row=0, column=1, sticky="w")

label_10 = tk.Label(text = "Строк:")
label_10.grid(row=1, column=0, padx=10, pady=10, sticky="e")

label_11 = tk.Label(text = "")
label_11.grid(row=1, column=1, sticky="w")

label_20 = tk.Label(text = "Столбцов:")
label_20.grid(row=2, column=0, padx=10, pady=10, sticky="e")

label_21 = tk.Label(text = "")
label_21.grid(row=2, column=1, sticky="w")

# Создание текстового вывода c прокруткой
output_text = st(height = 20, width = 50)
output_text.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Диалог открытия файла
def do_dialog():
    my_dir = os.getcwd()
    name = fd.askopenfilename(initialdir=my_dir)
    return name

# Обработка .csv файла при помощи pandas
def pandas_read_csv(file_name):
    df = pd.read_csv(file_name, header=[0], sep=';')
    cnt_rows = df.shape[0]
    cnt_columns = df.shape[1]
    label_11['text'] = cnt_rows
    label_21['text'] = cnt_columns
    return df

# Выборка столбца в список
def get_column(df, column_ix):
    cnt_rows = df.shape[0]
    lst = []
    for i in range(cnt_rows):
        lst.append(df.iat[i,column_ix])
    return lst
    
# Если в этом поле имя, пусть вернет True    
def meet_name(field):
    checkfor = ['Вера', 'Анатолий', 'Мария', 'Артём', 'Алексей', 
        'Валерия', 'Наталья', 'Оксана', 'Галина', 'Марина',
        'Вероника', 'Виталий', 'Борис', 'Диана', 'Ева']
    for s in checkfor:
        if s in str(field): # Нашлось!
            return True
    # Ничего не совпало
    return False
    
# Если в этом списке многие элементы содержат имя, пусть вернет True    
def list_meet_name(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_name(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0.2:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio
    
    # Если в этом поле e-mail, пусть вернет True    
def meet_mail(field):
    checkfor = ['@']
    for s in checkfor:
        if s in str(field): # Нашлось!
            return True
    # Ничего не совпало
    return False
    
 # Если в этом списке многие элементы содержат mail, пусть вернет True    
def list_meet_mail(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_mail(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0.5:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio
    
 # Если в этом поле телефон, пусть вернет True    
def meet_telephone(field):
    checkfor = ['95', '( )']
    for s in checkfor:
        if s in str(field): # Нашлось!
            return True
    # Ничего не совпало
    return False
    
    # Если в этом списке многие элементы содержат телефон, пусть вернет True    
def list_meet_telephone(fields_list):
    counter_total = 0
    counter_meet = 0
    for list_item in fields_list:
        counter_total += 1
        if meet_telephone(list_item):
            counter_meet += 1
    # Конец подсчета
    ratio = counter_meet / counter_total
    if ratio > 0.5:
        return True, ratio
    # Не набралось нужного количества совпадений
    return False, ratio
    
# Пройти все столбцы    
def check_all_columns(df):
    columns_cnt = df.shape[1]
    for i in range(columns_cnt): # От 0 до columns_cnt-1
        lst = get_column(df, i)
        
        # Первый критерий
        result1 = list_meet_name(lst)
        if result1[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1)
                + " предположительно содержится имя." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result1[1]*100)
                + "%." + os.linesep + os.linesep)
            continue # Все нашли, можно идти к следующему столбцу
    
        # Второй критерий
        result = list_meet_mail(lst)
        if result[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1)
                + " предположительно содержится mail." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result[1]*100)
                + "%." + os.linesep)
            continue # Все нашли, можно идти к следующему столбцу
        
        # Третий критерий
        result = list_meet_telephone(lst)
        if result[0]:
            output_text.insert(tk.END, "В столбце " + str(i+1)
                + " предположительно содержится телефон." + os.linesep)
            output_text.insert(tk.END, "Процент совпадений " + "{:.2f}".format(result[1]*100)
                + "%." + os.linesep)
            continue # Все нашли, можно идти к следующему столбцу
        
        # Соответствия критериям не найдено
        output_text.insert(tk.END, "Предположений для столбца " + str(i+1)
            + " не найдено." + os.linesep + os.linesep)
    
#обработчик нажатия кнопки
def process_button():
    file_name = do_dialog()
    label_01['text'] = file_name
    df = pandas_read_csv(file_name)
    check_all_columns(df)
        
    mb.showinfo(title=None, message="Готово!")

#кнопка
button=tk.Button(window, text = "Прочитать файл", command=process_button)
button.grid(row=4, column=1)

#mainloop
window.mainloop()
