# -*- coding:utf-8 -*-
import schedule
import telebot
from requests import get
from threading import Thread
from time import sleep,gmtime, strftime
from bs4 import BeautifulSoup
from re import compile

url = get("https://www.iski.istanbul/web/tr-TR/ariza-kesinti")
soup = BeautifulSoup(url.content, "html.parser")
bot_token = "Sizin botunuzun token bilgisi"
bot = telebot.TeleBot(bot_token)
chat_id = "Sizin botunuzun chat_id bilgisi"

@bot.message_handler(commands=['bilgi', 'start'])
def bilgi(message):
    metin = """
İski tarafından duyurulan planlı su kesintilerini mesaj olarak almak isterseniz /bildir İlçe Mahalle şeklinde aralarda boşlık bırakarak oturduğunuz ilçe ve mahalle bilgisini girebilirsiniz. İlçe ve mahalle bilgisini girerken baş harfleri büyük ve doğru yazdığınızdan emin olun. Bu bilgileri doğru girmediğiniz takdirde bildirimleri alamayabilirsiniz.

Örneğin /bildir Ümraniye Çakmak"""
    global msg
    msg = bot.send_message(message.chat.id,metin)

def bildir2(ilce,mahalle):
    global msg
    search = compile(ilce)
    sonuc = soup.find_all(text = search)
    for i in sonuc:
        if i is not None:
            sonuc = i.parent.parent.parent
            search2 = compile(mahalle)
            sonuc2 = sonuc.find(text = search2)
            if sonuc2 is not None:
                iter = 0
                sebep = sonuc.find_all("tr")
                for i in sebep:
                    if iter == 3:
                        aciklama = i.find_all("td")
                        aciklama2 = aciklama[2].text.strip()
                    if iter == 4:
                        baslama = i.find_all("td")
                        baslangic = baslama[2].text.strip()
                    if iter == 5:
                        bitis = i.find_all("td")
                        bitme = bitis[2].text.strip()
                    iter += 1
                mesaj = f"{ilce}-{mahalle} mahallesinde {aciklama2} sebebiyle, {baslangic} tarihinde baslanan/baslanacak {bitme}"
                if msg.text == mesaj:
                    pass
                else:
                    msg = bot.send_message(chat_id, mesaj)
            else:
                pass
        else:
            pass

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    @bot.message_handler(commands=['bildir'])
    def bildir(message):
        try:
            girdi = message.text.split(' ') 
            ilce = girdi[1]
            if ilce.lower() == "büyükçekmece" or ilce.lower() == "büyük çekmece" or ilce.lower() == "buyukcekmece" or ilce.lower() == "buyuk cekmece":
                ilce = "B.Çekmece"
                print(ilce)
            elif ilce.lower() == "küçükçekmece" or ilce.lower() == "küçük çekmece" or ilce.lower() == "kucukcekmece" or ilce.lower() == "kucuk cekmece":
                ilce = "K.Çekmece"
            elif ilce.lower() == "gaziosmanpaşa" or ilce.lower() == "gaziosmanpasa" or ilce.lower() == "gazi osman pasa"or ilce.lower() == "gazi osman paşa":
                ilce = "G.O.Paşa"
            mahalle = girdi[2]
            schedule.every(3).hours.do(bildir2,ilce,mahalle)
        except IndexError:
            pass
    Thread(target=schedule_checker).start()

while True:
    try:
        bot.polling(none_stop=True)     
    except Exception:
        sleep(15)
