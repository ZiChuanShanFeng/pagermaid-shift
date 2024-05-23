# Telegram Keyword Monitoring Bot

[中文](#中文说明) | [English](#english-description)

## English Description

This Telegram bot monitors specified groups for messages containing certain keywords and forwards them to a target group.

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/ZiChuanShanFeng/Telegram-Keyword-Monitoring-Bot.git
    cd Telegram-Keyword-Monitoring-Bot
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

### Configuration

- `TOKEN`: Your bot's token.
- `TARGET_CHAT_ID`: The chat ID of the target group.
- `SOURCE_CHAT_IDS`: A list of chat IDs of the groups to monitor.
- `KEYWORDS`: A list of keywords to monitor.

### License

This project is licensed under the MIT License.

---

## 中文说明

这个 Telegram 机器人可以监控指定群组中的消息，如果消息中包含特定关键词，就将其转发到目标群组。

### 设置

1. 克隆仓库：
    ```bash
    git clone https://github.com/ZiChuanShanFeng/Telegram-Keyword-Monitoring-Bot.git
    cd Telegram-Keyword-Monitoring-Bot
    ```

2. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

3. 在 `bot.py` 中设置你的 bot token、目标群组的 chat ID、监控的群组 chat ID 列表和关键词。

4. 运行机器人：
    ```bash
    python bot.py
    ```

### 配置

- `TOKEN`：你的 bot 的 token。
- `TARGET_CHAT_ID`：目标群组的 chat ID。
- `SOURCE_CHAT_IDS`：监控的群组 chat ID 列表。
- `KEYWORDS`：监控的关键词列表。

### 许可证

此项目采用 MIT 许可证。

---

## Project Structure

```plaintext
telegram-bot-project/
├── .gitignore
├── README.md
├── requirements.txt
└── bot.py
