import os

import cloudmersive_virus_api_client
from pymongo import MongoClient
from Natsuki.tl import functions, types
from Natsuki.tl.types import DocumentAttributeFilename, MessageMediaDocument

from Natsuki import MONGO_DB_URI, VIRUS_API_KEY
from Natsuki import telethn as tbot
from Natsuki.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


configuration = cloudmersive_virus_api_client.Configuration()
configuration.api_key["Apikey"] = VIRUS_API_KEY
api_instance = cloudmersive_virus_api_client.ScanApi(
    cloudmersive_virus_api_client.ApiClient(configuration)
)
allow_executables = True
allow_invalid_files = True
allow_scripts = True
allow_password_protected_files = True


@register(pattern="^/scanit$")
async def virusscan(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    if not event.reply_to_msg_id:
        await event.reply("Reply to a file to scan it.")
        return

    c = await event.get_reply_message()
    try:
        c.media.document
    except Exception:
        await event.reply("Thats not a file.")
        return
    h = c.media
    try:
        k = h.document.attributes
    except Exception:
        await event.reply("Thats not a file.")
        return
    if not isinstance(h, MessageMediaDocument):
        await event.reply("Thats not a file.")
        return
    if not isinstance(k[0], DocumentAttributeFilename):
        await event.reply("Thats not a file.")
        return
    try:
        virus = c.file.name
        await event.client.download_file(c, virus)
        gg = await event.reply("Scanning the file...")
        fsize = c.file.size
        if not fsize <= 3145700:  # MAX = 3MB
            await gg.edit("File size exceeds 3MB")
            return
        api_response = api_instance.scan_file_advanced(
            c.file.name,
            allow_executables=allow_executables,
            allow_invalid_files=allow_invalid_files,
            allow_scripts=allow_scripts,
            allow_password_protected_files=allow_password_protected_files,
        )
        if api_response.clean_result is True:
            await gg.edit("This file is safe ✔️\nNo virus detected 🐞")
        else:
            await gg.edit("This file is Dangerous ☠️️\nVirus detected 🐞")
        os.remove(virus)
    except Exception as e:
        print(e)
        os.remove(virus)
        await gg.edit("Some error occurred.")
        return
