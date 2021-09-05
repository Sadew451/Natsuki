from datetime import datetime

from gtts import gTTS
from telegram import ChatAction, Update
from telegram.ext import CallbackContext, run_async

from Natsuki import dispatcher
from Natsuki.modules.disable import DisableAbleCommandHandler


@run_async
def tts(update: Update, context: CallbackContext):
    args = context.args
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    datetime.now().strftime("%d%m%y-%H%M%S%f")
    reply = " ".join(args)
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    lang = "ml"
    tts = gTTS(reply, lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "en"
        tts = gTTS(reply, lang)
        tts.save("k.mp3")
    with open("k.mp3", "rb") as speech:
        update.message.reply_voice(speech, quote=False)


TTS_HANDLER = DisableAbleCommandHandler("tts", tts, pass_args=True)
dispatcher.add_handler(TTS_HANDLER)

__command_list__ = ["tts"]
__handlers__ = [TTS_HANDLER]
