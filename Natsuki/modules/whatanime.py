import asyncio
import datetime
import html
import os
import tempfile
import time
from datetime import timedelta
from decimal import Decimal
from urllib.parse import quote as urlencode

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

from Natsuki import pbot

session = aiohttp.ClientSession()
progress_callback_data = {}


def format_bytes(size):
    size = int(size)
    # 2**10 = 1024
    power = 1024
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]+'B'}"


def return_progress_string(current, total):
    filled_length = int(30 * current // total)
    return "[" + "=" * filled_length + " " * (30 - filled_length) + "]"


def calculate_eta(current, total, start_time):
    if not current:
        return "00:00:00"
    end_time = time.time()
    elapsed_time = end_time - start_time
    seconds = (elapsed_time * (total / current)) - elapsed_time
    thing = "".join(str(timedelta(seconds=seconds)).split(".")[:-1]).split(", ")
    thing[-1] = thing[-1].rjust(8, "0")
    return ", ".join(thing)


@pbot.on_message(filters.command("whatanime"))
async def whatanime(c: Client, m: Message):
    media = m.photo or m.animation or m.video or m.document
    if not media:
        reply = m.reply_to_message
        if not getattr(reply, "empty", True):
            media = reply.photo or reply.animation or reply.video or reply.document
    if not media:
        await m.reply_text("Photo or GIF or Video required")
        return
    with tempfile.TemporaryDirectory() as tempdir:
        reply = await m.reply_text("Downloading...")
        path = await c.download_media(
            media,
            file_name=os.path.join(tempdir, "0"),
            progress=progress_callback,
            progress_args=(reply,),
        )
        new_path = os.path.join(tempdir, "1.png")
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-i", path, "-frames:v", "1", new_path
        )
        await proc.communicate()
        await reply.edit_text("Uploading...")
        with open(new_path, "rb") as file:
            async with session.post(
                "https://trace.moe/api/search", data={"image": file}
            ) as resp:
                json = await resp.json()
    if isinstance(json, str):
        await reply.edit_text(html.escape(json))
    else:
        try:
            match = next(iter(json["docs"]))
        except StopIteration:
            await reply.edit_text("No match")
        else:
            nsfw = match["is_adult"]
            title_native = match["title_native"]
            title_english = match["title_english"]
            title_romaji = match["title_romaji"]
            synonyms = ", ".join(match["synonyms"])
            filename = match["filename"]
            tokenthumb = match["tokenthumb"]
            anilist_id = match["anilist_id"]
            episode = match["episode"]
            similarity = match["similarity"]
            from_time = (
                str(datetime.timedelta(seconds=match["from"]))
                .split(".", 1)[0]
                .rjust(8, "0")
            )
            to_time = (
                str(datetime.timedelta(seconds=match["to"]))
                .split(".", 1)[0]
                .rjust(8, "0")
            )
            at_time = match["at"]
            text = f'<a href="https://anilist.co/anime/{anilist_id}">{title_romaji}</a>'
            if title_english:
                text += f" ({title_english})"
            if title_native:
                text += f" ({title_native})"
            if synonyms:
                text += f"\n<b>Synonyms:</b> {synonyms}"
            text += f'\n<b>Similarity:</b> {(Decimal(similarity) * 100).quantize(Decimal(".01"))}%\n'
            if episode:
                text += f"<b>Episode:</b> {episode}\n"
            if nsfw:
                text += "<b>Hentai/NSFW:</b> no"

            async def _send_preview():
                url = f"https://media.trace.moe/video/{anilist_id}/{urlencode(filename)}?t={at_time}&token={tokenthumb}"
                with tempfile.NamedTemporaryFile() as file:
                    async with session.get(url) as resp:
                        while True:
                            chunk = await resp.content.read(10)
                            if not chunk:
                                break
                            file.write(chunk)
                    file.seek(0)
                    try:
                        await reply.reply_video(
                            file.name, caption=f"{from_time} - {to_time}"
                        )
                    except Exception:
                        await reply.reply_text("Cannot send preview :/")

            await asyncio.gather(
                reply.edit_text(text, disable_web_page_preview=True), _send_preview()
            )


async def progress_callback(current, total, reply):
    message_identifier = (reply.chat.id, reply.message_id)
    last_edit_time, prevtext, start_time = progress_callback_data.get(
        message_identifier, (0, None, time.time())
    )
    if current == total:
        try:
            progress_callback_data.pop(message_identifier)
        except KeyError:
            pass
    elif (time.time() - last_edit_time) > 1:
        if last_edit_time:
            download_speed = format_bytes(
                (total - current) / (time.time() - start_time)
            )
        else:
            download_speed = "0 B"
        text = f"""Downloading...
<code>{return_progress_string(current, total)}</code>

<b>Total Size:</b> {format_bytes(total)}
<b>Downladed Size:</b> {format_bytes(current)}
<b>Download Speed:</b> {download_speed}/s
<b>ETA:</b> {calculate_eta(current, total, start_time)}"""
        if prevtext != text:
            await reply.edit_text(text)
            prevtext = text
            last_edit_time = time.time()
            progress_callback_data[message_identifier] = (
                last_edit_time,
                prevtext,
                start_time,
            )
