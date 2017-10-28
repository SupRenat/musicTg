# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
import os
import sys
import time
import utils
import random

###
###

bot = telebot.TeleBot(config.token)
category = []
num=[]
mode=[]

#Если не аудио или файл
#А фото, видео, войс и тд
@bot.message_handler(func=lambda message: True,content_types=['video','photo','sticker','video','voice'])
def _return(message):
    upload_condition = utils.get_upload((message.from_user.id))
    if upload_condition==0:
        bot.send_message(message.chat.id,"It's nice, but I can't work with it c:")
        info(message)
    else:
        bot.send_message(message.chat.id, "Not audio!Try again!")
        utils.set_step(message.from_user.id, 1)
        utils.set_upload(message.from_user.id,0)
        info(message)

@bot.message_handler(func=lambda message: True,content_types=['audio'])
def upload_audio(message):
    upload_condition=utils.get_upload((message.from_user.id))
    category_id = utils.get_category_id((message.from_user.id))
    print(upload_condition)
    print(category_id)
    if upload_condition==1 and category_id!=0:
        print(message.audio)
        title = message.audio.title
        performer = message.audio.performer
        if str(title)!='None' and str(performer)!='None':
            utils.add_to_db(category_id, str(message.audio.file_id), str(performer+" "+title))
        elif str(title)=='None' and str(performer)!='None':
            utils.add_to_db(category_id, str(message.audio.file_id), str(performer))
        elif str(title)!='None' and str(performer)=='None':
            utils.add_to_db(category_id, str(message.audio.file_id), str(title))
        elif str(title)=='None' and str(performer)=='None':
            title = str(utils.get_category_name(category_id))+'_#'+str(len(utils.get_music_rows(category_id)))
            utils.add_to_db(category_id, str(message.audio.file_id), str(title))
        hide_categories(message, "Upload success")
        utils.set_upload((message.from_user.id),0)
    else:
        bot.send_message(message.chat.id,"Sorry, you dont choose the upload mode \n try the command '/upload' for this")

