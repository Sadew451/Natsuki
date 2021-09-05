from typing import List, Optional

from telegram import Message, MessageEntity
from telegram.error import BadRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from Natsuki import LOGGER
from Natsuki.modules.users import get_user_id


def id_from_reply(message):
    prev_message = message.reply_to_message
    if not prev_message:
        return None, None
    user_id = prev_message.from_user.id
    res = message.text.split(None, 1)
    if len(res) < 2:
        return user_id, ""
    return user_id, res[1]


def extract_user(message: Message, args: List[str]) -> Optional[int]:
    return extract_user_and_text(message, args)[0]


def extract_user_and_text(
    message: Message, args: List[str]
) -> (Optional[int], Optional[str]):
    prev_message = message.reply_to_message
    split_text = message.text.split(None, 1)

    if len(split_text) < 2:
        return id_from_reply(message)  # only option possible

    text_to_parse = split_text[1]

    text = ""

    entities = list(message.parse_entities([MessageEntity.TEXT_MENTION]))
    if len(entities) > 0:
        ent = entities[0]
    else:
        ent = None

    # if entity offset matches (command end/text start) then all good
    if entities and ent and ent.offset == len(message.text) - len(text_to_parse):
        ent = entities[0]
        user_id = ent.user.id
        text = message.text[ent.offset + ent.length :]

    elif len(args) >= 1 and args[0][0] == "@":
        user = args[0]
        user_id = get_user_id(user)
        if not user_id:
            message.reply_text(
                "I don't have that user in my db. You'll be able to interact with them if "
                "you reply to that person's message instead, or forward one of that user's messages."
            )
            return None, None

        else:
            user_id = user_id
            res = message.text.split(None, 2)
            if len(res) >= 3:
                text = res[2]

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])
        res = message.text.split(None, 2)
        if len(res) >= 3:
            text = res[2]

    elif prev_message:
        user_id, text = id_from_reply(message)

    else:
        return None, None

    try:
        message.bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in ("User_id_invalid", "Chat not found"):
            message.reply_text(
                "I don't seem to have interacted with this user before - please forward a message from "
                "them to give me control! (like a voodoo doll, I need a piece of them to be able "
                "to execute certain commands...)"
            )
        else:
            LOGGER.exception("Exception %s on user %s", excp.message, user_id)

        return None, None

    return user_id, text


def extract_text(message) -> str:
    return (
        message.text
        or message.caption
        or (message.sticker.emoji if message.sticker else None)
    )


def extract_unt_fedban(
    message: Message, args: List[str]
) -> (Optional[int], Optional[str]):
    prev_message = message.reply_to_message
    split_text = message.text.split(None, 1)

    if len(split_text) < 2:
        return id_from_reply(message)  # only option possible

    text_to_parse = split_text[1]

    text = ""

    entities = list(message.parse_entities([MessageEntity.TEXT_MENTION]))
    if len(entities) > 0:
        ent = entities[0]
    else:
        ent = None

    # if entity offset matches (command end/text start) then all good
    if entities and ent and ent.offset == len(message.text) - len(text_to_parse):
        ent = entities[0]
        user_id = ent.user.id
        text = message.text[ent.offset + ent.length :]

    elif len(args) >= 1 and args[0][0] == "@":
        user = args[0]
        user_id = get_user_id(user)
        if not user_id and not str(user_id).isdigit():
            message.reply_text(
                "I don't have this user's information in my database so, you'll not be able to interact with them"
                "Try replying to that person's msg or forward their message so i can act upon them"
            )
            return None, None

        else:
            user_id = user_id
            res = message.text.split(None, 2)
            if len(res) >= 3:
                text = res[2]

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])
        res = message.text.split(None, 2)
        if len(res) >= 3:
            text = res[2]

    elif prev_message:
        user_id, text = id_from_reply(message)

    else:
        return None, None

    try:
        message.bot.get_chat(user_id)
    except BadRequest as excp:
        if (
            excp.message in ("User_id_invalid", "Chat not found")
            and not str(user_id).isdigit()
        ):
            message.reply_text(
                "I don't seem to have interacted with this user before - please forward a message from "
                "them to give me control! (like a voodoo doll, I need a piece of them to be able "
                "to execute certain commands...)"
            )
            return None, None
        elif excp.message != "Chat not found":
            LOGGER.exception("Exception %s on user %s", excp.message, user_id)
            return None, None
        elif not str(user_id).isdigit():
            return None, None

    return user_id, text


def extract_user_fban(message: Message, args: List[str]) -> Optional[int]:
    return extract_unt_fedban(message, args)[0]


async def get_user(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message:
            if not previous_message.forward:
                replied_user = await event.client(
                    GetFullUserRequest(previous_message.from_id)
                )
            else:
                try:
                    user_id = previous_message.forward.sender.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                except Exception:
                    replied_user = await event.reply(
                        "This user's got his profile private. Ain't no peeping allowed."
                    )
    else:
        user = event.pattern_match.group(1)
        user = user.split(" ")
        user = user[0]

        if not user:
            user_id = event.from_id
            replied_user = await event.client(GetFullUserRequest(user_id))

        else:
            if user.isnumeric():
                user = int(user)
            if event.message.entities is not None:
                probable_user_mention_entity = event.message.entities[0]

                if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                    user_id = probable_user_mention_entity.user_id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user
            try:
                user_object = await event.client.get_entity(user)
                replied_user = await event.client(GetFullUserRequest(user_object.id))
            except (TypeError, ValueError) as err:
                await event.reply(str(err))
                return None

    return replied_user
