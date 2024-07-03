import re
import random
import logging
import json
from datetime import datetime
from hashlib import sha256
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Function to load messages from JSON file
def load_messages():
    try:
        with open('messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("messages.json file not found")
        return {}
    except json.JSONDecodeError:
        logger.error("JSON decoding error in messages.json")
        return {}

# Load messages
messages = load_messages()

# Function to handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.get('start', 'Error loading message'))

# Function to handle /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(messages.get('help', 'Error loading message'))

# Function to parse dice expressions
def parse_dice_expression(expression):
    dice_pattern = re.compile(r'(\d*)d(\d+)|([+-]\d+)')
    return dice_pattern.findall(expression)

# Function to evaluate dice expressions
def evaluate_expression(matches):
    total = 0
    results = []
    modifier = 0

    for match in matches:
        if match[0] or match[1]:  # If it's a dice expression, e.g., 2d6
            num_dice = int(match[0]) if match[0] else 1
            dice_size = int(match[1])
            dice_results = [random.randint(1, dice_size) for _ in range(num_dice)]
            results.extend(dice_results)
            total += sum(dice_results)
        elif match[2]:  # If it's a modifier, e.g., +3
            modifier += int(match[2])
            total += int(match[2])

    return total, results, modifier

# Function to handle /roll command
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Use user ID and message ID to initialize random seed
        user_id = update.message.from_user.id
        message_id = update.message.message_id
        seed_value = sha256(f"{datetime.now().timestamp()}_{user_id}_{message_id}".encode()).hexdigest()
        random.seed(int(seed_value, 16))

        message = context.args
        dice_expression = message[0] if message else "1d20"  # Default value

        matches = parse_dice_expression(dice_expression)

        if not matches:
            await update.message.reply_text(messages.get('invalid_format', 'Error loading message'))
            return

        total, results, modifier = evaluate_expression(matches)
        results_str = ", ".join(map(str, results))
        modifier_str = f" + {modifier}" if modifier else ""

        await update.message.reply_text(
            messages.get('roll_result', 'Error loading message').format(
                dice_expression=dice_expression, results_str=results_str, modifier_str=modifier_str, total=total),
            reply_to_message_id=update.message.message_id
        )

    except Exception as e:
        logger.error(f"{messages.get('log_error', 'Error processing /roll command')}: {e}")
        await update.message.reply_text(
            messages.get('error', 'Error loading message'),
            reply_to_message_id=update.message.message_id
        )

def main():
    # Insert your token here
    token = 'YOUR_TELEGRAM_BOT_TOKEN'

    # Create the application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("roll", roll))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
