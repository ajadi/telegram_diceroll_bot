# Telegram DnD Bot

This Telegram bot allows rolling dice for Dungeons & Dragons games, supporting commands in the format /roll XdY(+Z). For example, /roll 2d20+5 or /roll 2d6+1d8+3.

## Installation and Launch

1. Clone the repository:

    ```sh
    git clone https://github.com/ajadi/telegram_diceroll_bot.git
    cd telegram_diceroll_bot
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```
4. Replace YOUR_TELEGRAM_BOT_TOKEN with your bot's token in the telegram_diceroll_bot.py file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.