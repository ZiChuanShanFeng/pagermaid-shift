import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 你的 bot 的 token
TOKEN = 'YOUR_BOT_TOKEN'

# 需要监控的关键词列表
KEYWORDS = ['keyword1', 'keyword2']

# 目标群组的 chat id
TARGET_CHAT_ID = 'YOUR_TARGET_CHAT_ID'

# 监控的群组 chat id 列表
SOURCE_CHAT_IDS = ['SOURCE_CHAT_ID_1', 'SOURCE_CHAT_ID_2']

# 配置日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def message_handler(update: Update, context: CallbackContext):
    try:
        message_text = update.message.text
        chat_id = str(update.message.chat.id)
        
        if chat_id in SOURCE_CHAT_IDS and any(keyword in message_text for keyword in KEYWORDS):
            context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message_text)
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text & (~Filters.command), message_handler)
    dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
