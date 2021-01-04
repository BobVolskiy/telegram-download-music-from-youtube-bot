#!/usr/bin/python3.8
import telebot
import os
from config import * #create config.py file next to this one. config.py example copy from 
import youtube_dl
import eyed3
import re
from PIL import Image
bot = telebot.TeleBot(token)
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'Этот бот конвертирует видео с ютуба в MP3 320kbps\nОтправь мне ссылку на видео, чтобы скачать песню...')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул старт')
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,'Этот бот конвертирует видео с ютуба в MP3 320kbps и высылает вам в виде аудио\n\nБота создал @bob_volskiy\nИсходный код: github.com/BobVolskiy/\n\nМои боты:\n@bvsticker_bot\n@bob_musica_bot')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул хелп')
@bot.message_handler(content_types=["text"])
def link(message):
    link=message.text
    if link.find('youtu')!=-1:
        try:
            ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best[filesize<50M]',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info=ydl.extract_info(link)
            title=info['title']
            code=info['id']
            name=title.replace("/", "_")
            punct = '[–-]+'
            lst = re.split(punct, title)
            os.system("youtube-dl "+"--write-thumbnail "+"--skip-download "+"--output "+code+" "+link) 
            audiofile = eyed3.load(name+'.mp3')
            try:
                audiofile.tag.artist = lst[0]
                audiofile.tag.title = lst[1]
            except: audiofile.tag.title = title
            audiofile.tag.images.set(3, open(code+'.webp','rb').read(), 'image/jpeg')
            audiofile.tag.save()
            
            k = open(name+'.mp3','r+b')
            photo = Image.open(code+'.webp')
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, photo)
            bot.send_chat_action(message.chat.id, 'upload_audio')
            bot.send_audio(message.chat.id,k)
            os.remove(name+'.mp3')
            os.remove(code+'.webp')
        except:
            bot.send_message(message.chat.id,'Произошла какая-то ошибка ❌')
    else: bot.send_message(message.chat.id,'Это не похоже на ссылку с ютуба ❌')
print('Бот начал свою работу...')
bot.polling()