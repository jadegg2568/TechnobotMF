import recorder

import config
import time
import random


def handle_message(bot, msg):
    if "■" in msg:
        return

    print(msg)

    if config.message_output:
        recorder.record_message(msg)

    if "→" in msg:
        handle_player_message(bot, msg)

    elif "› Игрок " in msg:
        handle_player_join(bot, msg)



def handle_player_message(bot, msg):
    nickname = extract_nickname(msg)
    message = extract_message(msg)
    if nickname is None: return

    if config.message_responses is not None:
        try:
            if len(config.message_responses) != 0:
                response = random.choice(config.message_responses)
                bot.send_bot_message(response.replace("%nickname%", nickname))
        except:
            pass


def handle_player_join(bot, msg):
    nickname = msg.split(" ")[3]

    if config.join_responses is not None:
        try:
            if len(config.join_responses) != 0:
                response = random.choice(config.join_responses)
                bot.send_bot_message(response.replace("%nickname%", nickname))
        except:
            pass       


def chat_lines(bot, lines, cooldown):
    for line in lines:
        if not bot.is_started():
            return
        bot.send_bot_message(f"!{line}")
        time.sleep(cooldown)


def extract_nickname(msg):
    parts = msg.split(" ")
    for i in range(2, len(parts)):
        if "[" in parts[i] and not "[" in parts[i + 1]:
            return parts[i + 1]
    return None


def extract_message(msg):
    return msg.split("→ ")[1]