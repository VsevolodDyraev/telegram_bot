import telebot
from telebot import types
import uuid
import os
import speech_recognition as sr
from translatepy.translators.google import GoogleTranslate
gtranslate = GoogleTranslate()


language='ru_RU'
f = open("config.txt",'r')
TOKEN=f.readline()
bot = telebot.TeleBot(TOKEN) #<---- Если запускаете, впишите сюда токен бота
r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            return [text,1]
        except:
            return ["Sorry.. run again...",0]

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
    text,f=recognise(file_name_full_converted)
    if f:
        bot.reply_to(message, text = "Ты сказал: " + text + "😳\n"+"А теперь на английском: "+gtranslate.translate(text, "English").result)
    else:
        bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Помогите")
    btn2 = types.KeyboardButton("почти мой пост (нет)")
    btn3 = types.KeyboardButton("Селфи №1🐱")
    btn4 = types.KeyboardButton("Селфи №2😸")
    btn5 = types.KeyboardButton("Лябовь❤️")
    btn6 = types.KeyboardButton("ChatGPT для бабушек🤖")
    btn7 = types.KeyboardButton("❓Sql, NoSql? ЧТО?❓")
    btn8 = types.KeyboardButton("GIT")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    return markup

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Это тестовый бот, чтобы узнать, что я умею напиши /help.", reply_markup=get_keyboard()) 

    elif message.text == "/help" or message.text == "Помогите":
        bot.send_message(message.from_user.id, "У тебя снизу должна появиться клавиатура, там можно потыкать.\n Еще ты можешь записать аудиосообщение и посмотри что будет))\n\n Eсли ничего не появилось, то напиши в адvинистрацию, мы оторвем руки нашему программисту😊",reply_markup=get_keyboard())

    elif message.text == "/post" or message.text == "почти мой пост (нет)":
        bot.send_message(message.from_user.id, text=' <b>ЗДАРОВА БАНДИТЫ! </b> \n\n С ВАМИ СНОВА Я! ДЖУУУУЛАЙ 😈 \n\n ТЕМА этого поста: <u>хобби</u>\n Я расскажу вам про свое хобби - фотографию. 📸 \n\n У всех под рукой всегда есть телефон, и чаще всего вы сидите в соцсетях и не замечаете того, что происходит вокруг вас... Залипаете в инсте (запрещена в РФ) и лайкаете фотки инстадевочек с кучей фильтров, пока кто-то эти фотки делает 😏😏 \n\n Так вот, в чем же суть? \n Фотография помогает передать чувства и настроение человека, который попадает в кадр и, конечно же, самого себя. Ну мы говорим про настоящих фотографов, а не тех, кто снимает завтраки из ресторанов для нового поста) Настоящего фотографа можно назвать полноценным художником со своим мировосприятием и стилем!!! \n\n Так что, ребятки, развивайтесь, изучайте новые сферы, будьте в РЕСУРСЕ, ПОТОКЕ и тд. \n\n Пишите к комментариях про свои хобби и прикрепляйте фото!', parse_mode='HTML')  
    
    
    elif message.text == "/self1" or message.text == "Селфи №1🐱":
        bot.send_photo(message.from_user.id, open("image\\self1.jpg",'rb'),"Это моя первая фотка)")
    
    
    elif message.text == "/self2" or message.text == "Селфи №2😸":
        bot.send_photo(message.from_user.id, open("image\\self2.jpg",'rb'),"Это моя вторая фотка)")           
    
    elif message.text == "/love" or message.text == "Лябовь❤️":
        bot.send_voice(message.from_user.id,open("voice\\love.ogg",'rb'))
    
    elif message.text == "/gpt" or message.text == "ChatGPT для бабушек🤖":
        bot.send_voice(message.from_user.id,open("voice\\gpt.ogg",'rb'))
    
    elif message.text == "/sql" or message.text == "❓Sql, NoSql? ЧТО?❓":
        bot.send_voice(message.from_user.id,open("voice\\sql_nosql.ogg",'rb'))
    
    elif message.text == "/git" or message.text == "GIT":
        bot.send_message(message.from_user.id, "Ссылка на репозиторий: https://github.com/VsevolodDyraev/telegram_bot")
    

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.") 

bot.polling(none_stop=True, interval=0)