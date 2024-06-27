# PagerMaid Shift

由 @Zichuan1lan 修改 原版本在PagerMaid上 如果侵权 请联系删除

PagerMaid Shift 是一个 Telegram 机器人插件，用于自动转发消息。它支持多种选项，如静默转发、按类型过滤消息（文字、照片、文档、视频）以及按关键字过滤。

PagerMaid Shift is a Telegram bot plugin for automatically forwarding messages. It supports various options like silent forwarding, filtering messages by type (text, photo, document, video), and filtering by keywords.

[中文](#中文版本) | [English](#english-version)

## 中文版本

### 功能

- **自动转发消息**: 自动将一个频道的新消息转发到另一个频道。
- **关键字过滤**: 仅转发包含特定关键字的消息。
- **类型过滤**: 仅转发特定类型的消息，如文字、照片、文档、视频。
- **静默转发**: 禁用通知进行静默转发。

### 安装

1. 克隆这个仓库并进入项目目录：
    ```sh
    git clone https://github.com/ZiChuanShanFeng/pagermaid-shift.git
    cd pagermaid-shift
    ```

2. 配置 PagerMaid，添加并启用 `shift` 插件。

### 使用方法

- **设置转发**:
    ```
    /shift set [来源频道] [目标频道] (silent) (keywords:[keyword1,keyword2,...])
    ```

- **删除转发**:
    ```
    /shift del [来源频道]
    ```

- **备份频道**:
    ```
    /shift backup [来源频道] [目标频道] (silent)
    ```

- **列出所有转发**:
    ```
    /shift list
    ```

### 示例

设置从 `source_channel` 转发消息到 `target_channel`：
/shift set source_channel target_channel all

删除转发规则：
/shift del source_channel

## English Version

### Features

- **Automatic Message Forwarding**: Automatically forward new messages from one channel to another.
- **Keyword Filtering**: Forward only messages containing specific keywords.
- **Type Filtering**: Forward only specific types of messages such as text, photo, document, and video.
- **Silent Forwarding**: Forward messages without notifications.

### Installation

1. Clone the repository and enter the project directory:
    ```sh
    git clone https://github.com/ZiChuanShanFeng/pagermaid-shift.git
    cd pagermaid-shift
    ```


2. Configure PagerMaid, add and enable the `shift` plugin.

### Usage

- **Set up forwarding**:
    ```
    /shift set [from channel] [to channel] (silent) (keywords:[keyword1,keyword2,...])
    ```

- **Delete forwarding**:
    ```
    /shift del [from channel]
    ```

- **Backup channel**:
    ```
    /shift backup [from channel] [to channel] (silent)
    ```

- **List all forwardings**:
    ```
    /shift list
    ```

### Examples

Set up forwarding from `source_channel` to `target_channel`:
/shift set source_channel target_channel all


Delete forwarding rule:
/shift del source_channel

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
