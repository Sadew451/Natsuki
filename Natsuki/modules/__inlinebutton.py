import os
from pyrogram import Client, filters
from pyrogram.types import *

from Natsuki import pbot

TEXT = "Click A Button To Get Started.👋 This is Natsuki inline „\nAn Advanced Inline  Bot For All Your Needs !!\n\n↼ Øwñêr ⇀ : 『 @Darkridersslk 』\n╭──────────────\n┣─ » Python ~ 3.8.6\n┣─ » Update ~ Recently\n╰──────────────\n\n»»» @TheNatsukiBot «««"

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("Alive", switch_inline_query_current_chat="alive"),
        InlineKeyboardButton("Youtube", switch_inline_query_current_chat="yt"),
        InlineKeyboardButton("tr", switch_inline_query_current_chat="tr"),
        InlineKeyboardButton("modapk", switch_inline_query_current_chat="modapk")
        ],[
        InlineKeyboardButton("ud", switch_inline_query_current_chat="ud"),
        InlineKeyboardButton("google", switch_inline_query_current_chat="google"),
        InlineKeyboardButton("webss", switch_inline_query_current_chat="webss"),
        InlineKeyboardButton("bitly", switch_inline_query_current_chat="bitly")
        ],[
        InlineKeyboardButton("wall", switch_inline_query_current_chat="wall"),
        InlineKeyboardButton("pic", switch_inline_query_current_chat="pic"),
        InlineKeyboardButton("saavn", switch_inline_query_current_chat="saavn"),
        InlineKeyboardButton("deezer", switch_inline_query_current_chat="deezer")
        ],[
        InlineKeyboardButton("torrent", switch_inline_query_current_chat="torrent"),
        InlineKeyboardButton("reddit", switch_inline_query_current_chat="reddit"),
        InlineKeyboardButton("imdb", switch_inline_query_current_chat="imdb"),
        InlineKeyboardButton("spaminfo", switch_inline_query_current_chat="spaminfo"),
        ],[
        InlineKeyboardButton("lyrics", switch_inline_query_current_chat="lyrics"),
        InlineKeyboardButton("paste", switch_inline_query_current_chat="paste"),
        InlineKeyboardButton("define", switch_inline_query_current_chat="define"),
        InlineKeyboardButton("synonyms", switch_inline_query_current_chat="synonyms"),
        ],[
        InlineKeyboardButton("antonyms", switch_inline_query_current_chat="antonyms"),
        InlineKeyboardButton("country", switch_inline_query_current_chat="country"),
        InlineKeyboardButton("cs", switch_inline_query_current_chat="cs"),
        InlineKeyboardButton("fakegen", switch_inline_query_current_chat="fakegen"),
        ],[
        InlineKeyboardButton("weather", switch_inline_query_current_chat="weather"),
        InlineKeyboardButton("datetime", switch_inline_query_current_chat="datetime"),
        InlineKeyboardButton("app", switch_inline_query_current_chat="app"),
        InlineKeyboardButton("Github", switch_inline_query_current_chat="gh"),
        ],[
        InlineKeyboardButton("so ", switch_inline_query_current_chat="so"),
        InlineKeyboardButton("wiki", switch_inline_query_current_chat="wiki"),
        InlineKeyboardButton("ping", switch_inline_query_current_chat="ping"),
        InlineKeyboardButton("pokedex", switch_inline_query_current_chat="pokedex"),
        ]]
    )

@pbot.on_message(filters.command(["inline"]))
async def finline(pbot, update):
    await update.reply_text(
        text=TEXT,    
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )

@pbot.on_inline_query()
async def line(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "menus":
        await client.answer_inline_query(
            query.id,
            results=menus,            
            switch_pm_text={menus},
            cache_time=0,
        )


# ==================#
# Testing plugin 

menus = [
    InlineQueryResultArticle(title="Inline commands", description="Inline commands",
                             input_message_content=InputTextMessageContent("/inline")),
    InlineQueryResultArticle(title="Start Bot", description="Start Bot",
                             input_message_content=InputTextMessageContent("/start")),
]
