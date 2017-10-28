# -*- coding: utf-8 -*-
import sqlite3

class SQLighter:

    def __init__(self,database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """Получаем все строки"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def select_single(self,rownum):
        """"Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id=?',(rownum)).fetchall()[0]

    def get_all_audio(self):
        """"Получаем все строки"""
        with self.connection:
            return self.cursor.execute('SELECT file_id FROM `music`').fetchall()


    def get_audio(self,category_id,last, num):
        """"Получаем num сразу после last строк с category_id"""
        with self.connection:
            return self.cursor.execute('SELECT file_id FROM `music` WHERE category_id=? LIMIT ?,?',(category_id,last,num,)).fetchall()


    def get_some_audio_from_category(self,category_id, num):
        """"Получаем num сразу после last строк с category_id"""
        with self.connection:
            return self.cursor.execute('SELECT file_id FROM `music` WHERE category_id=? LIMIT ?',(category_id,num,)).fetchall()

    def get_rowid_from_category(self,category_id):
        """Получаем список всех ROWID категории"""
        with self.connection:
            return self.cursor.execute('SELECT ROWID FROM `music` WHERE category_id=?',(category_id,)).fetchall()

    def get_rowid_from_all(self):
        """Получаем список всех ROWID"""
        with self.connection:
            return self.cursor.execute('SELECT ROWID FROM `music`').fetchall()

    def get_all_from_category(self,category_id):
        """"Получаем все строки с category_id"""
        with self.connection:
            return self.cursor.execute('SELECT file_id FROM `music` WHERE category_id=? ',(category_id,)).fetchall()

    def select_all_categories(self):
        """"Получаем все категории"""
        with self.connection:
            return self.cursor.execute('SELECT category_name FROM `category` ').fetchall()

    def count_rows(self,name):
        """"Считаем количество строк"""
        with self.connection:
            if name == 'music':
                result = self.cursor.execute('SELECT * FROM `music`').fetchall()
            elif name == 'category':
                result = self.cursor.execute('SELECT * FROM `category`').fetchall()
            return len(result)

    def add(self,category_id,file_id,title):
        """Записываем в бд"""
        with self.connection:
            self.cursor.execute('INSERT INTO `music` (category_id,file_id,title) VALUES (?,?,?)',(category_id,file_id,title)).fetchall()

    def add_user(self,user_id):
        """"Добавлям пользователя в БД"""
        with self.connection:
            self.cursor.execute('INSERT INTO `users` (user_id) VALUES (?)',(user_id,)).fetchall()
    def change(self,user_id,mode,step,category_id,upload):
        """"Меняем поля в таблице пользователя"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET mode=?, step=?, category_id=?, upload=? WHERE user_id=? ',(mode,step,category_id,upload,user_id,)).fetchall()

    def get_mode(self,user_id):
        """Получаем режим из таблицы"""
        with self.connection:
            result = self.cursor.execute('SElECT mode FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return  result
    def set_mode(self,user_id,mode):
        """Задаем режим в таблице"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET mode=? WHERE user_id=?',(mode,user_id,)).fetchall()


    def get_step(self,user_id):
        """Получаем шаг из таблицы"""
        with self.connection:
            result = self.cursor.execute('SElECT step FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return  result
    def set_step(self,user_id,step):
        """Задаем шаг в таблице"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET step=? WHERE user_id=?',(step,user_id,)).fetchall()


    def get_category_id(self,user_id):
        """Получаем категорию из таблицы"""
        with self.connection:
            result = self.cursor.execute('SELECT category_id FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return result
    def set_category_id(self,user_id,category_id):
        """Задаем категорию в таблице"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET category_id=? WHERE user_id=?',(category_id,user_id,)).fetchall()


    def get_upload(self,user_id):
        """Получаем режим загрузки из таблицы"""
        with self.connection:
            result = self.cursor.execute('SELECT upload FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return result
    def set_upload(self,user_id,upload):
        """Задаем режим загрузки в таблице"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET upload=? WHERE user_id=?',(upload,user_id,)).fetchall()


    def get_last_in_category_1(self,user_id):
        """Получаем последнее в категории num"""
        with self.connection:
            result=self.cursor.execute('SELECT last_in_category_1 FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return result
    def set_last_in_category_1(self,user_id, num):
        """Задаем последнее в категории num"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET last_in_category_1=? WHERE user_id=?',(num,user_id,)).fetchall()


    def get_last_in_category_2(self,user_id):
        """Получаем последнее в категории num"""
        with self.connection:
            result=self.cursor.execute('SELECT last_in_category_2 FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return result
    def set_last_in_category_2(self,user_id, num):
        """Задаем последнее в категории num"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET last_in_category_2=? WHERE user_id=?',(num,user_id,)).fetchall()


    def get_last_in_category_3(self,user_id):
        """Получаем последнее в категории num"""
        with self.connection:
            result=self.cursor.execute('SELECT last_in_category_3 FROM `users` WHERE user_id=?',(user_id,)).fetchall()
        return result
    def set_last_in_category_3(self,user_id, num):
        """Задаем последнее в категории num"""
        with self.connection:
            self.cursor.execute('UPDATE `users` SET last_in_category_3=? WHERE user_id=?',(num,user_id,)).fetchall()


    def get_category_name(self,category_id):
        """"Получаем название категории по ее id"""
        with self.connection:
            result = self.cursor.execute('SELECT category_name FROM `category` WHERE category_id=?',(category_id,)).fetchall()
        return result

    def get_audio_by_rowid(self,rowid):
        """Получаем аудио (file_id) по значению rowid"""
        with self.connection:
            result = self.cursor.execute('SELECT file_id FROM `music` WHERE ROWID=?',(rowid,)).fetchall()
        return result

    def close(self):
        """"Закрываем текущее соединение с БД"""
        self.connection.close()