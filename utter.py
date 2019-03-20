# from bot import Bot2
from bot import Bot2_neo

if __name__ == '__main__':
    # bot = Bot2("vocabulary.txt")
    # bot.utter(10)
    #
    bot = Bot2_neo("vocabulary_DB.txt")
    for i in range(100):
        print(bot.utter())
