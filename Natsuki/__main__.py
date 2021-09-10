import html
import importlib
import json
import re
import time
import traceback
from sys import argv
from typing import Optional

from telegram import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
    Update,
    User,
)
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown

from Natsuki import (
    ALLOW_EXCL,
    BL_CHATS,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    WHITELIST_CHATS,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Natsuki.modules import ALL_MODULES
from Natsuki.modules.helper_funcs.alternate import typing_action
from Natsuki.modules.helper_funcs.chat_status import is_user_admin
from Natsuki.modules.helper_funcs.misc import paginate_modules
from Natsuki.modules.helper_funcs.readable_time import get_readable_time

PM_START_TEXT = """
👋 Hello There, I'm 𝗡𝗮𝘁𝘀𝘂𝗸𝗶. I'm a Powerfull Group Manager Bot With Cool Modules. @TeamNatsuki

Guys. /help to Find My List Of Available Commands 🙋‍♂️

"""

buttons = [
    [
        InlineKeyboardButton(
            text="Natsuki News 🙋‍♂️", url="https://t.me/Natsuki_Updates"
        ),
        InlineKeyboardButton(
            text="Support Group 💬", url="https://t.me/NatsukiSupport_Official"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Source 🗒", url="Github.com/Sadew451"
        ),
        InlineKeyboardButton(
            text="Command Help ❓", url="http://t.me/TheNatsukiBot?start=help"
        ),
    ],
    [
        InlineKeyboardButton(
            text="➕ Add To Me Your Group ➕",
            url="t.me/TheNatsukiBot?startgroup=true",
        ),
    ],
]

NATSUKI_IMG = "https://telegra.ph/file/a6281ecaae26667a13716.png"

HELP_STRINGS = f"""
*ALL Commands :* [❤]()

✨ Every possibility of Natsuki is documentated here.
🙋‍♀️ Click buttons to get Thanks.
""".format(
    dispatcher.bot.first_name,
    "" if not ALLOW_EXCL else "\nAll commands can either be used with / or !.\n",
)


DONATE_STRING = """Heya, glad to hear you want to donate!
You can donate to the original writer's of the Base code,
Support them  [SADEW JAYASEKARA](t.me/Darkridersslk)"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
USER_BOOK = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Natsuki.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__user_book__"):
        USER_BOOK.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )


@run_async
def test(update, context):
    try:
        print(update)
    except:
        pass
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            update.effective_user.first_name
            update.effective_message.reply_text(
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_text(
            "I'm awake already!\n<b>Haven't slept since:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*⚊❮❮❮❮ ｢  Help  for  {}  module 」❯❯❯❯⚊*\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in help buttons. %s", str(query.data))


@run_async
def Natsuki_about_callback(update, context):
    query = update.callback_query
    if query.data == "aboutmanu_":
        query.message.edit_text(
            text=f"* Hi There  The name's {dispatcher.bot.first_name} \n\nAs  You I'm a next generational group management bot developed by Natsuki Updates.* "
            f"\n\n Join [NatsukiUpdates](https://t.me/Natsuki_Updates) To Keep Yourself Updated About {dispatcher.bot.first_name}"
            f"\n\n I have the normal GROUP MANAGING functions like flood control, a warning system etc but I mainly have the advanced and handy Antispam system and the SIBYL banning system which safegaurds and helps your group from spammers."
            f"\n\nI Can Manage Your Groups Smoothly, With Some Special Features"
            f"\n\nYou Can Know More About Me By Clicking The Below Buttons",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🙋‍♀️ How To Use Me", callback_data="aboutmanu_howto"
                        ),
                        InlineKeyboardButton(
                            text="🗒 Terms and Conditions", callback_data="aboutmanu_tac"
                        ),
                    ],
                    [InlineKeyboardButton(text="Help ❔", callback_data="help_back")],
                    [InlineKeyboardButton(text="Back", callback_data="aboutmanu_back")],
                ]
            ),
        )
    elif query.data == "aboutmanu_back":
        query.message.edit_text(
            PM_START_TEXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
        )

    elif query.data == "aboutmanu_howto":
        query.message.edit_text(
            text=f"* ｢ BASIC HELP 」*"
            f"\nIf You Can Also Add {dispatcher.bot.first_name} To Your Chats By Clicking [Here](http://t.me/{dispatcher.bot.username}?startgroup=true) And Selecting Chat. \n"
            f"\n\nYou Can get support {dispatcher.bot.first_name} by joining [Natsuki Support](https://t.me/NatsukiSupport_Official).\n"
            f"",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Admins", callback_data="aboutmanu_permis"
                        ),
                        InlineKeyboardButton(text="Help", callback_data="help_back"),
                    ],
                    [InlineKeyboardButton(text="Back", callback_data="aboutmanu_")],
                ]
            ),
        )
    elif query.data == "aboutmanu_credit":
        query.message.edit_text(
            text=f"*{dispatcher.bot.first_name} Is the redisigned version of Daisy and Naruto for the best performance.*"
            f"\n\nBased on [SDBOTsInifinity](https://t.me/SDBOTs_Inifinity)."
            f"\n\n{dispatcher.bot.first_name}'s source code was written by Sadew Jayasekara"
            f"\n\nIf Any Question About {dispatcher.bot.first_name}, \nLet Us Know At @{SUPPORT_CHAT}.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="aboutmanu_tac")]]
            ),
        )

    elif query.data == "aboutmanu_permis":
        query.message.edit_text(
            text=f"<b> ｢ Admin Permissions 」</b>"
            f"\nTo avoid slowing down, {dispatcher.bot.first_name} caches admin rights for each user. This cache lasts about 10 minutes; this may change in the future. This means that if you promote a user manually (without using the /promote command), {dispatcher.bot.first_name} will only find out ~10 minutes later."
            f"\n\nIF you want to update them immediately, you can use the /admincache command,thta'll force {dispatcher.bot.first_name} to check who the admins are again and their permissions"
            f"\n\nIf you are getting a message saying:"
            f"\n<Code>You must be this chat administrator to perform this action!</code>"
            f"\nThis has nothing to do with {dispatcher.bot.first_name}'s rights; this is all about YOUR permissions as an admin. {dispatcher.bot.first_name} respects admin permissions; if you do not have the Ban Users permission as a telegram admin, you won't be able to ban users with {dispatcher.bot.first_name}. Similarly, to change {dispatcher.bot.first_name} settings, you need to have the Change group info permission."
            f"\n\nThe message very clearly says that you need these rights - <i>not {dispatcher.bot.first_name}.</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]
            ),
        )
    elif query.data == "aboutmanu_spamprot":
        query.message.edit_text(
            text="* ｢ Anti-Spam Settings 」*"
            "\n- /antispam <on/off/yes/no>: Change antispam security settings in the group, or return your current settings(when no arguments)."
            "\n_This helps protect you and your groups by removing spam flooders as quickly as possible._"
            "\n\n- /setflood <int/'no'/'off'>: enables or disables flood control"
            "\n- /setfloodmode <ban/kick/mute/tban/tmute> <value>: Action to perform when user have exceeded flood limit. ban/kick/mute/tmute/tban"
            "\n_Antiflood allows you to take action on users that send more than x messages in a row. Exceeding the set flood will result in restricting that user._"
            "\n\n- /addblacklist <triggers>: Add a trigger to the blacklist. Each line is considered one trigger, so using different lines will allow you to add multiple triggers."
            "\n- /blacklistmode <off/del/warn/ban/kick/mute/tban/tmute>: Action to perform when someone sends blacklisted words."
            "\n_Blacklists are used to stop certain triggers from being said in a group. Any time the trigger is mentioned, the message will immediately be deleted. A good combo is sometimes to pair this up with warn filters!_"
            "\n\n- /reports <on/off>: Change report setting, or view current status."
            "\n • If done in pm, toggles your status."
            "\n • If in chat, toggles that chat's status."
            "\n_If someone in your group thinks someone needs reporting, they now have an easy way to call all admins._"
            "\n\n- /lock <type>: Lock items of a certain type (not available in private)"
            "\n- /locktypes: Lists all possible locktypes"
            "\n_The locks module allows you to lock away some common items in the telegram world; the bot will automatically delete them!_"
            '\n\n- /addwarn <keyword> <reply message>: Sets a warning filter on a certain keyword. If you want your keyword to be a sentence, encompass it with quotes, as such: /addwarn "very angry" This is an angry user. '
            "\n- /warn <userhandle>: Warns a user. After 3 warns, the user will be banned from the group. Can also be used as a reply."
            "\n- /strongwarn <on/yes/off/no>: If set to on, exceeding the warn limit will result in a ban. Else, will just kick."
            "\n_If you're looking for a way to automatically warn users when they say certain things, use the /addwarn command._"
            "\n\n- /welcomemute <off/soft/strong>: All users that join, get muted"
            "\n_ A button gets added to the welcome message for them to unmute themselves. This proves they aren't a bot! soft - restricts users ability to post media for 24 hours. strong - mutes on join until they prove they're not bots._",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="aboutmanu_howto")]]
            ),
        )
    elif query.data == "aboutmanu_tac":
        query.message.edit_text(
            text=f"<b> ｢ Terms and Conditions 」</b>\n"
            f"\n<i>To Use This Bot, You Need To Read Terms and Conditions Carefully.</i>\n"
            f"\n✪ We always respect your privacy \n  We never log into bot's api and spying on you \n  We use a encripted database \n  Bot will automatically stops if someone logged in with api."
            f"\n✪ Always try to keep credits, so \n  This hardwork is done by Natsuki Updates team spending many sleepless nights.. So, Respect it."
            f"\n✪ Some modules in this bot is owned by different authors, So, \n  All credits goes to them \n  Also for <b>Paul Larson for Marie</b>."
            f"\n✪ If you need to ask anything about \n  this bot, Go @{SUPPORT_CHAT}."
            f"\n✪ If you asking nonsense in Support \n  Chat, you will get warned/banned."
            f"\n✪ All api's we used owned by originnal authors \n  Some api's we use Free version \n  Please don't overuse AI Chat."
            f"\n✪ We don't Provide any support to forks,\n  So these terms and conditions not applied to forks \n  If you are using a fork of TheNatsukiBot we are not resposible for anything."
            f"\n\nFor any kind of help, related to this bot, Join @{SUPPORT_CHAT}."
            f"\n\n<i>Terms & Conditions will be changed anytime</i>\n",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Credits", callback_data="aboutmanu_credit"
                        ),
                        InlineKeyboardButton(text="Back", callback_data="aboutmanu_"),
                    ]
                ]
            ),
        )


@run_async
@typing_action
def get_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Support Chat",
                            url="https://t.me/{}".format(SUPPORT_CHAT),
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update, context):
    query = update.callback_query
    user = update.effective_user
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = context.bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                "Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(chat.title),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                "Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(chat.title),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = context.bot.get_chat(chat_id)
            query.message.edit_text(
                text="Hi there! There are quite a few settings for *{}* - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()
    except Exception as excp:
        if excp.message == "Message is not modified":
            pass
        elif excp.message == "Query_id_invalid":
            pass
        elif excp.message == "Message can't be deleted":
            pass
        else:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Settings",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update, context):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def is_chat_allowed(update, context):
    if len(WHITELIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id not in WHITELIST_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(BL_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BL_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat! Leaving..."
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(WHITELIST_CHATS) != 0 and len(BL_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BL_CHATS:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Unallowed chat, leaving"
            )
            try:
                context.bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    else:
        pass


@run_async
def donate(update: Update, context: CallbackContext):
    update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
        update.effective_message.reply_text(
            "You can also donate to the person currently running me "
            "[here]({})".format(DONATION_LINK),
            parse_mode=ParseMode.MARKDOWN,
        )

    else:
        pass


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "I am now online ❤")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    # test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start, pass_args=True)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Natsuki_about_callback, pattern=r"aboutmanu_"
    )

    donate_handler = CommandHandler("donate", donate)

    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)
    is_chat_allowed_handler = MessageHandler(Filters.group, is_chat_allowed)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(is_chat_allowed_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)
            client.run_until_disconnected()

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
