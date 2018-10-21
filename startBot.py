import time
import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from scripts import botNature, botAction

# Token of your bot on Telegram
botToken = 'XXXXXXXXX:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Set the bot and start running it
updater = Updater(botToken)
dispatcher = updater.dispatcher
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
updater.start_polling()

#
# Make default message for "/start" command
#
command = "start"
startMessage = ["Hi USER! How are ya?",
                "What may I do for ya?"]
startOptions = ["I need a little help from ya, bot",
                "I'm tottaly fine"]
startObj = botNature.botPersonality(userText = ("/" + command),
                                    replyText = startMessage,
                                    optionsBoard = startOptions)
start_handler = CommandHandler(command, startObj.action)
dispatcher.add_handler(start_handler)

#
# Make default message for "/learn" command
#
command = "learn"
learnMessage = ["Generating Pickles..."]
learnObj = botNature.botPersonality(userText = ("/" + command),
                                    replyText = learnMessage,
                                    methodExec = botAction.generatePickles)
learn_handler = CommandHandler(command, learnObj.action)
dispatcher.add_handler(learn_handler)

#
# Make default message for received images
#
imageMessage = ["So, what do you want to do with this image?"]
imageOptions = ["Register the person above",
                "Analyse the photo",
                "Sorry, wrong chat!"]
photoObj = botNature.botPersonality(replyText = imageMessage,
                                    optionsBoard = imageOptions,
                                    methodExec = botAction.saveImage)
photo_handler = MessageHandler(Filters.photo, photoObj.action)
dispatcher.add_handler(photo_handler)

#
# If any other kind of message is sent by the user
#
reactObj = botNature.botPersonality()
react_handler = MessageHandler(Filters.text, reactObj.action)
dispatcher.add_handler(react_handler)

# Reaction No.1: "I need a little help from ya, bot"
# TODO: Not completely implemented...
reaction1 = ["What kind of help do ya need?"]
reactObj.addReaction(userText = startOptions[0],
                     replyText = reaction1)

# Reaction No.2: "I'm tottaly fine"
reaction2 = ["Nice!\nNow I'm at kitchen preparing a nice cake 🍰, " +
            "but Gordon Ramsay is yelling at me, ... I don't know why... ='("]
reactObj.addReaction(userText = startOptions[1],
                     replyText = reaction2,
                     imageName = "angry_gordon.jpg")

# Reaction No.3: "Register the object/person above"
reactObj.addReaction(userText = imageOptions[0],
                     methodExec = botAction.registerName)

# Reaction No.4: "Analyse the photo"
reactObj.addReaction(userText = imageOptions[1],
                     methodExec = botAction.identifyPhoto)

# Reaction No.5: "Sorry, wrong chat!"
reaction5 = ["Nah, that's ok 😉"]
reactObj.addReaction(userText = imageOptions[2],
                     replyText = reaction5)

while 1:
    time.sleep(1000)