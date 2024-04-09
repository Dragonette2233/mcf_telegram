from telegram import Update
from telegram import ReplyKeyboardMarkup, KeyboardButton
from functools import wraps
from telegram.ext import Application, CommandHandler, CallbackContext, StringRegexHandler, MessageHandler, filters
from io import BytesIO
# from bot_reload import (
#     close_mcf_and_chrome,
#     start_mcf,
#     status_mcf
# )
import json
import os
import logging
import redis
from static_data import (
    PATH,
    OWNER,
    AUTH_COMMAND
)
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


with open(PATH.AUTH_USERS, 'r') as us:
    authorized_users = [i[:-1] for i in us.readlines()]

snip = {
    "time": 0,

    "blue_kills": 0,
    "red_kills": 0,

    "blue_towers": 0,
    "red_towers": 0,

    "blue_t1_hp": 0,
    "red_t1_hp": 0,

    "blue_gold": 0,
    "red_gold": 0,

    "is_active": 0
}

# Установка значения
for key, value in snip.items():
    r.set(key, value)

def auth(authorized_users):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext):
            user_id = update.message.from_user.id
            if str(user_id) in authorized_users:
                return await func(update, context)
            else:
                await update.message.reply_text("🚫 Unauthorized")
        return wrapper
    return decorator

async def first_auth(update: Update, context: CallbackContext):
    us_id = str(update.message.from_user.id)
    
    keyboard = [[KeyboardButton('/game')] ]
    # print(update.message.from_user.id)
    if update.message.from_user.id == OWNER:
        keyboard.append([KeyboardButton('/mcf_status')])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if us_id in authorized_users:
        await update.message.reply_text('✅ Вы уже авторизовались', reply_markup=reply_markup)
    else:
        authorized_users.append(us_id)

        with open(PATH.AUTH_USERS, 'w+') as us:
            for i in authorized_users:
                us.writelines(i + '\n')

        await update.message.reply_text('✅ Авторизация успешна', reply_markup=reply_markup)

# @auth(authorized_users=authorized_users)
async def info(update: Update, context: CallbackContext):

    if update.message.text == '/info':
        answer = open(PATH.MAIN_INFO, encoding='utf-8').read()
    elif update.message.text == '/info_bets':
        answer = open(PATH.BETS_INFO, encoding='utf-8').read()
    await update.message.reply_text(answer)

# @auth(authorized_users=authorized_users)
async def start(update: Update, context: CallbackContext):

    visitor = update.message.chat.first_name
    with open(PATH.GREET_MESSAGE, 'r', encoding='utf-8') as greet:
        await update.message.reply_text(greet.read().format(visitor=visitor, trial_link=PATH.INVITE_LINK, chat_link=PATH.CHAT_LINK))

@auth(authorized_users=authorized_users)
async def emul(update: Update, context: CallbackContext):
    
    r.set('emulation', '0')

    await update.message.reply_text('Emulation stoped')

# @auth(authorized_users=authorized_users)
async def actual_mirror(update: Update, context: CallbackContext):
    with open(PATH.MIRROR_PAGE, 'r') as ex_url:
        await update.message.reply_text(f'Актуальное зеркало: {ex_url.read()}')

@auth(authorized_users=authorized_users)
async def change_actual_mirror(update: Update, context: CallbackContext):

    league_alt_rout = '/ru/live/cyber-zone/league-of-legends'
    message = update.message.text

    if not message.startswith('https://1xlite-') and not message.startswith('https://melb'):
        await update.message.reply_text(f'Неверная ссылка для зеркала')
    else:
        link_parts = message.split('/')
        new_link = '/'.join(link_parts[0:3]) + league_alt_rout
        with open(PATH.MIRROR_PAGE, 'w+') as ex_url:
            ex_url.write(new_link)

        await update.message.reply_text(f'Зеркало добавлено: {new_link}')

@auth(authorized_users=authorized_users)
async def echo_score(update: Update, context: CallbackContext) -> None:
    

    if r.get('is_active') != '0':
        
        with open(PATH.SCORE_ANSWER, 'r', encoding='utf-8') as sample:
            message_sample = sample.read()

        timestamp = divmod(int(r.get('time')), 60)
        minutes = timestamp[0] if timestamp[0] > 9 else f"0{timestamp[0]}"
        seconds = timestamp[1] if timestamp[1] > 9 else f"0{timestamp[1]}"
        message_for_reply = message_sample.format(
            blue_kills = r.get('blue_kills'),
            blue_towers = r.get('blue_towers'),
            red_kills = r.get('red_kills'),
            red_towers = r.get('red_towers'),
            blue_gold = r.get('blue_gold'),
            red_gold = r.get('red_gold'),
            blue_t1_hp = r.get('blue_t1_hp'),
            red_t1_hp = r.get('red_t1_hp'),
            time = ':'.join([str(minutes), str(seconds)]),
        )
        await update.message.reply_text(message_for_reply)
    else:
        await update.message.reply_text('Нет активной игры')


@auth(authorized_users=authorized_users)
async def mcf_status(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == OWNER:
        from PIL import ImageGrab
        
        screen = ImageGrab.grab()
        img_byte_array = BytesIO()
        screen.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Отправка изображения как фото
        await update.message.reply_photo(photo=img_byte_array)

async def trial(update: Update, context: CallbackContext) -> None:

    await update.message.reply_text('Пробный период действует сутки: {link}'.format(link=PATH.INVITE_LINK))


# @auth(authorized_users=authorized_users)
async def predicts_check(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""

    with open(PATH.PREDICTS_ANSWER, 'r', encoding='utf-8') as file:
        predicts_answer_message = file.read()

    if update.message.text == '/predicts_global':
        top_message = 'Результат по предиктам за все время'
        predicts_path = PATH.PREDICTS_TRACE_GLOBAL
    else:
        top_message = 'Результат по предиктам за сутки'
        predicts_path = PATH.PREDICTS_TRACE_DAILY

    with open(predicts_path, 'r', encoding='utf-8') as js_stats:
        predicts: dict = json.load(js_stats)
        itms = list(predicts.items())

        ordered_plus = [value[1][0] for value in itms]
        ordered_minus = [value[1][1] for value in itms]

        message = predicts_answer_message.format(*ordered_plus, *ordered_minus, top_message=top_message)

    await update.message.reply_text(message)
       
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(AUTH_COMMAND, first_auth))
    application.add_handler(CommandHandler("game", echo_score))
    # application.add_handler(CommandHandler("build", echo_build))
    application.add_handler(CommandHandler("predicts_global", predicts_check))
    application.add_handler(CommandHandler("predicts_daily", predicts_check))
    # application.add_handler(CommandHandler("trial", trial))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'https\S+'), change_actual_mirror))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'https\S+'), change_actual_mirror))

    application.add_handler(CommandHandler('info', info))
    #application.add_handler(CommandHandler('info_predicts', info))
    #application.add_handler(CommandHandler('info_extend', info))
    application.add_handler(CommandHandler('info_bets', info))
    application.add_handler(CommandHandler('mirror', actual_mirror))

    application.add_handler(CommandHandler('emul_stop', emul))
    application.add_handler(CommandHandler('mcf_status', mcf_status))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()