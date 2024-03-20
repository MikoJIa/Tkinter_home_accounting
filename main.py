import tkinter as tk
import tkinter.ttk as ttk
from tkinter import BOTH
import sqlite3


# Теперь создадим класс главного окна и унаследуемся от модуля Tkinter
# Frame - это контейнер, который в свою очередь служит для организации обьктов и виджетов внутри окна.
class Main(tk.Frame):
    def __init__(self, root):
        # возмём метод init у базового класса Frame и передадим в него аргумент root
        # метод super() отыскивает базовый класс у класса Main и возвращает его, а дальше идёт обращение к методу init
        # этого найденного класса
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # создадим функции в которой будем хранить и инициализировать все обьекты нашего графического интерфейса
    # вызывать функцию будем через конструктор класса
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='artboard.png')
        btn_open_window_child = tk.Button(toolbar, text='Добавить', bg='#d7d8e0', command=self.open_window_child,
                                          compound=tk.TOP, image=self.add_img)
        btn_open_window_child.pack(side=tk.LEFT)

        self.add_img2 = tk.PhotoImage(file='deal_done.png')

        btn_open = tk.Button(toolbar, text='Работник', bg='#d7d8e0', compound=tk.TOP, image=self.add_img2)
        btn_open.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='pencil_icon_261870.png')
        btn_edit = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', compound=tk.TOP,
                             image=self.update_img, command=self.open_update)
        btn_edit.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='trash_icon_246188.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', compound=tk.TOP,
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.RIGHT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', compound=tk.TOP,
                               image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.RIGHT)

        self.return_img = tk.PhotoImage(file='return_to_back.png')
        btn_return = tk.Button(toolbar, text='Главная страница', bg='#d7d8e0', compound=tk.TOP,
                               image=self.return_img, command=self.view_records)
        btn_return.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('id', 'description', 'costs', 'total'), height=19, show='headings')

        # Теперь добавим параметры колонкам
        self.tree.column('id', width=160, anchor=tk.CENTER)
        self.tree.column('description', width=160, anchor=tk.CENTER)
        self.tree.column('costs', width=160, anchor=tk.CENTER)
        self.tree.column('total', width=160, anchor=tk.CENTER)

        # теперь мы дадим привычные названия колонкам
        self.tree.heading('id', text='id')
        self.tree.heading('description', text='Описание')
        self.tree.heading('costs', text='доходы\расходы')
        self.tree.heading('total', text='сумма')

        self.tree.pack(side=tk.LEFT)

        scroll_bar = tk.Scrollbar(self, command=self.tree.yview)
        scroll_bar.pack(fill=tk.Y, side=tk.LEFT)
        self.tree.configure(yscrollcommand=scroll_bar.set)

    # Информация которая будет отоброжаться на главной странице
    def records(self, description, costs, total):
        self.db.add_information(description, costs, total)
        self.view_records()

    # Напишем функцию которая буде редактировать наши записи в БД
    def update_records(self, description, costs, total):
        self.db.cursor.execute('''UPDATE accounting SET description=?, costs=?, total=? WHERE id=?''',
                               (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
                                    # id мы найдём через метод set  с двумя аргументами: первый- selection()[0],
                                    # второй - column '#1'
        self.db.conn.commit()
        # что бы отоброзить обновлённую информацию в главном окне, необходимо вызвать функцию view_records
        self.view_records()

    def delete_records(self):
        for item_sel in self.tree.selection():
            self.db.cursor.execute('''DELETE FROM accounting WHERE id=?''', (self.tree.set(item_sel, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = '%' + description + '%'
        self.db.cursor.execute('''SELECT * FROM accounting WHERE description LIKE ?''',
                               (description, ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]


    # эта функция будет извлекать информацию из таблицы accounting
    def view_records(self):
        self.db.cursor.execute('''SELECT * FROM accounting''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def open_window_child(self):
        Child()

    def open_update(self):
        Update()

    def open_search(self):
        Search()


# Создадим дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        # вызов нашей функции init_child()
        self.init_child()
        self.main_view = app

    def init_child(self):
        self.title('Добавить доходы\рассходы')
        self.geometry('350x300+470+350')
        self.resizable(False, False)

        desc_leb = ttk.Label(self, text='Назначение')
        desc_leb.place(relx=0.5, rely=0.1)
        select_income_expenses_leb = ttk.Label(self, text='расходы\доходы')
        select_income_expenses_leb.place(relx=0.55, rely=0.2)
        summ_leb = ttk.Label(self, text='Сумма')
        summ_leb.place(relx=0.5, rely=0.3)

        # создаём наши виджиты Entry для ввода параметров
        self.entry_desc = ttk.Entry(self)
        self.entry_desc.place(relx=0.1, rely=0.1)

        self.entry_cash = ttk.Entry(self)
        self.entry_cash.place(relx=0.1, rely=0.2)

        self.entry_summ = ttk.Entry(self)
        self.entry_summ.place(relx=0.1, rely=0.3)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(relx=0.1, rely=0.2)

        # Кнопки для закрытие окна и для сохранения в базе
        # destroy() - метод для закрытие окна
        btn_close = ttk.Button(self, text='Закрыть окно', command=self.destroy)
        btn_close.place(relx=0.1, rely=0.6)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(relx=0.65, rely=0.6)
        # сделаем так что бы наша кнопка срабатывало при нажатии правой кнопки мыши
        self.btn_add.bind('<Button-1>', lambda event: self.main_view.records(self.entry_desc.get(),
                                                                        self.combobox.get(),
                                                                        self.entry_summ.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):  # Унаследуемся от класса Child
    def __init__(self):
        super().__init__()
        self.init_edit()
        # и для того чтобы обращатся к функциям из класса Main, передадим его в конструктор класса UPDATE
        self.main_view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Изменить информацию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(relx=0.65, rely=0.6)
        btn_edit.bind('<Button-1>', lambda event: self.main_view.update_records(self.entry_desc.get(),
                                                                                self.combobox.get(),
                                                                                self.entry_summ.get()))
        # убираем кнопку добавить (btn_add)
        self.btn_add.destroy()

    def default_data(self):
        self.db.cursor.execute('''SELECT * FROM accounting WHERE id=?''',
                               (self.main_view.tree.set(self.main_view.tree.selection()[0], '#1'),))
        # создадим переме5нную в которую будем сохранять результаты запросов
        row = self.db.cursor.fetchone()
        self.entry_desc.insert(0, row[1])
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_summ.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.main_view = app


    def init_search(self):
        self.title('Окно поиска')
        self.geometry('300x100+500+600')
        self.resizable(False, False)

        search_lab = tk.Label(self, text='Поиск')
        search_lab.place(relx=0.2, rely=0.1)

        self.search_entry = tk.Entry(self)
        self.search_entry.place(relx=0.5, rely=0.1)

        btn_search = ttk.Button(self, text='Найти данные')
        btn_search.place(relx=0.2, rely=0.4)
        btn_search.bind('<Button-1>', lambda event: self.main_view.search_records(self.search_entry.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Реализация класса для базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('accounting.db')
        # создание обьекта курсор.
        # Данный обьект позволяет взаимодействовать с БД. Например: добавлять, удалять, изменять и т.д.
        self.cursor = self.conn.cursor()
        # создадим таблицу
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS accounting(
            id integer primary key,
            description text,
            costs text,
            total real)'''
        )
        # сохраним изменение
        self.conn.commit()

    def add_information(self, description, costs, total):
        self.cursor.execute('''INSERT INTO ACCOUNTING(description, costs, total) VALUES(?, ?, ?)''',
                            (description, costs, total))
        self.conn.commit()


# напишем условную конструкцию
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Accounting Home Finance')
    root.geometry('720x500+300+200')
    root.resizable(False, False)
    root.mainloop()