@bot.message_handler(func=lambda message:True, content_types=['document'])
def handle_doc(message):
    upload_condition = utils.get_upload((message.from_user.id))
    category_id = utils.get_category_id((message.from_user.id))
    if upload_condition == 1 and category_id != 0:
        try:
            if message.document.file_size >= 20900000:
                bot.send_message(message.chat.id,"Your file is too big")
                utils.set_step(message.from_user.id, 1)
                show_categories(message)
            elif message.document.mime_type == 'audio/mp3':
                tFile = create_file(message,message.document.file_name)
                print("File Creating!")
                try:
                    file_info = bot.get_file(message.document.file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    tFile.write(downloaded_file)
                    tFile.close()
                    f = open('template/'+str(message.from_user.id)+'/'+message.document.file_name, 'rb')
                    msg = bot.send_audio(message.chat.id, f, None)
                    f.close()
                    msg.audio.title = message.document.file_name
                    #print(msg.audio)
                    #bot.send_message(message.chat.id, msg.audio.file_id)
                    utils.add_to_db(category_id, str(msg.audio.file_id), str(msg.audio.title))
                    hide_categories(message, "Upload success")
                    utils.set_upload((message.from_user.id), 0)
                    delete_file(message,message.document.file_name)
                except:
                    print("Unexpected error:", sys.exc_info())
                    tFile.close()
                    f.close()
                    delete_file(message, message.document.file_name)
            else:
                bot.send_message(message.chat.id, "Not audio!Try again!")
                utils.set_step(message.from_user.id, 1)
                show_categories(message)
        except:
            print("Error!", sys.exc_info())
    else:
        bot.send_message(message.chat.id, "Sorry, you dont choose the upload mode \n try the command '/upload' for this")

@bot.message_handler(func=lambda message: True, commands=['menu'])
def show_mode(message):
    global mode
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    mode = [('Random in all',), ('In order in category',), ('Random in category',), ('Close',)]
    for i in range (len(mode)):
        markup.row(mode[i][0])
    bot.send_message(chat_id=message.chat.id, text="Choose the mode", reply_markup=markup)



@bot.message_handler(func=lambda message: True, commands=['upload'])
def upload(message):
    bot.send_message(message.chat.id, "Attention, you can simultaneously download only one audio file, and it should be less than or equal to 20 mb \n"
                                        "To upload a new audio file, re-enter the '/ upload'")
    utils.set_upload(message.from_user.id,1)
    utils.set_step(message.from_user.id,1)
    show_categories(message)
    #if bot.message_handler(func=lambda message: True,content_types=['audio']) or bot.message_handler(func=lambda message:True, content_types=['document']):
    #    print('Handled the right file')

@bot.message_handler(func=lambda message: True, commands=['disable_upload'])
def dis_upload(message):
    utils.set_upload(message.from_user.id,0)
    bot.send_message(message.chat.id,"Your upload condition is "+str(utils.get_upload(message.from_user.id)))

''''def find_file_ids(message):
    for file in os.listdir('music/psytrance/'):
        if file.split('.')[-1] == "mp3":
            f = open('music/psytrance/'+file, 'rb')
            msg = bot.send_audio(message.chat.id,f,None)
            #bot.send_message(message.chat.id,msg.audio.file_id, reply_to_message_id=msg.message_id)
            #file.split('.')[0] #имя файла
            f.close()
            utils.add_to_db(1, str(msg.audio.file_id), str(file.split('.')[0]))
        time.sleep(3)
'''''
@bot.message_handler(commands=['start'])
def start(message):
    try:
        utils.add_user((message.from_user.id))
        bot.send_message(message.chat.id, "Type'/menu' for listening \n"
                                          "Type '/upload' for upload \n"
                                          "Type '/info' for geting this message again \n")
        print(message.from_user.id)

    except :
        print(sys.exc_info())
        #if str(sys.exc_info()[0])=="<class 'sqlite3.IntegrityError'>":
        # bot.send_message(message.chat.id,"Я вас уже знаю с:")

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, "Type'/menu' for listening \n"
                                         "Type '/upload' for upload \n"
                                         "Type '/info' for geting this message again \n\n"
                                         "Attention, you can simultaneously download only one audio file, and it should be less than or equal to 20 mb \n"
                                        "To upload a new audio file, re-enter the '/ upload'")

@bot.message_handler(func=lambda message: True,content_types=["text"])
def check(message):
    try:
        global category,mode,num
        step=utils.get_step(message.from_user.id)
        upload_condition = utils.get_upload(message.from_user.id)
        mode_id=utils.get_mode(message.from_user.id)
        print(step)
        print(mode_id)
        print(upload_condition)
        print(category)
        # Close
        if  message.text  == "Close":
            hide_categories(message, 'In the next time')
            utils.set_step((message.from_user.id),0)
            return
        #Back
        elif message.text == "Back" and step !=0:
            if step == 1:
                show_mode(message)
            elif step == 2:
                show_categories(message)
            utils.set_step(message.from_user.id, step-1)
            return

        if step == 1 and upload_condition == 1:
            # Category
            print(len(category)-1)
            for i in range(len(category) - 1):
                print(i)
                print(category[i])
                if "('" + message.text + "',)" == str(category[i]):
                    utils.set_category_id((message.from_user.id),i+1)
                    utils.set_step(message.from_user.id, 0)
                    hide_categories(message, "Please, upload the audio in '" + message.text + "' category")
                    break
            return
            #Mode
            #All random
        if "('" + message.text + "',)" == str(mode[0]) and (step == 0):
            utils.set_mode((message.from_user.id),0)
            utils.set_step((message.from_user.id), 2)
            show_options_for_random(message)
            return

            #Other
        if "('" + message.text + "',)" == str(mode[1])  and (step == 0) :
            utils.set_mode((message.from_user.id), 1)
            utils.set_step((message.from_user.id), 1)
            show_categories(message)
            return

        if "('" + message.text + "',)" == str(mode[2])  and (step == 0):
            utils.set_mode((message.from_user.id), 2)
            utils.set_step((message.from_user.id), 1)
            show_categories(message)
            return

        # Category
        if step==1 and upload_condition!=1:
            for i in range(len(category) - 1):
                if "('" + message.text + "',)" == str(category[i]):
                    utils.set_category_id((message.from_user.id), i + 1)
                    utils.set_step((message.from_user.id), 2)
                    show_options_for_category(message, message.text)
                    break
            return

        #Num of tracks
        if step == 2:
            for i in range(len(num)-1):
                if "('" + message.text + "',)" == str(num[i]):
                    print(num[i][0])
                    utils.set_step((message.from_user.id), 0)
                    #Вытакскивать треки
                    mode_id=utils.get_mode(message.from_user.id)
                    category_id = utils.get_category_id(message.from_user.id)
                    n=int(num[i][0])
                    unload_tracks(message,mode_id,category_id,n)
                    show_mode(message)
                    break
            return
    except:
        print(sys.exc_info())
        print("text Error!")
        show_mode(message)


