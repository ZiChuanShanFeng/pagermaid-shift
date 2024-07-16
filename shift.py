import contextlib
from asyncio import sleep
from random import uniform
from typing import Any, List, Union, Set
from pyrogram.enums.chat_type import ChatType
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import Chat
from pagermaid import log, logs
from pagermaid.enums import Client, Message
from pagermaid.listener import listener
from pagermaid.single_utils import sqlite
from pagermaid.utils import lang
import re  # 导入正则表达式模块

WHITELIST = []
AVAILABLE_OPTIONS = {"silent", "text", "all", "photo", "document", "video"}

def try_cast_or_fallback(val: Any, t: type) -> Any:
    try:
        return t(val)
    except:
        return val

def check_chat_available(chat: Chat):
    assert (
        chat.type in [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP, ChatType.BOT, ChatType.PRIVATE]
        and not chat.has_protected_content
    )

@listener(
    command="shift",
    description="开启转发频道新消息功能",
    parameters="set [from channel] [to channel] (silent) (keywords:[keyword1,keyword2,...]) (blacklist:[word1,word2,...]) 自动转发包含关键词的频道新消息（可以使用频道用户名或者 id）\n"
               "del [from channel] 删除转发\n"
               "backup [from channel] [to channel] (silent) 备份频道（可以使用频道用户名或者 id）\n"
               "list 显示目前转发的频道\n"
               "blacklist [from channel] add [word] 添加黑名单词\n"
               "blacklist [from channel] remove [word] 删除黑名单词\n"
               "blacklist [from channel] list 查看黑名单词列表\n"
               "keywords [from channel] add [word] 添加关键词\n"
               "keywords [from channel] remove [word] 删除关键词\n"
               "keywords [from channel] list 查看关键词列表\n\n"
               "选项说明：\n"
               "silent: 禁用通知, text: 文字, all: 全部信息都传, photo: 图片, document: 文件, video: 视频\n\n由 @Zichuan1an 修改",
)
async def shift_set(client: Client, message: Message):
    if not message.parameter:
        await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        return
    if message.parameter[0] == "set":
        if len(message.parameter) < 3:
            return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        
        options = set()
        keywords = []
        blacklist = []

        for param in message.parameter[3:]:
            if param.startswith("keywords:"):
                keywords = param[len("keywords:"):].strip("[]").split(",")
            elif param.startswith("blacklist:"):
                blacklist = param[len("blacklist:"):].strip("[]").split(",")
            else:
                options.add(param)

        if options.difference(AVAILABLE_OPTIONS):
            return await message.edit("出错了呜呜呜 ~ 无法识别的选项。")

        # 检查来源频道
        try:
            source = await client.get_chat(
                try_cast_or_fallback(message.parameter[1], int)
            )
            assert isinstance(source, Chat)
            check_chat_available(source)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的来源对话。")
        if source.id in WHITELIST:
            return await message.edit("出错了呜呜呜 ~ 此对话位于白名单中。")

        # 检查目标频道
        try:
            target = await client.get_chat(
                try_cast_or_fallback(message.parameter[2], int)
            )
            assert isinstance(target, Chat)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的目标对话。")
        if target.id in WHITELIST:
            await message.edit("出错了呜呜呜 ~ 此对话位于白名单中。")
            return

        sqlite[f"shift.{source.id}"] = target.id
        sqlite[f"shift.{source.id}.options"] = list(options) if options else ["all"]
        sqlite[f"shift.{source.id}.keywords"] = keywords
        sqlite[f"shift.{source.id}.blacklist"] = blacklist

        await message.edit(f"已成功配置将对话 {source.id} 的新消息转发到 {target.id} 。")
        await log(f"已成功配置将对话 {source.id} 的新消息转发到 {target.id} 。")

    elif message.parameter[0] == "del":
        if len(message.parameter) != 2:
            return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        # 检查来源频道
        try:
            source = await client.get_chat(
                try_cast_or_fallback(message.parameter[1], int)
            )
            assert isinstance(source, Chat)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的来源对话。")
        try:
            del sqlite[f"shift.{source.id}"]
            with contextlib.suppress(Exception):
                del sqlite[f"shift.{source.id}.options"]
                del sqlite[f"shift.{source.id}.keywords"]
                del sqlite[f"shift.{source.id}.blacklist"]
        except Exception:
            return await message.edit("emm...当前对话不存在于自动转发列表中。")
        await message.edit(f"已成功关闭对话 {str(source.id)} 的自动转发功能。")
        await log(f"已成功关闭对话 {str(source.id)} 的自动转发功能。")

    elif message.parameter[0] == "backup":
        if len(message.parameter) < 3:
            return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        
        options = set(message.parameter[3:] if len(message.parameter) > 3 else ())
        if options.difference(AVAILABLE_OPTIONS):
            return await message.edit("出错了呜呜呜 ~ 无法识别的选项。")
        
        # 检查来源频道
        try:
            source = await client.get_chat(
                try_cast_or_fallback(message.parameter[1], int)
            )
            assert isinstance(source, Chat)
            check_chat_available(source)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的来源对话。")
        if source.id in WHITELIST:
            return await message.edit("出错了呜呜呜 ~ 此对话位于白名单中。")

        # 检查目标频道
        try:
            target = await client.get_chat(
                try_cast_or_fallback(message.parameter[2], int)
            )
            assert isinstance(target, Chat)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的目标对话。")
        if target.id in WHITELIST:
            return await message.edit("出错了呜呜呜 ~ 此对话位于白名单中。")

        # 开始遍历消息
        await message.edit(f"开始备份频道 {source.id} 到 {target.id} 。")

        async for msg in client.search_messages(source.id):  # type: ignore
            await sleep(uniform(0.5, 1.0))
            await loosely_forward(
                message,
                msg,
                target.id,
                options,
                disable_notification="silent" in options,
            )
        await message.edit(f"备份频道 {source.id} 到 {target.id} 已完成。")

    elif message.parameter[0] == "list":
        from_ids = list(
            filter(
                lambda x: (x.startswith("shift.") and (not x.endswith("options")) and (not x.endswith("keywords")) and (not x.endswith("blacklist"))),
                list(sqlite.keys()),
            )
        )
        if not from_ids:
            return await message.edit("没有要转存的频道")
        output = "总共有 %d 个频道要转存\n\n" % len(from_ids)
        for from_id in from_ids:
            to_id = sqlite[from_id]
            output += "%s -> %s\n" % (from_id[6:], to_id)
        await message.edit(output)

    elif message.parameter[0] == "blacklist":
        if len(message.parameter) < 3:
            return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        try:
            source = await client.get_chat(
                try_cast_or_fallback(message.parameter[1], int)
            )
            assert isinstance(source, Chat)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的来源对话。")
        
        if message.parameter[2] == "add" and len(message.parameter) == 4:
            blacklist = sqlite.get(f"shift.{source.id}.blacklist", [])
            word = message.parameter[3]
            if word not in blacklist:
                blacklist.append(word)
                sqlite[f"shift.{source.id}.blacklist"] = blacklist
                await message.edit(f"已成功将词 '{word}' 添加到对话 {source.id} 的黑名单中。")
            else:
                await message.edit(f"词 '{word}' 已在对话 {source.id} 的黑名单中。")
        
        elif message.parameter[2] == "remove" and len(message.parameter) == 4:
            blacklist = sqlite.get(f"shift.{source.id}.blacklist", [])
            word = message.parameter[3]
            if word in blacklist:
                blacklist.remove(word)
                sqlite[f"shift.{source.id}.blacklist"] = blacklist
                await message.edit(f"已成功将词 '{word}' 从对话 {source.id} 的黑名单中移除。")
            else:
                await message.edit(f"词 '{word}' 不在对话 {source.id} 的黑名单中。")
        
        elif message.parameter[2] == "list" and len(message.parameter) == 3:
            blacklist = sqlite.get(f"shift.{source.id}.blacklist", [])
            if blacklist:
                output = f"对话 {source.id} 的黑名单词列表：\n" + "\n".join(blacklist)
                await message.edit(output)
            else:
                await message.edit(f"对话 {source.id} 的黑名单中没有词。")
        else:
            await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
    elif message.parameter[0] == "keywords":
        if len(message.parameter) < 3:
            return await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        try:
            source = await client.get_chat(
                try_cast_or_fallback(message.parameter[1], int)
            )
            assert isinstance(source, Chat)
        except Exception:
            return await message.edit("出错了呜呜呜 ~ 无法识别的来源对话。")
        
        if message.parameter[2] == "add" and len(message.parameter) == 4:
            keywords = sqlite.get(f"shift.{source.id}.keywords", [])
            word = message.parameter[3]
            if word not in keywords:
                keywords.append(word)
                sqlite[f"shift.{source.id}.keywords"] = keywords
                await message.edit(f"已成功将关键词 '{word}' 添加到对话 {source.id} 中。")
            else:
                await message.edit(f"关键词 '{word}' 已在对话 {source.id} 中。")
        
        elif message.parameter[2] == "remove" and len(message.parameter) == 4:
            keywords = sqlite.get(f"shift.{source.id}.keywords", [])
            word = message.parameter[3]
            if word in keywords:
                keywords.remove(word)
                sqlite[f"shift.{source.id}.keywords"] = keywords
                await message.edit(f"已成功将关键词 '{word}' 从对话 {source.id} 中移除。")
            else:
                await message.edit(f"关键词 '{word}' 不在对话 {source.id} 中。")
        
        elif message.parameter[2] == "list" and len(message.parameter) == 3:
            keywords = sqlite.get(f"shift.{source.id}.keywords", [])
            if keywords:
                output = f"对话 {source.id} 的关键词列表：\n" + "\n".join(keywords)
                await message.edit(output)
            else:
                await message.edit(f"对话 {source.id} 中没有关键词。")
        else:
            await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
    else:
        await message.edit(f"{lang('error_prefix')}{lang('arg_error')}")
        return

