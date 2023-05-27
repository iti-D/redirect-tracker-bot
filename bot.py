import telebot
import subprocess
import json
from DB_handling import id_to_db, num_of_users, retrive_ids
import time

# Replace with your Telegram bot token
bot = telebot.TeleBot('TOKEN')

# Replace with your Telegram user ID (you can get it by sending a message to @userinfobot)
bot_owner_id = 111111

# Counter for the number of link messages received
link_count = 0

# Command to start the bot and welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a link and I'll try to dereference it.\n Send /help for more info")
    id_to_db(message.from_user.id)


# Command for help and more info to user
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Hello!\nI was created by @UnitedStatesOfEurasia, using deref.link API.\n"
                          "Just send a link, and I'll show you where the really goes, including intermediate stops in between!\n"
                          "It is important to know where the link is leading, before clicking it!\n"
                          "so forward me any link you receive before clicking on it!\n"
                          "Read more here: https://en.wikipedia.org/wiki/URL_shortening#Privacy_and_security\n"
                          "")



# Handler for messages containing links
@bot.message_handler(regexp=r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+')
def handle_link(message):
    global link_count
    link_count += 1
    link = message.text.strip()
    try:
        output = subprocess.check_output(['curl', '-s', '-d', 'url={}'.format(link), 'https://deref.link/deref']).decode('utf-8')
        result = json.loads(output)
        response = "Here's what I found:\n\n"
        response += "Start URL: {}\n".format(result['start_url'])
        response += "Final URL: {}\n".format(result['final_url'])
        response += "Final Domain: {}\n".format(result['final_domain'])
        response += "\nRoute Log:\n"
        for i, url in enumerate(result['route_log'], start=1):
            response += "{}. {}\n".format(i, url)
        bot.reply_to(message, response)

    except KeyError as e:
        bot.reply_to(message, "There seem to have been a problem with the link or with the API, please send it to me @UnitedStatesOfEurasia, and I'll try to fix that!\n or try again later....\nMake sure you send ONLY the link.")
        error_note = "Error: " + str(e) + "\n Message:\n" + str(message.text) + "\n userID: " + str(message.from_user.id) 
        bot.send_message(chat_id=390034852, text=error_note)
    time.sleep(0.4)


# Handler for bot owner commands
@bot.message_handler(commands=['send', 'stats'])
def handle_owner_commands(message):
    global link_count
    if message.from_user.id == 1111111:
        if message.text.startswith('/stats'):
            the_stats = str(num_of_users()) + "\n Links count: " + str(link_count)
            bot.reply_to(message, the_stats)
        elif message.text.startswith('/send'):
            ids = retrive_ids()
            notice = message.text.split(maxsplit=1)[1::]
            for acc in ids:
                try:
                    bot.send_message(chat_id=acc, text=notice)
                except:
                    continue

    else:
        bot.reply_to(message, "I'm sorry, I only handle links. Send me a link and I'll try to dereference it.")


#handler for non-link messages
@bot.message_handler(func=lambda message: True)
def handle_nonlink(message):
    bot.reply_to(message, "I'm sorry, I only handle links. Send me a link and I'll try to derefrence it.")

bot.polling()
