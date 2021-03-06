import re
from telegram import Update, Bot, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, Chat, Message, ChatAction

from actions import send_action
from commands import reply_main_keyboard
from cronometer import START_CTIMER
from database import get_hours_db, save_hours_db

# Callback Constants
CALLBACK_HOURS_ADD = 'hours_add'
CALLBACK_HOURS_MINUTES_ADD = 'hours_minutes_add'

CALLBACK_HOURS_ADD_TWO_HOURS = 'hours_add_two_hours'
CALLBACK_HOURS_ADD_ONE_HOUR = 'hours_add_one_hour'
CALLBACK_HOURS_REMOVE_TWO_HOURS = 'hours_add_two_hour'
CALLBACK_HOURS_REMOVE_ONE_HOUR = 'hours_remove_one_hour'

CALLBACK_HOURS_ADD_THIRTY_MINUTES = 'hours_add_thirty_minutes'
CALLBACK_HOURS_ADD_FIFTEEN_MINUTES = 'hours_add_fifteen_minutes'
CALLBACK_HOURS_ADD_TEN_MINUTES = 'hours_add_ten_minutes'
CALLBACK_HOURS_ADD_FIVE_MINUTES = 'hours_add_five_minutes'
CALLBACK_HOURS_ADD_ONE_MINUTE = 'hours_remove_one_minute'
CALLBACK_HOURS_REMOVE_THIRTY_MINUTES = 'hours_remove_thirty_minutes'
CALLBACK_HOURS_REMOVE_FIFTEEN_MINUTES = 'hours_remove_fifteen_minutes'
CALLBACK_HOURS_REMOVE_TEN_MINUTES = 'hours_remove_ten_minutes'
CALLBACK_HOURS_REMOVE_FIVE_MINUTES = 'hours_remove_five_minutes'
CALLBACK_HOURS_REMOVE_ONE_MINUTE = 'hours_remove_one_minute'

# Time in Seconds Constants
TWO_HOURS_IN_SECS = 7200
ONE_HOUR_IN_SECS = 3600
THIRTY_MIN_IN_SECS = 1800
TEN_MIN_IN_SECS = 600
FIVE_MIN_IN_SECS = 300
TWO_MIN_IN_SECS = 120
ONE_MIN_IN_SECS = 60

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_HOURS_ADD)]]
)

edit_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Editar", callback_data=CALLBACK_HOURS_ADD)]]
)

add_remove_hours_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("+2 horas", callback_data=CALLBACK_HOURS_ADD_TWO_HOURS),
      InlineKeyboardButton("-2 horas", callback_data=CALLBACK_HOURS_REMOVE_TWO_HOURS)],

     [InlineKeyboardButton("+1 hora", callback_data=CALLBACK_HOURS_ADD_ONE_HOUR),
      InlineKeyboardButton("-1 hora", callback_data=CALLBACK_HOURS_REMOVE_ONE_HOUR)],

     [InlineKeyboardButton("Minutos", callback_data=CALLBACK_HOURS_MINUTES_ADD)]]
)

add_remove_minutes_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("+30 min", callback_data=CALLBACK_HOURS_ADD_THIRTY_MINUTES),
      InlineKeyboardButton("+10 min", callback_data=CALLBACK_HOURS_ADD_TEN_MINUTES),
      InlineKeyboardButton("+5 min", callback_data=CALLBACK_HOURS_ADD_FIVE_MINUTES)],

     [InlineKeyboardButton("-30 min", callback_data=CALLBACK_HOURS_REMOVE_THIRTY_MINUTES),
      InlineKeyboardButton("-10 min", callback_data=CALLBACK_HOURS_REMOVE_TEN_MINUTES),
      InlineKeyboardButton("-5 min", callback_data=CALLBACK_HOURS_REMOVE_FIVE_MINUTES)],

     [InlineKeyboardButton("Horas", callback_data=CALLBACK_HOURS_ADD)]]
)


