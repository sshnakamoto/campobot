# Callback Constants
import re

from telegram import Bot, CallbackQuery, Chat, InlineKeyboardButton, InlineKeyboardMarkup, Update, User, Message

from commands import reply_main_keyboard
from database import get_returns_db, get_returns_list_db, save_returns_db

CALLBACK_RETURNS_ADD_ONE = 'returns_add_one'
CALLBACK_RETURNS_REMOVE_ONE = 'returns_remove_one'
CALLBACK_RETURNS_ADD_THREE = 'returns_add_three'

CALLBACK_RETURNS_LIST = 'returns_list'
CALLBACK_RETURNS_INSTERESTED = 'returns_interested'

# Keyboards Inline
add_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_RETURNS_ADD_ONE)]]
)

add_remove_keyboard = InlineKeyboardMarkup(
     [[InlineKeyboardButton("+3", callback_data=CALLBACK_RETURNS_ADD_THREE),
      InlineKeyboardButton("+1", callback_data=CALLBACK_RETURNS_ADD_ONE ),
      InlineKeyboardButton("-1", callback_data=CALLBACK_RETURNS_REMOVE_ONE)]
      #    ,
      #
      # [InlineKeyboardButton("🙋 Interessados", callback_data=CALLBACK_RETURNS_LIST)]
      ]
)

add_interested = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Adicionar", callback_data=CALLBACK_RETURNS_INSTERESTED)]]
)


def returns_inline(bot: Bot, update: Update):
    usr: User = update.effective_user
    return_count = get_returns_db(update)

    if return_count > 0:
        update.message.reply_text(text='🏠 *Revisitas*\n\n'
                                       "Total de Revisitas: " + str(return_count),
                                  reply_markup=add_remove_keyboard, parse_mode='Markdown')

    else:
        update.message.reply_text(text='🏠 *Revisitas*\n\n' 
                                       "Você não marcou nenhuma revisita até agora.",
                                  reply_markup=add_keyboard, parse_mode='Markdown')


def returns_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    query: CallbackQuery = update.callback_query
    returns_count = get_returns_db(update)

    if query.data == CALLBACK_RETURNS_ADD_ONE:
        returns_count += 1

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_RETURNS_REMOVE_ONE:
        # Prevent negative values
        if returns_count == 0:
            return query.answer()

        returns_count -= 1

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    elif query.data == CALLBACK_RETURNS_ADD_THREE:
        returns_count += 3

        bot.edit_message_text(text='🏠 *Revisitas*\n\n'
                                   'Total de Revisitas: ' + str(returns_count),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=add_remove_keyboard,
                              parse_mode='Markdown')

    # TODO: Handle Interested People
    elif query.data == CALLBACK_RETURNS_LIST:
        returns_list = get_returns_list_db(update)
        if len(returns_list) == 0:

            bot.edit_message_text(text='🙋 *Interessados*\n\n'
                                       'Você não adicionou nenhum interessado até agora.',
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=add_interested,
                                  parse_mode='Markdown')
        elif len(returns_list) <= 3:
            position = 0
            interested = ''
            for item in returns_list:
                position += 1
                interested += 'N: ' + str(position) + \
                              'Nome: ' + item.get('name') + '\n' + \
                              'Endereço: ' + item.get('address') + '\n\n'

            bot.edit_message_text(text='🙋 *Interessados*\n\n' +
                                       interested,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=add_interested,
                                  parse_mode='Markdown')

        else:

            bot.edit_message_text(text='🙋 *Interessados*\n\n'
                                       'Mais de 4 interessados. Falta a lista.',
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=add_interested,
                                  parse_mode='Markdown')

    save_returns_db(update, returns_count)
    query.answer()


def returns_offline_add_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    returns_count = get_returns_db(update)
    increment = re.findall('\d+', msg.text)

    if increment[0].isdigit():
        returns_count += int(increment[0])
        save_returns_db(update, returns_count)

        bot.send_message(text='✅ Suas revisitas foram adicionados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível atualizar as suas revisitas. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', increment[0])


def returns_offline_remove_callback(bot: Bot, update: Update):
    chat: Chat = update.effective_chat
    msg: Message = update.effective_message

    returns_count = get_returns_db(update)
    decrement = re.findall('\d+', msg.text)

    if decrement[0].isdigit():
        returns_count -= int(decrement[0])

        # Prevent negative values
        if returns_count < 0:
            returns_count = 0
        save_returns_db(update, returns_count)

        bot.send_message(text='✅ Suas revisitas foram atualizados!',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)
    else:
        # Error caught
        bot.send_message(text='😓 Desculpe, algo estranho aconteceu. \n'
                              'Não foi possível atualizar suas revisitas. '
                              'Tente novamente ou escreva /ajuda',
                         chat_id=chat.id,
                         reply_to_message_id=msg.message_id,
                         reply_markup=reply_main_keyboard)

        raise TypeError('Invalid data type in regex', decrement[0])


