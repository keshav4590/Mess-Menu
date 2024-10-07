import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize the bot with your bot token
bot = telebot.TeleBot("7048929088:AAF3RPjcr00CQiuYahnCWlccH32Q0rNmXGE")

# Sample mess menu data for each day and meal
menu = {
    'Monday': {'Breakfast': '🥞 Pancakes and Tea', 'Lunch': '🍛 Rice and Curry', 'Snacks': '🥟 Samosa', 'Dinner': '🍲 Chapati and Dal'},
    'Tuesday': {'Breakfast': '🍳 Omelette and Bread', 'Lunch': '🍗 Biryani', 'Snacks': '🍤 Pakora', 'Dinner': '🍤 Fried Rice and Chicken'},
    'Wednesday': {'Breakfast': '🍛 Idli and Sambar', 'Lunch': '🍲 Pulao', 'Snacks': '🍪 Biscuits', 'Dinner': '🍽 Chapati and Paneer'},
    'Thursday': {'Breakfast': '🥗 Poha', 'Lunch': '🍛 Rajma Rice', 'Snacks': '🥠 Kachori', 'Dinner': '🍛 Dosa and Sambar'},
    'Friday': {'Breakfast': '🥔 Aloo Paratha', 'Lunch': '🍗 Chicken Curry', 'Snacks': '🥜 Namkeen', 'Dinner': '🍲 Dal Fry and Rice'},
    'Saturday': {'Breakfast': '🥘 Puri Bhaji', 'Lunch': '🐟 Fish Curry', 'Snacks': '🥪 Sandwich', 'Dinner': '🍜 Noodles and Soup'},
    'Sunday': {'Breakfast': '🍛 Upma', 'Lunch': '🍽 Chole Bhature', 'Snacks': '🍰 Cake', 'Dinner': '🍕 Pizza'}
}

# Start Command Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    for day in menu.keys():
        markup.add(InlineKeyboardButton(text=day, callback_data=day))

    bot.reply_to(message, "Welcome to the Mess Menu Bot! 🍽\nPlease select a day:", reply_markup=markup)

# Handle Day Selection from Buttons
@bot.callback_query_handler(func=lambda call: call.data in menu.keys())
def select_day(call):
    day = call.data
    markup = InlineKeyboardMarkup()

    # Add meal options as buttons
    meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']
    for meal in meals:
        markup.add(InlineKeyboardButton(text=meal, callback_data=f"{day}_{meal}"))

    bot.send_message(call.message.chat.id, f"🍽 You've selected {day}. Now choose a meal:", parse_mode='Markdown', reply_markup=markup)

# Handle Meal Selection
@bot.callback_query_handler(func=lambda call: any(day in call.data for day in menu.keys()))
def select_meal(call):
    day, meal = call.data.split('_')
    meal_menu = menu[day].get(meal, "No meal information available.")

    bot.send_message(call.message.chat.id, f"🍽 {meal} on {day}:\n\n{meal_menu}", parse_mode='Markdown')
    
# Polling
bot.polling()