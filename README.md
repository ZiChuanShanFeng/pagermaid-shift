# Telegram Keyword Monitoring Bot

This Telegram bot monitors specified groups for messages containing certain keywords and forwards them to a target group.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-bot-project.git
    cd telegram-bot-project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your bot token, target chat ID, source chat IDs, and keywords in `bot.py`.

4. Run the bot:
    ```bash
    python bot.py
    ```

## Configuration

- `TOKEN`: Your bot's token.
- `TARGET_CHAT_ID`: The chat ID of the target group.
- `SOURCE_CHAT_IDS`: A list of chat IDs of the groups to monitor.
- `KEYWORDS`: A list of keywords to monitor.

## License

This project is licensed under the MIT License.
