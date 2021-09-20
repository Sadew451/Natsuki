import os
from pyrogram import Client, filters
from pyrogram.types import *

from Natsuki.config import get_str_key
from Natsuki import pbot

REPO_TEXT = "**A Powerful BOT to Make Your Groups Secured and Organized ! \n\n↼ Øwñêr ⇀ : 『 @TeamNatsuki 』\n╭──────────────\n┣─ » Python ~ 3.8.6\n┣─ » Update ~ Resently\n╰──────────────\n\n»»» @TheNatsukiBot «««"
  
BUTTONS = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("Repository", url=f"https://github.com/Sadew451/Natsuki"),
        InlineKeyboardButton("Watch Tutorial ", url=f"https://youtu.be/YyiO6jdPzXg"),
      ],[
        InlineKeyboardButton("Natsuki News", url="https://t.me/Natsuki_News"),
        InlineKeyboardButton("Natsuki Support", url="https://t.me/NatsukiSupport_Official"),
      ],[
        InlineKeyboardButton("Main Channel", url="https://t.me/SDBOTs_Inifinity"),
        InlineKeyboardButton("Developer", url="https://t.me/TeamNatsuki"),
      ]]
    )
  
  
@pbot.on_message(filters.command(["repo"]))
async def repo(pbot, update):
    await update.reply_text(
        text=REPO_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
