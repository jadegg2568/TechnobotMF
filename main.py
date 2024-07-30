import msghandler
import config

from javascript import require, On

import threading
import os

mineflayer = require("mineflayer")


class MineflayerBot:
    def __init__(self):
        self.bot = None

    def start(self):
        self.bot = mineflayer.createBot({
            "host": config.ip,
            "port": config.port,
            "username": config.nickname
        })

        @On(self.bot, "message")
        def message_handler(_self, message, *args):
            global bot
            msg = message.getText()
            if msg == "":
                return
            handle_message(msg)

        @On(self.bot, "kicked")
        def kicked_handler(_self, reason, loggedIn, *args):
            error(str(reason))
            self.end()

        @On(self.bot, "error")
        def error_handler(_self, err, *args):
            error(str(err))
            self.end()

    def end(self):
        try:
            self.bot.end()
        except:
            pass
        self.bot = None

    def is_started(self):
        return self.bot is not None

    def right_click(self):
        self.bot.activateItem(False)

    def players_list(self):
        return self.bot.players

    def send_bot_message(self, message):
        if message is None or message == "":
            return
        self.bot.chat(message)


def execute_command(cmd):
    global bot
    split = cmd.split(" ")
    name = split[0]
    args = split[1:]
    label = " ".join(split)

    if name == ".nickname":
        if len(args) < 1:
            return "Ошибка: Неправильный синтаксис."
        nickname = args[0]
        if len(nickname) > 15:
            return "Ошибка: Никнейм не должен привышать 15 символов."

        config.nickname = nickname
        return f"Сменён ник на {nickname}."

    elif name == ".start":
        if bot.is_started():
            return "Ошибка: Бот уже запущен."
        bot.start()

    elif name == ".end":
        if not bot.is_started():
            return "Ошибка: Бот не запущен."
        bot.end()
        return "Бот завершил свою работу."

    elif name == ".restart":
        if not bot.is_started():
            return "Ошибка: Бот не запущен."
        bot.start()
        bot.end()
        return "Бот рестартнут."

    elif name == ".online":
        online = ""
        for player in bot.players_list():
            online += player + "   "
        return online

    elif name == ".chatfile":
        if len(args) < 2:
            return "Ошибка: Неправильный синтаксис."
        name = args[0]
        cooldown = args[1]

        if not os.path.exists(name):
            return f"Ошибка: Файл \"{name}\" не найден."
        try:
            int(cooldown)
        except:
            return f"Ошибка: {cooldown} не является числом."
        file = open(name, encoding="utf8")
        content = file.read()
        lines = content.replace("\r", "").split("\n")
        msghandler.chat_lines(bot, lines, int(cooldown))

    elif label.startswith("."):
        return "Ошибка: Неизвестная команда."
    elif label.startswith("!!"):
        return None
    else:
        if bot is None:
            return None
        elif len(cmd) > 130:
            return "Ошибка: Слишком большое сообщение."
        try:
            bot.send_bot_message(cmd)
        except:
            pass
    return None


def console_handler():
    while True:
        user_input = input(">")
        result = execute_command(user_input)
        if result is not None:
            print(result)


def handle_message(msg):
    global bot
    msghandler.handle_message(bot, msg)


def error(msg):
    print("-------------ERROR--------------\nS"
          + f"{msg}\n"
          + "-------------------------------")
    print("Mineflayer-Бот аварийно завершил свою работу.")


def main():
    t = threading.Thread(target=console_handler)
    t.start()


bot = MineflayerBot()
autochat_data = dict()


if __name__ == "__main__":
    main()