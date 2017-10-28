# -*- coding: utf-8 -*-
from config import  database_name
from SQLighter import SQLighter
import random

def get_count_rows(name):
    db=SQLighter(database_name)
    rowsnum = db.count_rows(name)
    db.close()
    return rowsnum

def get_categories_rows():
    db = SQLighter(database_name)
    category_list =db.select_all_categories()
    return category_list

def generate_category_markup():
    all_items=get_categories_rows()
    print(all_items)
    #all_items = '{},{}'.format("Hello", "World")
    list_items = []
    for item in all_items:
        list_items.append(item)
    list_items.append(('Close',))
    return list_items

def get_category_rows_count(category_id):
    db = SQLighter(database_name)
    rowsnum = len(db.select_all_from_category(category_id))
    db.close()
    return rowsnum

def get_category_rows(category_id):
    db = SQLighter(database_name)
    category_rows =db.select_all_from_category(category_id)
    db.close()
    return category_rows

def add_to_db(category_id,file_id,title):
    db = SQLighter(database_name)
    db.add(category_id,file_id,title)
    db.close()

def get_all_music_rows():
    db = SQLighter(database_name)
    result = db.get_all_audio()
    db.close()
    return result

def get_music_rows(category_id):
    db = SQLighter(database_name)
    result = db.get_all_from_category(category_id)
    db.close()
    return result
def get_some_music_rows(category_id,num):
    db = SQLighter(database_name)
    result = db.get_some_audio_from_category(category_id,num)
    db.close()
    return result

def add_user(user_id):
    db = SQLighter(database_name)
    db.add_user(user_id)
    db.close()

def get_mode(user_id):
    db = SQLighter(database_name)
    result = db.get_mode(user_id)[0][0]
    db.close()
    return result
def set_mode(user_id,mode):
    db = SQLighter(database_name)
    db.set_mode(user_id,mode)
    db.close()


def get_step(user_id):
    db = SQLighter(database_name)
    result = db.get_step(user_id)[0][0]
    db.close()
    return result
def set_step(user_id,step):
    db = SQLighter(database_name)
    db.set_step(user_id,step)
    db.close()


def get_category_id(user_id):
    db = SQLighter(database_name)
    result = db.get_category_id(user_id)[0][0]
    db.close()
    return result
def set_category_id(user_id,category_id):
    db = SQLighter(database_name)
    db.set_category_id(user_id,category_id)
    db.close()

def get_upload(user_id):
    db = SQLighter(database_name)
    result = db.get_upload(user_id)[0][0]
    db.close()
    return result
def set_upload(user_id,upload):
    db = SQLighter(database_name)
    db.set_upload(user_id,upload)
    db.close()

def get_last_in_category(user_id,category_id):
    db = SQLighter(database_name)
    result=0
    if category_id==1:
        result=db.get_last_in_category_1(user_id)[0][0]
    elif category_id==2:
        result=db.get_last_in_category_2(user_id)[0][0]
    elif category_id==3:
        result=db.get_last_in_category_3(user_id)[0][0]
    db.close()
    return result

def set_last_in_category(user_id,category_id,count):
    db = SQLighter(database_name)
    if category_id==1:
        db.set_last_in_category_1(user_id,count)
    elif category_id==2:
        db.set_last_in_category_2(user_id, count)
    elif category_id==3:
        db.set_last_in_category_3(user_id, count)
    db.close()


def get_category_name(category_id):
    db = SQLighter(database_name)
    result = db.get_category_name(category_id)[0][0]
    db.close()
    return result

def get_audio(category_id,last, num):
    db = SQLighter(database_name)
    result = db.get_audio(category_id,last, num)
    db.close()
    return result

def get_random_in_category(category_id,num):
    db = SQLighter(database_name)
    result =[]
    ids=db.get_rowid_from_category(category_id)
    list = random.sample(ids,num)
    for i in range(num):
        result.append(db.get_audio_by_rowid(list[i][0]))
    db.close()
    return result

def get_random_in_all(num):
    db = SQLighter(database_name)
    result = []
    ids = db.get_rowid_from_all()
    list = random.sample(ids, num)
    for i in range(num):
        result.append(db.get_audio_by_rowid(list[i][0]))
    db.close()
    return result