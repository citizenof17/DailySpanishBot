
import telebot
import constants
import random
import threading


bot = telebot.TeleBot(constants.token)

words = constants.words
n = len(words)
iterator = random.randrange(0, n)
PERIODIC_ID = constants.per_id
TIMER = constants.timer


def create_answer():
    global iterator
    answer = 'Слово: ' + words[iterator][0] + '\nЗначение: ' + words[iterator][1]
    iterator = (iterator + 1) % n
    return answer


def log(message, answer):
    print("<Message>\n\t<From>\n\t\t{0} {1} (id {2})\n\t</From>\n\t<text>\n\t\t{3}\n\t</text>"
          "\n\t<answer>\n\t\t{4}\n\t</answer>\n</Message>".format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                  str(message.from_user.id),
                                                                  message.text,
                                                                  answer))


@bot.message_handler(commands=['help'])
def handle_text(message):
    answer = """Я всего лишь маленький бот и пока умею очень мало, но я стараюсь!
Каждый день я буду (пока нет) давать тебе новое слово и его объяснение
Чтобы получить следующее слово, введи /next
Чтобы начать сначала, введи /start"""
    bot.send_message(message.from_user.id, answer)
    # log(message, answer)


@bot.message_handler(commands=['next'])
def handle_text(message):
    answer = create_answer()
    bot.send_message(message.from_user.id, answer)
    # log(message, answer)


@bot.message_handler(commands=['start'])
def handle_text(message):
    global iterator
    iterator = 0
    answer = create_answer()
    bot.send_message(message.from_user.id, answer)
    # log(message, answer)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    answer = 'Просто текст?'
    bot.send_message(message.from_user.id, answer)
    # log(message, answer)


def send_message_perm(per_id):
    answer = create_answer()
    bot.send_message(per_id, answer)
    threading.Timer(TIMER, send_message_perm(per_id)).start()


def main():
    random.shuffle(words)
    send_message_perm(PERIODIC_ID)
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
