import telebot
import uuid
import os
import speech_recognition as sr
from translatepy.translators.google import GoogleTranslate

language='ru_RU'
TOKEN='6434718463:AAEG-tu5DmIY5qKYA-9sPXqTPRyfWt6rH-I'
bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')
            return "Sorry.. run again..."

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    bot.reply_to(message, text)
    # os.remove(file_name_full)
    # os.remove(file_name_full_converted)

@bot.message_handler(content_types=['text'])
def sending_voice(message):
    if message.text == "/start":
        pass
    if message.text == "/help":
        pass
    if message.text == "/love":
        bot.send_voice(message.from_user.id,open("voice\\love.ogg",'rb'))
    if message.text == "/gpt":
        bot.send_voice(message.from_user.id,open("voice\\gpt.ogg",'rb'))
    if message.text == "/sql":
        bot.send_voice(message.from_user.id,open("voice\\sql_nosql.ogg",'rb'))
   


# bot.polling()