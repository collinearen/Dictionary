import sqlite3
from tkinter import *
from tkinter import ttk


class Dictionary:
    db_name = 'dictionary_my.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Словарь')

        # creating elements for entering words and values
        frame = LabelFrame(self.wind, text='Добавление слова')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frame, text='Слово: ').grid(row=1, column=0)
        self.word = Entry(frame)
        self.word.focus()
        self.word.grid(row=1, column=1)
        Label(frame, text='Значение: ').grid(row=2, column=0)
        self.meaning = Entry(frame)
        self.meaning.grid(row=2, column=1)
        ttk.Button(frame, text='Сохранить', command=self.add_word).grid(row=3, columnspan=2, sticky=W + E)
        self.message = Label(text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
        # table of words and their meanings
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Слово', anchor=CENTER)
        self.tree.heading('#1', text='Значение', anchor=CENTER)

        # post editing buttons
        ttk.Button(text='Удалить', command=self.delete_word).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='Изменить', command=self.edit_word).grid(row=5, column=1, sticky=W + E)

        # filling out the table
        self.get_words()

    def run_query(self, query, parameters=()):
        '''
        :return: connecting and querying the database
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_words(self):
        '''
        :return: filling the table with words and their meanings
        '''
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM dictionary ORDER BY word DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validation(self):
        '''
        :return: input validation
        '''
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0

    def add_word(self):
        '''
        :return: adding a new word
        '''
        if self.validation():
            query = 'INSERT INTO dictionary VALUES(NULL, ?, ?)'
            parameters = (self.word.get(), self.meaning.get())
            self.run_query(query, parameters)
            self.message['text'] = f'слово {self.word.get()} добавлено в словарь'
            self.word.delete(0, END)
            self.meaning.delete(0, END)
        else:
            self.message['text'] = 'введите слово и значение'
        self.get_words()

    def delete_word(self):
        '''
        :return: deleting a word
        '''
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите слово, которое нужно удалить'
            return
        self.message['text'] = ''
        word = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM dictionary WHERE word = ?'
        self.run_query(query, (word,))
        self.message['text'] = f'Слово {format(word)} успешно удалено'
        self.get_words()

    def edit_word(self):
        '''
        :return: editing a word or meaning
        '''
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите слово для изменения'
            return
        word = self.tree.item(self.tree.selection())['text']
        old_meaning = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Изменить слово'

        Label(self.edit_wind, text='Прежнее слово:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=word), state='readonly').grid(row=0,
                                                                                                         column=2)

        Label(self.edit_wind, text='Новое слово:').grid(row=1, column=1)
        # предзаполнение поля
        new_word = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=word))
        new_word.grid(row=1, column=2)

        Label(self.edit_wind, text='Прежнее значение:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_meaning), state='readonly').grid(row=2,
                                                                                                                column=2)

        Label(self.edit_wind, text='Новое значение:').grid(row=3, column=1)
        # предзаполнение поля
        new_meaning = Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_meaning))
        new_meaning.grid(row=3, column=2)

        Button(self.edit_wind, text='Изменить',
               command=lambda: self.edit_records(new_word.get(), word, new_meaning.get(), old_meaning)).grid(row=4,
                                                                                                             column=2,
                                                                                                             sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_word, word, new_meaning, old_meaning):
        '''
        :return: making changes to the database
        '''
        query = 'UPDATE dictionary SET word = ?, meaning = ? WHERE word = ? AND meaning = ?'
        parameters = (new_word, new_meaning, word, old_meaning)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()


if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()
