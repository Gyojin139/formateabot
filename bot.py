import colorsys
import io
import logging
import random
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedSticker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import InlineQueryHandler

from text_editor import TextEditor
from word_art import create_text_gradient

logging.basicConfig(filename='app.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


with open('token.txt', 'r') as f:
    token = f.read().strip()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

with open('sticker_dumper.txt', 'r') as f:
    sticker_dumper_id = f.read()

MAX_LEN = 100

def fraktur(update, context):
    text = TextEditor.fraktur(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def cursive(update, context):
    text = TextEditor.cursive(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def sans(update, context):
    text = TextEditor.sans(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def squared(update, context):
    text = TextEditor.squared(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def doublestruck(update, context):
    text = TextEditor.doublestruck(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def circled(update, context):
    text = TextEditor.circled(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def cursed(update, context):
    text = TextEditor.cursed(' '.join(context.args))
    if text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")


def sticker(update, context):
    text = ' '.join(context.args)
    if text:
        if len(text) > MAX_LEN:
            context.bot.send_message(chat_id=update.effective_chat.id, text="That's a very long text for the sticker")
            return
        image = create_sticker(text)
        with io.BytesIO() as bytes_io:
            image.save(bytes_io, format='webp')
            bytes_io.seek(0)
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=bytes_io)
            return
    context.bot.send_message(chat_id=update.effective_chat.id, text="I need some text to convert")

def log_stuff(update, context):
    logging.info(context.chat_data)
    logging.info(context.user_data)
    logging.info(update.effective_chat.id)


def create_sticker(text):
    return create_text_gradient(
        text, 512, 512,
        *[list(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(random.random(), 1, 1)))
          for _ in range(random.randint(2, 6))])


def get_sticker_id(bot, text):
    image = create_sticker(text)
    with io.BytesIO() as bytes_io:
        image.save(bytes_io, format='webp')
        bytes_io.seek(0)
        sent_sticker = bot.send_sticker(sticker_dumper_id, bytes_io)
    return sent_sticker.sticker.file_id


def inline_fraktur(update, context):
    query = update.inline_query.query
    if not query or len(query) > MAX_LEN:
        return
    results = [InlineQueryResultArticle(
        id=uuid4(),
        title='Fraktur',
        input_message_content=InputTextMessageContent(TextEditor.fraktur(query)),
        description=TextEditor.fraktur(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Cursive',
        input_message_content=InputTextMessageContent(TextEditor.cursive(query)),
        description=TextEditor.cursive(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Sans',
        input_message_content=InputTextMessageContent(TextEditor.sans(query)),
        description=TextEditor.sans(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Circled',
        input_message_content=InputTextMessageContent(TextEditor.circled(query)),
        description=TextEditor.circled(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Squared',
        input_message_content=InputTextMessageContent(TextEditor.squared(query)),
        description=TextEditor.squared(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Doublestruck',
        input_message_content=InputTextMessageContent(TextEditor.doublestruck(query)),
        description=TextEditor.doublestruck(query),
    ), InlineQueryResultArticle(
        id=uuid4(),
        title='Cursed',
        input_message_content=InputTextMessageContent(TextEditor.cursed(query)),
        description=TextEditor.cursed(query),
    ), InlineQueryResultCachedSticker(
        id=uuid4(),
        sticker_file_id=get_sticker_id(updater.bot, query),
    )]
    context.bot.answer_inline_query(update.inline_query.id, results)


def send_help(update, context):
    text = """/fraktur - 𝖂𝖗𝖎𝖙𝖊𝖘 𝖙𝖊𝖝𝖙 𝖎𝖓 𝖋𝖗𝖆𝖐𝖙𝖚𝖗
/cursive - 𝓦𝓻𝓲𝓽𝓮𝓼 𝓽𝓮𝔁𝓽 𝓲𝓷 𝓬𝓾𝓻𝓼𝓲𝓿𝓮
/sans - 𝖶𝗋𝗂𝗍𝖾𝗌 𝗍𝖾𝗑𝗍 𝗂𝗇 𝗌𝖺𝗇𝗌
/circled - Ⓦⓡⓘⓣⓔⓢ ⓒⓘⓡⓒⓛⓔⓓ ⓣⓔⓧⓣ
/squared - 🅆🅁🄸🅃🄴🅂 🅂🅀🅄🄰🅁🄴🄳 🅃🄴🅇🅃
/doublestruck - 𝕎𝕣𝕚𝕥𝕖𝕤 𝕥𝕖𝕩𝕥 𝕚𝕟 𝕕𝕠𝕦𝕓𝕝𝕖 𝕤𝕥𝕣𝕦𝕔𝕜
/cursed - W͉̩͂́͜͟ṛ̥͒ͦ̅̕i̝͌̀͝te͂s̩̎ͨ͞ ̯̈cu̶̹̤͔̻͇ͨ̉ͧ́͐̊͆̏ͮ̿͑̕͢͞ͅr͖s̬̠ͨ͐ͫe̺d̴͇ ̣͎te̔x̸͖̑̇t
/sticker - Sends a beautiful sticker with your text

It also works inline! Try writing @FormateaBot in another chat"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


dispatcher.add_handler(InlineQueryHandler(inline_fraktur))
dispatcher.add_handler(CommandHandler('fraktur', fraktur))
dispatcher.add_handler(CommandHandler('cursive', cursive))
dispatcher.add_handler(CommandHandler('sans', sans))
dispatcher.add_handler(CommandHandler('circled', circled))
dispatcher.add_handler(CommandHandler('squared', squared))
dispatcher.add_handler(CommandHandler('cursed', cursed))
dispatcher.add_handler(CommandHandler('doublestruck', doublestruck))
dispatcher.add_handler(CommandHandler('sticker', sticker))
dispatcher.add_handler(CommandHandler('help', send_help))
dispatcher.add_handler(MessageHandler(Filters.text, log_stuff))

if __name__ == '__main__':
    logging.info('Bot is online!')
    updater.start_polling()
    updater.idle()
