#
# Copyright (C) 2024 by THE-VIP-BOY-OP@Github, < https://github.com/THE-VIP-BOY-OP >.
#
# This file is part of < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/THE-VIP-BOY-OP/VIP-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#
from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from VIPMUSIC import Platform, app
from VIPMUSIC.core.call import VIP
from VIPMUSIC.misc import db
from VIPMUSIC.utils import AdminRightsCheck, seconds_to_min

# Command
SEEK_COMMAND = get_command("SEEK_COMMAND")

@app.on_message(filters.command(SEEK_COMMAND) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_28"])
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text(_["admin_29"])
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_30"])
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return await message.reply_text(_["admin_30"])
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                _["admin_31"].format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_32"])
    if "vid_" in file_path:
        n, file_path = await Platform.youtube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text(_["admin_30"])
    try:
        await BAD.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except Exception:
        return await mystic.edit_text(_["admin_34"])
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(_["admin_33"].format(seconds_to_min(to_seek)))
    
