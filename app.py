#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, Document, Emoji
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, InlineQueryHandler
import logging, requests, urllib2
import json, re
import cnetoken
from random import randint
from uuid import uuid4

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

headers = {
    'User-Agent': '@CNEREPBot Telegram bot telegram.me/CNEREPBot',
    'From': 'celisflenbers@gmail.com'
    }

def get_data(nac, cedula):
    r = requests.get(r'http://cne.gob.ve/consultamovil?nacionalidad=%s&cedula=%s&tipo=RE'%(nac,cedula), headers=headers)
    #r.encoding = 'utf-8'

    result = {}

    if str(r.status_code) == '200':
        #print r.headers['content-type']
        #print r.encoding
        #print r.text

        data = r.json()
        #print data

        status = unicode(data['st'])
        obj = unicode(data['obj'])

        if data['st'] == '':
            result = {
                'st' : '',\

                'ci' : data['ci'], \
                'nb' : data['nb'], \
                'nb1' : data['nb1'], \
                'nb2' : data['nb2'], \
                'ap1' : data['ap1'], \
                'ap2' : data['ap2'], \
                'fn' : data['fecha_nacimiento'],\

                'cv' : data['cv'],\
                'di' : data['dir'],\
                'est' : data['stdo'],\
                'mun' : data['mcp'],\
                'par' : data['par'],\
            }
        else:
            result = {
                'st' : status,\
                'ob' : obj,\

                'ci' : data['ci'], \
                'nb' : data['nb'], \
           }

    return result

def rep(bot, update):

    rep_req = update.message.text[5:]
    nac = rep_req[0:1].upper()
    ci = rep_req[1:]
    #print '{nac}-{ci}'.format(nac=nac,ci=ci)

    data = get_data(nac, ci)
    #print 'rep {data}\n'.format(data=data)

    coletilla = "\n\nVer más detalles en <a href='http://cne.gob.ve/web/registro_electoral/ce.php?nacionalidad={nac}&cedula={ci}'>CNE Consulta</a>"
    if data['st'] == '':
        bot.sendMessage(chat_id=update.message.chat_id, text="<b>Cédula:</b> {nac}-{ci}\n<b>Nombre:</b> {nb}\n<b>Fecha Nacimiento:</b> {fn}\n\n<b>{school}CENTRO DE VOTACIÓN</b>\n{cv}\n{di}{col}".format(col= coletilla, school = Emoji.SCHOOL, nac=nac, ci = ci, nb = data['nb'], fn = data['fn'], cv = data['cv'], di = data['di']), parse_mode='html')
    else:
        #obj
        bot.sendMessage(chat_id=update.message.chat_id, text=u"<b>Cédula:</b> {nac}-{ci}\n<b>Nombre:</b> {nb}\n\n<b>Estatus:</b> <i>{st}</i>\n\t{noentry}<b>Objeción:</b> <i>{ob}</i>{col}".format(col = coletilla.decode('unicode-escape'), nac=nac, ci = ci, nb = data['nb'], st = data['st'], ob = data['ob'], noentry = Emoji.NO_ENTRY.decode('unicode-escape')), parse_mode='html')



def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hola! Este bot buscara la cédula que desee en la web del CNE", parse_mode='html')

def ayuda(bot, update):
    bot.sendMessage(update.message.chat_id, text="Para buscar escriba /rep con la cédula a buscar /rep V12345678", parse_mode='html')

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text="Error, por favor escriba una cédula válida")

def acerca(bot, update):
    bot.sendMessage(update.message.chat_id, text='Creado por @CelisFlen_Bers en Python con la ayuda del API del www.cne.gob.ve')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"\n' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(cnetoken.bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("ayuda", ayuda))
    dp.addHandler(CommandHandler("rep", rep))
    dp.addHandler(CommandHandler("acerca", acerca))

    # inline query
    #dp.addHandler(InlineQueryHandler(search))


    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
