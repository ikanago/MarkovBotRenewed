from bot import Bot

if __name__ == '__main__':
    bot = Bot("vocabulary_DB.txt")
    for i in range(10):
        print(bot.generate_text())