def show_categories(message):
    global category
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    category= utils.generate_category_markup()
    for i in range(len(category)):
        markup.row(category[i][0])
    bot.send_message(chat_id=message.chat.id, text="Choose the category", reply_markup=markup)

def show_options_for_category(message,category):
    global num
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = [('1',),('5',),('10',),('Back',),('Close',)]
    for i in range(len(num)):
        markup.row(num[i][0])
    bot.send_message(chat_id=message.chat.id, text="Choose the num of tracks of "+category, reply_markup=markup)

def show_options_for_random(message):
    global num
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = [('1',), ('5',), ('10',), ('Close',)]
    for i in range(len(num)):
        markup.row(num[i][0])
    bot.send_message(chat_id=message.chat.id, text="Choose the num of tracks ", reply_markup=markup)
def hide_categories(message,text):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


def create_file(message,fileName):
    os.mkdir('template/'+str(message.from_user.id),mode=0o777)
    templateFile = open('template/'+str(message.from_user.id)+'/'+fileName,'wb')
    return templateFile


def delete_file(message,fileName):
    try:
        os.remove('template/'+str(message.from_user.id)+'/'+fileName)
        os.rmdir('template/'+str(message.from_user.id))
    except:
        print("delete Error!")


def unload_tracks(message,mode,category_id,num):
        #Random in all
    if mode ==0:
        num_rows = len(utils.get_all_music_rows())
        if num >= num_rows:
            rows = utils.get_all_music_rows()
            print(rows)
            for i in range(num_rows):
                sendAudio(message, str(rows[i][0]))
        else:
            rows = utils.get_random_in_all(num)
            for i in range(num):
                sendAudio(message, str(rows[i][0][0]))
        #In round in category
    elif mode == 1:
        num_rows = len(utils.get_music_rows(category_id))
        if num >= num_rows:
            rows = utils.get_music_rows(category_id)
            print(rows)
            for i in range(num_rows):
                sendAudio(message,str(rows[i][0]))
        else:
            last = utils.get_last_in_category(message.from_user.id,category_id)
            utils.set_last_in_category(message.from_user.id, category_id, last+num)
            rows=utils.get_audio(category_id,last,num)
            if num_rows <= utils.get_last_in_category(message.from_user.id,category_id):
                utils.set_last_in_category(message.from_user.id, category_id, 0)
            for i in range(num):
                sendAudio(message,str(rows[i][0]))

        #Random in category
    elif mode == 2:
        num_rows = len(utils.get_music_rows(category_id))
        if num >= num_rows:
            rows = utils.get_music_rows(category_id)
            print(rows)
            for i in range(num_rows):
                sendAudio(message,str(rows[i][0]))
        else:
            rows = utils.get_random_in_category(category_id, num)
            for i in range(num):
                sendAudio(message,str(rows[i][0][0]))

def sendAudio(message,file_id):
    bot.send_audio(message.chat.id,file_id)




if __name__ == '__main__':
    bot.polling(none_stop=True)

