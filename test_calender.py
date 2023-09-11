import telebot
from telebot import types
import datetime

# Replace with your own Bot Token
TOKEN = "6000416074:AAGD_1u1UaVIgn43Ld0BsGv1IpZcUc99qy8"

bot = telebot.TeleBot(TOKEN)

# dt = datetime.datetime.now()
# weekday_num = dt.weekday()
# weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
# weekday = weekdays[weekday_num]

def generate_calendar(year, month):

    first_day = datetime.date(year, month, 1)
    # print(first_day, first_day.weekday())
    last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    # print(last_day)
    current_day = first_day
    # print("-".join(str(current_day).split("-")[:2]))
    # print()

    markup = types.InlineKeyboardMarkup(row_width=7)
    header = [types.InlineKeyboardButton("<<", callback_data=current_day.strftime("prev_month_%Y_%m")),
              types.InlineKeyboardButton(f"{year}-{month:02d}", callback_data="no_op"),
              types.InlineKeyboardButton(">>", callback_data=current_day.strftime("next_month_%Y_%m"))]
    markup.row(*header)
    
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    day_buttons = [types.InlineKeyboardButton(day, callback_data="no_op") for day in days]
    markup.row(*day_buttons)
    
    row = []
    # print(current_day.weekday()+1)
    for i in range(current_day.weekday()):
        row.append(types.InlineKeyboardButton("-", callback_data="None"))
    
    # print(row)
    while current_day <= last_day:
        # print(current_day.weekday(), len(row))
        if current_day.weekday() == 6 and row:
            row.append(types.InlineKeyboardButton(str(current_day.day), callback_data=current_day.strftime("day_%Y_%m_%d")))
            markup.row(*row)
            row = []
        else:
            row.append(types.InlineKeyboardButton(str(current_day.day), callback_data=current_day.strftime("day_%Y_%m_%d")))
        current_day += datetime.timedelta(days=1)

    for i in range(6-last_day.weekday()):
        row.append(types.InlineKeyboardButton("-", callback_data="None"))

    if row:
        markup.row(*row)
    
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    now = datetime.datetime.now()
    bot.send_message(message.chat.id, f"Welcome to the calendar bot! Please select a date:", reply_markup=generate_calendar(now.year, now.month))

@bot.callback_query_handler(func=lambda call: call.data.startswith("day"))
def callback_query(call):
    selected_date = datetime.datetime.strptime("-".join(call.data.split('_')[1:]), "%Y-%m-%d").date()
    response = f"You selected the date: {selected_date}"
    bot.send_message(call.message.chat.id, response)

@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_month"))
def prev_month(call):
    current_date = datetime.datetime.strptime("-".join(call.data.split("_")[2:]), "%Y-%m").date()
    prev_month = current_date.replace(day=1) - datetime.timedelta(days=1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=prev_month.strftime("%Y-%m"), reply_markup=generate_calendar(prev_month.year, prev_month.month))

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_month"))
def next_month(call):
    current_date = datetime.datetime.strptime("-".join(call.data.split("_")[2:]), "%Y-%m").date()
    next_month = current_date.replace(day=1) + datetime.timedelta(days=31)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=next_month.strftime("%Y-%m"), reply_markup=generate_calendar(next_month.year, next_month.month))

if __name__ == "__main__":
    bot.polling()
