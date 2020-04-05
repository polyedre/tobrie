#sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
#pip install python-telegram-bot==12.0.0b1 --upgrade

from uuid import uuid4
import telegram
from telegram import InlineQueryResultArticle, InlineQueryResultVideo, InputTextMessageContent, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, ChosenInlineResultHandler, CommandHandler, MessageHandler, Filters
import re
import logging
import random
from datetime import datetime, timedelta
import time
import os
from shutil import move
import requests
from urllib.parse import unquote
from timeloop import Timeloop
from zalgo_text import zalgo

import subprocess
import wave

import re
from collections import defaultdict

TEST = False

#videoPath = 'video/'
soundPath = 'sound/'
memePath = 'meme/'
logPath = 'log/'
dataServerAddress = 'http://copperbot.fr/tobrie_uploader/videos/'

dataPath = 'data/old/'

chatbot_enable = False
auto_reply = True
di_enable = True

sound_files = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "x", "d", "r", "c"]

users = {'Alban':470589955, 'Mathieu':400322253, 'Vincent':479998987,
        'Emile':938620840, 'Tristan':427032387, 'Leo':936261629,
        'Erwann':893891596, 'Sebastien':902796168, 'Hugo':460908392,
        'Martin':955908707}

admin_user_id = [users['Alban'], users['Vincent']]
super_admin = users['Vincent']

messages_perso = [['TudorEustache', 100, "C'est Ambre qui t'a dit ça?"],['lgqsbdc', 200, "Mais oui c'est clair!"],['G_W_did_911', 20, "C'est pas faux"],['Filipouq',10,"Je sais où tu te caches!"]]


id_test = -1001486633512
id_conv_robot = -1001455757279
id_campagne = -1001445559004
id_petites_loutres = -1001216704238
id_loutres_officielles = -1001403402459
id_first_year = -366419257

