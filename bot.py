import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# 你的 bot 的 token
TOKEN = 'your bot token'

# 需要监控的关键词列表
KEYWORDS = ['key1', 'key2']

# 目标群组的 chat id
TARGET_CHAT_ID = 'chat_id'

# 监控的群组 chat id 列表
SOURCE_CHAT_IDS = ['chat_id1', 'chat_id2']

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

async def message_handler(update: Update, context: CallbackContext):
    try:
        message_text = update.message.text
        chat_id = str(update.message.chat.id)
        
        if chat_id in SOURCE_CHAT_IDS and any(keyword in message_text for keyword in KEYWORDS):
            await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text)
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler)
    app.add_handler(text_handler)

    await app.initialize()
    await app.updater.start_polling()  # 启动 Telegram bot

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