@send_action(ChatAction.TYPING)
def hours_inline(bot: Bot, update: Update):
    hours_count = get_hours_db(update)

    if hours_count > 0:
        update.message.reply_text(text='🕓 *Horas*\n\n'
                                       "Total de Horas: " + seconds_to_hours(hours_count),
                                  reply_markup=edit_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text='🕓 *Horas*\n\n' 
                                       "Você não tem horas até agora.",
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def hours_callback(bot: Bot, update: Update, user_data: dict = None):
    query: CallbackQuery = update.callback_query
    hours_count = get_hours_db(update)

    if query.data == CALLBACK_HOURS_ADD:

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_hours_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_MINUTES_ADD:

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    # Handle Hours accordingly
    elif query.data == CALLBACK_HOURS_ADD_ONE_HOUR:
        hours_count += ONE_HOUR_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_hours_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_REMOVE_ONE_HOUR:
        hours_count -= ONE_HOUR_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_hours_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_ADD_TWO_HOURS:
        hours_count += TWO_HOURS_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_hours_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_REMOVE_TWO_HOURS:
        hours_count -= TWO_HOURS_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_hours_keyboard,
                              parse_mode='Markdown')

    # Handle Minutes accordingly
    elif query.data == CALLBACK_HOURS_ADD_THIRTY_MINUTES:
        hours_count += THIRTY_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_REMOVE_THIRTY_MINUTES:
        hours_count -= THIRTY_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_ADD_TEN_MINUTES:
        hours_count += TEN_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_REMOVE_TEN_MINUTES:
        hours_count -= TEN_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_ADD_FIVE_MINUTES:
        hours_count += FIVE_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_HOURS_REMOVE_FIVE_MINUTES:
        hours_count -= FIVE_MIN_IN_SECS

        bot.edit_message_text(text='🕓 *Horas*\n\n'
                                   'Total de Horas: ' + seconds_to_hours(hours_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_minutes_keyboard,
                              parse_mode='Markdown')

    # Prevent negatives values
    if hours_count < 0:
        hours_count = 0

    save_hours_db(update, hours_count)

    if user_data is not None:
        if user_data.get(START_CTIMER) is not None:
            return query.answer(text='⚠  Seu cronômetro está ativo ', show_alert=False)

    # Cronometer ins't active, just go ahead.
    query.answer()


@send_action(ChatAction.TYPING)
def callback_offline_add_hours(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    hours_count = get_hours_db(update)
    increment = re.findall('\d+', msg.text)

    if len(increment) > 1:
        # Input has hours and minutes
        hours_count += int(increment[0]) * 3600 + int(increment[1]) * 60
    else:
        # Input only has hours
        if increment[0].isdigit():
            hours_count += int(increment[0]) * 3600
        else:
            # Error caught
            bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                                  'Não foi possível adicionar suas horas. '
                                  'Tente novamente ou escreva /ajuda',
                             chat_id=chat.id,
                             reply_to_message_id=msg.message_id,
                             reply_markup=reply_main_keyboard)

            raise TypeError('Invalid data type in regex', increment[0])

    save_hours_db(update, hours_count)
    bot.send_message(text='✅ Suas horas foram adicionadas!',
                     chat_id=chat.id,
                     reply_to_message_id=msg.message_id,
                     reply_markup=reply_main_keyboard)


@send_action(ChatAction.TYPING)
def callback_offline_remove_hours(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    hours_count = get_hours_db(update)
    decrement = re.findall('\d+', msg.text)

    if len(decrement) > 1:
        # Input has hours and minutes
        hours_count -= int(decrement[0]) * 3600 + int(decrement[1]) * 60
    else:
        # Input only has hours
        if decrement[0].isdigit():
            hours_count -= int(decrement[0]) * 3600
        else:
            # Error caught
            bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                                  'Não foi possível adicionar suas horas. '
                                  'Tente novamente ou escreva /ajuda',
                             chat_id=chat.id,
                             reply_to_message_id=msg.message_id,
                             reply_markup=reply_main_keyboard)

            raise TypeError('Invalid data type in regex', decrement[0])

    # Prevent negatives values
    if hours_count < 0:
        hours_count = 0

    save_hours_db(update, hours_count)
    bot.send_message(text='✅ Suas horas foram atualizadas!',
                     chat_id=chat.id,
                     reply_to_message_id=msg.message_id,
                     reply_markup=reply_main_keyboard)


@send_action(ChatAction.TYPING)
def callback_offline_add_minutes(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    hours_count = get_hours_db(update)
    increment = re.findall('\d+', msg.text)

    if increment[0].isdigit():
        hours_count += int(increment[0]) * 60
        save_hours_db(update, hours_count)

        bot.send_message(text='✅ Seus minutos foram adicionados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível adicionar seus minutos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', increment[0])


@send_action(ChatAction.TYPING)
def callback_offline_remove_minutes(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    hours_count = get_hours_db(update)
    decrement = re.findall('\d+', msg.text)

    if decrement[0].isdigit():
        hours_count -= int(decrement[0]) * 60
        # Prevent negatives values
        if hours_count < 0:
            hours_count = 0

        save_hours_db(update, hours_count)

        bot.send_message(text='✅ Seus minutos foram atualizados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível editar seus minutos. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', decrement[0])


def seconds_to_hours(seconds):
    # Prevent negative values
    if seconds < 0:
        seconds = 0

    total_hours: int = round(seconds) // ONE_HOUR_IN_SECS
    total_minutes: int = (round(seconds) % ONE_HOUR_IN_SECS) // ONE_MIN_IN_SECS

    if seconds == 0:
        return str('0:00')
    elif seconds < 2:
        return str('😂😂😂 \n'
                   'Só {} segundo? Você está me testando?'.format(round(seconds)))
    elif seconds < 10:
        return str('😂😂😂 \n'
                   'Só {} segundos? Você está me testando?'.format(round(seconds)))
    elif seconds < ONE_MIN_IN_SECS:
        return str('Apenas {} segundos...'.format(round(seconds)))
    elif seconds < TWO_MIN_IN_SECS:
        return str('{} minuto'.format(total_minutes))
    elif seconds < ONE_HOUR_IN_SECS:
        return str('{} minutos'.format(total_minutes))
    else:
        # If it has less than 10 minutes, improve readability concatenating a 0
        if total_minutes < 10:
            return str('{}:0{}'.format(total_hours, total_minutes))
        else:
            return str('{}:{}'.format(total_hours, total_minutes))