def id_print(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Campagne: "+str(id_campagne)+"\nPetites Loutres: "+str(id_petites_loutres)+"\nConv 1A: "+str(id_first_year))

conv_link = []#[id_loutres_officielles, id_first_year]

id_console = 479998987

conv_perso = 479998987
conv_out = conv_perso

depth = 0

simple_map = [[u'whisky', u'Non bordel, ramenez pas du whisky, personne n\'aime ça sauf Hugo !'], [u'matlab', u'T\'as mis clc ?'], [u'tristant', u'Y a pas de T a la fin bordel !'], [u'soeur d\'alban', u'Alban a une soeur?'], [u'matthieu', u'Mathieu avec un seul T!!!'], [u'forsans', u'C\'est en forçant qu\'on y arrive !!'], [u'jeanne', u'Au secours !!!'], [u'bolzano', u'Un espace metrisable X est compact (au sens de l\'axiome de Borel-Lebesgue) si (et seulement si) toute suite d\'elements de X admet une valeur d\'adherence dans X ou, de maniere equivalente, admet une sous-suite qui converge vers un element de X.']]
end_map = [['quoi', 'feur'], ['vincent', 'timetre'], ['hugo', 'blet'], ['lucas', 'tapulte']]
sticker_map = [['tesson', 16], ['biere', 18], ['reunion', 19], ['velo', 4], ['energie', 23], ['tocard', 14], ['silence', 13]]

########################################################################################################################################################
#                                                                       LOGS                                                                           #
########################################################################################################################################################

def saveToLog(msg):
    if not TEST:
        file = open(logPath+str(msg.chat_id),"a")
        file.write("["+msg.from_user.first_name+", "+str(msg.from_user.id)+", "+str(datetime.now())+": "+msg.text+"\n")
        file.close()

def notifConsole(update, context):
    if (update.message.chat_id != (-1001455757279)):
        context.bot.send_message(chat_id=conv_perso, text="["+str(update.message.chat_id)+", "+update.message.from_user.first_name+", "+str(update.message.from_user.id)+": "+update.message.text)


########################################################################################################################################################
#                                                                       TEXT                                                                           #
########################################################################################################################################################


def sendVideo(update, context, file):
    context.bot.send_video(chat_id=update.message.chat_id, video=dataServerAddress+file, supports_streaming=True)

def sendYesNo(bot, update):
    if random.randint(0, 1) == 0:
        bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendDocument(chat_id=update.message.chat_id, document="https://media1.giphy.com/media/uXiGkGqG4ZQ6A/giphy.gif?cid=3640f6095c9b5bc04c6d737836068cde")
    else:
        bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendDocument(chat_id=update.message.chat_id, document="https://i.imgflip.com/19nqxs.gif")
def recur(update, context, msg):
    seteirbot = context.bot.get_sticker_set("EIRBOTO")
    msg_lower = msg.lower()

    # Anti spam
    global depth
    depth+=1
    if depth > 2:return

    # di/cri
    if "di" in msg_lower:
        i = msg_lower.find("di")
        j = msg.find(" ", i);
        if j == -1:
            j = len(msg)
        if j-i-2 > 1:
            context.bot.send_message(chat_id=update.message.chat_id, text=msg[i+2:j])
            recur(update, context, msg[i+2:j])
    if "cri" in msg_lower:
        i = msg_lower.find("cri")
        j = msg.find(" ", i);
        if j == -1:
            j = len(msg)
        if j-i-3 > 1:
            context.bot.send_message(chat_id=update.message.chat_id, text=msg[i+3:j].upper())
            recur(update, context, msg[i+3:j].upper())

    # Special detection
    if "mercredi" in msg_lower:
        context.bot.send_message(chat_id=update.message.chat_id, text="It is wednesday my dudes !")
    if "cafe" in msg_lower:
        context.bot.send_message(chat_id=update.message.chat_id, text="PATAR")
    if "fromage" in msg_lower:
        context.bot.sendSticker(chat_id=update.message.chat_id, sticker=seteirbot.stickers[24])

    # Generic maps
    for i in sticker_map:
        if i[0] in msg_lower:
            context.bot.sendSticker(chat_id=update.message.chat_id, sticker=seteirbot.stickers[i[1]])
    for i in end_map:
        if msg_lower.endswith(i[0]):
            context.bot.send_message(chat_id=update.message.chat_id, text=i[1])
    for i in simple_map:
        if i[0] in msg_lower:
            context.bot.send_message(chat_id=update.message.chat_id, text=i[1])

    if "salim" in msg_lower and not("salime" in msg_lower):
        context.bot.send_message(chat_id=update.message.chat_id, text="Salime avec un E!!!")
    if "ariane" in msg_lower:
        context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        context.bot.sendDocument(chat_id=update.message.chat_id, document="https://media3.giphy.com/media/3ov9jPjweggTGwtalG/giphy.gif")
    elif msg[-1] == "?":
        if random.randint(0, 2) == 0:
            sendYesNo(context.bot, update)
def handleText(update, context):
    # Chatbot response
    if chatbot_enable and update.message.chat_id in [-1001216704238, -1001294887664]:
        context.bot.send_message(chat_id=conv_out, text=generate().replace('apos', '\''))

    msg = update.message.text

    # Log + forward
    if update.message.chat_id != update.message.from_user.id:
        saveToLog(update.message);
    if update.message.chat_id == conv_perso:
        context.bot.send_message(chat_id=conv_out, text=update.message.text)
    else:
        notifConsole(update, context)

    # Process text for responses
    if di_enable:
        global depth
        depth = 0
        for i in messages_perso:
            if update.message.from_user.username == i[0] and i[1]-1 >= 0 and random.randint(0, i[1]-1) == 0:
                context.bot.send_message(chat_id=update.message.chat_id, text=i[2])
                recur(update, context, msg)
        # Video auto reply from video_strong_tags
    if auto_reply:
        i = 0
        results = []
        while i < len(video_strong_tags):
            if video_strong_tags[i] != '' and ' '+video_strong_tags[i]+' ' in ' '+msg.lower()+' ':
                #sendVideo(update, context, video_names_out[i])
                #i = len(video_strong_tags)
                results+=[video_names_out[i]]
            i+=1
        if len(results) > 0:
            sendVideo(update, context, results[random.randint(0, len(results)-1)])


########################################################################################################################################################
#                                                                       VIDEO                                                                          #
########################################################################################################################################################

video_strong_tags = []
video_names_out = []
def update_video_names():
    global video_names_out, video_strong_tags
    #Mouhahaha
    video_names_out=sorted([i.split('>')[0][9:-1] for i in unquote(requests.get(dataServerAddress).text).split("<img src=\"/__ovh_icons/movie.gif\" alt=\"[VID]\"> ")[1:]])
    video_strong_tags = [(i+'__.mp4').split('__')[1][:-4] for i in video_names_out]
update_video_names()
def update_video_names_command(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hack de votre pc en cours...")
    update_video_names()
    global video_names_out
    context.bot.send_message(chat_id=update.message.chat_id, text="Ménage effectué ("+str(len(video_names_out))+" fichiers supprimés).")
    sendVideo(update, context, 'lol_issou_xd_1.mp4')

def getResults(txt, names):
    results = []
    for vid in names:
        i = 0
        ok = True
        while i < len(txt):
            if not(txt[i] in vid.lower()):
                ok = False
                i = len(txt)
            i+=1
        if ok:
            results+=[vid]
    return results
def inlinequery(update, context):
    context.bot.send_message(chat_id=conv_perso, text="["+", "+str(update.inline_query.from_user.first_name)+", "+str(update.inline_query.from_user.id)+": "+update.inline_query.query)
    txt = update.inline_query.query.lower().split(" ")

    if txt[0] == 'z':
        zal = zalgo.zalgo().zalgofy(" ".join(txt[1:]))
        results = [InlineQueryResultArticle(id=uuid4(), title=zal, input_message_content=InputTextMessageContent(zal), description=zal)]#zalgo.zalgo().zalgofy("Some text to zalgofy!")
        update.inline_query.answer(results)
    else:
        r = getResults(txt, video_names_out)
        results = [InlineQueryResultVideo(uuid4(), dataServerAddress+vname, "video/mp4", "https://bde.eirb.fr/storage/img/logo/LogoEirbot.png", vname) for vname in r]
        update.inline_query.answer(results)
def list(update, context):
    notifConsole(update, context)
    if update.message.chat_id == update.message.from_user.id:
        for i in range(len(video_names_out)//10):
            context.bot.send_message(chat_id=update.message.chat_id, text="\n".join(video_names_out[i*10:(i+1)*10]))
        context.bot.send_message(chat_id=update.message.chat_id, text="\n".join(video_names_out[(int(len(video_names_out)//10))*10:]))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Le /list est interdit dans les groupes")
def dico(update, context):
    notifConsole(update, context)
    if update.message.chat_id == update.message.from_user.id:
        d = []
        for name in video_names_out:
            for i in name[:-4].split('_'):
                if not i in d:
                    d+=[i]
        d = sorted(d)
        for i in range(len(d)//100):
            context.bot.send_message(chat_id=update.message.chat_id, text=", ".join(d[i*100:(i+1)*100]))
        context.bot.send_message(chat_id=update.message.chat_id, text=", ".join(d[(int(len(d)//100))*100:]))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Le /dico est interdit dans les groupes")
def dico2(update, context):
    notifConsole(update, context)
    if update.message.chat_id == update.message.from_user.id:
        d = []
        for name in video_strong_tags:
            if name != '' and not name in d:
                d+=[name]
        d = sorted(d)
        for i in range(len(d)//100):
            context.bot.send_message(chat_id=update.message.chat_id, text=", ".join(d[i*100:(i+1)*100]))
        context.bot.send_message(chat_id=update.message.chat_id, text=", ".join(d[(int(len(d)//100))*100:]))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Le /dico2 est interdit dans les groupes")


########################################################################################################################################################
#                                                              OTHER COMMANDS                                                                          #
########################################################################################################################################################


def msg(update, context):
    notifConsole(update, context)
    data = update.message.text[5:].split(' ')
    if len(data) == 3:
        a = data[0][1:]
        b = int(data[1])
        if b >= 0 and update.message.from_user.username != a:
            global messages_perso
            l = [i[0] for i in messages_perso]
            if a in l:
                c = l.index(a)
                messages_perso[c][1] = b
                messages_perso[c][2] = " ".join(data[2:])
            else:
                messages_perso+=[[a, b, " ".join(data[2:])]]

def conv(update, context):
    global conv_out
    if update.message.from_user.id == super_admin:
        conv_out = int(update.message.text[6:])
def setDI(update, context):
    notifConsole(update, context)
    #if update.message.from_user.id == super_admin:
    global di_enable
    di_enable = not(di_enable)
    context.bot.send_message(chat_id=update.message.chat_id, text=str(di_enable))
def setAutoReply(update, context):
    notifConsole(update, context)
    #if update.message.from_user.id == super_admin:
    global auto_reply
    auto_reply = not(auto_reply)
    context.bot.send_message(chat_id=update.message.chat_id, text=str(auto_reply))

def meme(update, context):
    notifConsole(update, context)
    memes = [f for f in os.listdir(memePath) if os.path.isfile(os.path.join(memePath, f))]
    m = memes[random.randint(0, len(memes)-1)]
    context.bot.send_photo(update.message.chat_id, open(memePath+m, 'rb'))

def help(update, context):
    notifConsole(update, context)
    context.bot.send_message(chat_id=update.message.chat_id, text=open("help.txt", "r").read())

def calc(update, context):
    notifConsole(update, context)
    context.bot.send_chat_action(update.message.chat_id, 'upload_audio')
    infiles = []
    for c in update.message.text[6:]:
        if c == '/':c = 'd'
        if c == '*':c = 'x'
        if c in sound_files:
            infiles+=[soundPath+c+".wav"]
    outfile = soundPath+"v.wav"
    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(infiles)):
        output.writeframes(data[i][1])
    output.close()
    wav = outfile
    cmd = 'lame --preset insane %s' % wav
    subprocess.call(cmd, shell=True)
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(soundPath+"v.mp3", 'rb'))

########################################################################################################################################################
#                                                                RANDOM TEXTS                                                                          #
########################################################################################################################################################

def getQuote():
    text = requests.get('http://generateur.vuzi.fr/').text
    i = text.index('<span id="quotemarkContent">')
    j = text.index('</span>', i)
    return text[i+37:j-6]
def getInfo():
    text = requests.get('https://www.savoir-inutile.com/').text
    i = text.index('<h2 id="phrase"')
    j = text.index('</h2>', i)
    return text[i+39:j]
def sendMessage(update, context, fun):
    param = chat_id=update.message.text.split(' ')
    ci = update.message.chat_id
    if len(param) >= 2:
        a = int(param[1])
        if a != 0:
            ci = a
    n = 1
    if len(param) >= 3:
        n = int(param[2])
    troll = n > 10
    if len(param) >= 4:
        troll = param[3]!="false"
    remove_l = []
    for i in range(n):
        m = context.bot.send_message(chat_id=ci, text=fun())
        if troll:
            remove_l = remove_l+[m.message_id]
    for id in remove_l:
        context.bot.delete_message(ci, id)
    if troll:
        context.bot.send_video(chat_id=ci, video=dataServerAddress+"nounours_en_fait_non.mp4", supports_streaming=True)
def info(update, context):
    notifConsole(update, context)
    sendMessage(update, context, getInfo)
def quote(update, context):
    notifConsole(update, context)
    sendMessage(update, context, getQuote)

########################################################################################################################################################
#                                                              OTHER COMMANDS                                                                          #
########################################################################################################################################################

def alban(update, context):
    pack = context.bot.get_sticker_set("ROBOT20")
    context.bot.sendSticker(chat_id=update.message.chat_id, sticker=pack.stickers[random.randint(0, 4)])

def rapport(update, context):
    msg = update.message
    today = datetime.now()
    d = datetime(2020, 2, 12, 23, 59, 59, 999999)
    reste = d-today
    sec = reste.seconds
    if reste.days >= 0 and sec//3600>=0 and ((sec%3600)//60)>=0 and (sec%3600)%60>=0:
        context.bot.send_message(chat_id=msg.chat_id, text="Dépêche toi, il te reste "+str(reste.days)+" jours, "+str(sec//3600)+" heures, "+str((sec%3600)//60)+" minutes et "+str((sec%3600)%60)+" secondes pour finir ton rapport !")
    else:
        reste = today-d
        sec = reste.seconds
        context.bot.send_message(chat_id=msg.chat_id, text="Trop tard, il fallait rendre le rapport de projet robot il y a "+str(reste.days)+" jours, "+str(sec//3600)+" heures, "+str((sec%3600)//60)+" minutes et "+str((sec%3600)%60)+" secondes !")
        #context.bot.send_message(chat_id=msg.chat_id, text="C'est finiiiiiiiit!!!!!!")


def bowling(update, context):
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(soundPath+"liam_bowling.mp3", 'rb'))



########################################################################################################################################################
#                                                                    CHATBOT                                                                           #
########################################################################################################################################################

def getDataFiles():
    return [dataPath+f for f in os.listdir(dataPath) if os.path.isfile(os.path.join(dataPath, f))]

class LString:
    def __init__(self):
        self._total = 0
        self._successors = defaultdict(int)

    def put(self, word):
        self._successors[word] += 1
        self._total += 1

    def get_random(self):
        ran = random.randint(0, self._total - 1)
        for key, value in self._successors.items():
            if ran < value:
                return key
            else:
                ran -= value

couple_words = defaultdict(LString)

def load(phrasesFiles):
    global couple_words
    couple_words = defaultdict(LString)
    for phrases in phrasesFiles:
        with open(phrases, 'r', encoding="utf8") as f:
            for line in f:
                """
                if line[0] == '[':
                    line = line.split(':')[3]
                    #message = re.sub(r'[^\w\s\']', '', line).lower().strip()
                    #print(message)
                    add_message(line)
                """
                add_message(line)

def add_message(message):
    message = re.sub(r'[^\w\s\']', '', message).lower().strip()
    words = message.split()
    if len(words) < 2:
        return
    for i in range(2, len(words)):
        couple_words[(words[i - 2], words[i - 1])].put(words[i])
    couple_words[(words[-2], words[-1])].put("")

def generate():
    result = []
    while len(result) < 7 or len(result) > 20:
        result = []
        l = [i for i in couple_words.keys()]
        s = random.choice(l)
        result.extend(s)
        while result[-1]:
            w = couple_words[(result[-2], result[-1])].get_random()
            result.append(w)
    return " ".join(result)

def setChat(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=generate().replace('apos', '\''))
    #notifConsole(update, context)
    #if update.message.from_user.id == super_admin:
    #global chatbot_enable
    #chatbot_enable = not(chatbot_enable)
    #context.bot.send_message(chat_id=update.message.chat_id, text=str(chatbot_enable))

def loadData(update, context):
    load(getDataFiles())
load(getDataFiles())

########################################################################################################################################################
#                                                                       MAIN                                                                           #
########################################################################################################################################################

#Quoteirbot
#834389299:AAH1PThvlI1k03OJ8_WEle4MrdRZVjP6gQ0
#Tobrie:
#720838667:AAGZLMgYiik_io66Su2-COVQ20SOkGOcCYE

def main():
    TOKEN='834389299:AAH1PThvlI1k03OJ8_WEle4MrdRZVjP6gQ0' if TEST else '720838667:AAGZLMgYiik_io66Su2-COVQ20SOkGOcCYE'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    #dp.add_handler(MessageHandler(Filters.video, handleVideo))
    dp.add_handler(MessageHandler(Filters.text, handleText))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_handler(CommandHandler('list',list))
    dp.add_handler(CommandHandler('dico',dico))
    dp.add_handler(CommandHandler('dico2',dico2))
    #dp.add_handler(CommandHandler('w',wideo))
    dp.add_handler(CommandHandler('msg',msg))
    dp.add_handler(CommandHandler('help',help))
    #dp.add_handler(CommandHandler('link',link))
    dp.add_handler(CommandHandler('calc',calc))
    dp.add_handler(CommandHandler('meme',meme))
    dp.add_handler(CommandHandler('info',info))
    dp.add_handler(CommandHandler('quote',quote))
    dp.add_handler(CommandHandler('id',id_print))
    dp.add_handler(CommandHandler('di', setDI))
    dp.add_handler(CommandHandler('video', setAutoReply))
    dp.add_handler(CommandHandler('alban',alban))
    dp.add_handler(CommandHandler('rapport',rapport))
    dp.add_handler(CommandHandler('update',update_video_names_command))
    dp.add_handler(CommandHandler('bowling',bowling))

    #dp.add_handler(CommandHandler('play',play))

    dp.add_handler(CommandHandler('chat',setChat))
    dp.add_handler(CommandHandler('loadData',loadData))

    #Admin commands
    #dp.add_handler(CommandHandler('add',add))
    #dp.add_handler(CommandHandler('rm',rm))
    #dp.add_handler(CommandHandler('mv',mv))

    #Personal commands
    dp.add_handler(CommandHandler('conv', conv))

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