@listener(is_plugin=True, incoming=True, ignore_edited=True, ignore_forwarded=False)
async def shift_channel_message(message: Message):
    """Event handler to auto forward channel messages."""
    d = dict(sqlite)
    source = message.chat.id

    # 找消息类型video、document...
    media_type = message.media.value if message.media else "text"
    target = d.get(f"shift.{source}")
    if not target:
        return
    if message.chat.has_protected_content:
        del sqlite[f"shift.{source}"]
        return
    options = d.get(f"shift.{source}.options") or []
    keywords = d.get(f"shift.{source}.keywords") or []
    blacklist = d.get(f"shift.{source}.blacklist") or []

    # 检查黑名单词
    if any(re.search(word, message.text or "", re.IGNORECASE) for word in blacklist):
        return

    # 检查关键词
    if keywords:
        if any(re.search(keyword, message.text or "", re.IGNORECASE) for keyword in keywords):
            await message.forward(
                target,
                disable_notification="silent" in options,
            )
    elif (not options) or "all" in options:
        await message.forward(
            target,
            disable_notification="silent" in options,
        )
    elif media_type in options:
        await message.forward(
            target,
            disable_notification="silent" in options,
        )
    else:
        logs.debug("skip message type: %s", media_type)

async def loosely_forward(
        notifier: Message,
        message: Message,
        chat_id: int,
        options: Union[List[str], Set[str]],
        disable_notification: bool = False,
):
    # 找消息类型video、document...
    media_type = message.media.value if message.media else "text"
    try:
        if (not options) or "all" in options:
            await message.forward(
                chat_id,
                disable_notification=disable_notification,
            )
        elif media_type in options:
            await message.forward(
                chat_id,
                disable_notification=disable_notification,
            )
        else:
            logs.debug("skip message type: %s", media_type)
    except FloodWait as ex:
        min: int = ex.value  # type: ignore
        delay = min + uniform(0.5, 1.0)
        await notifier.edit(f"触发 Flood ，暂停 {delay} 秒。")
        await sleep(delay)
        await loosely_forward(notifier, message, chat_id, options, disable_notification)
    except Exception:
        pass  # drop other errors
