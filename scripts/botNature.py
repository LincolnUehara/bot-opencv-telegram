import telegram
from scripts import botManag

class botPersonality:
    '''
    userText : The message that user sent in the chat.
    replyText : The message that bot will send to user in the chat.
    optionsBoard : Options offered to the user in key button format.
    imageName : The name of the image to be sent in the chat.
    methodExec : The name of the method to be executed.
    addReaction() : method to add the bot's reaction to enforce its personality.
    '''

    def __init__(self, userText = None, replyText = None, optionsBoard = None,
                 imageName = None, methodExec = None, methodArg = None):
        
        # Create a list of reactions for bot
        self.reactionList = []

        # Defining keywords for dictionary to not mistype
        self.userTextKey = "userTalk_key"
        self.replyTextKey = "replyText_key"
        self.optionsBoardKey = "OptionsBoard_key"
        self.imagePathKey = "imagePath_key"
        self.methodExecKey = "methodExec_key"
        self.methodArgKey = "methodArg_key"
        
        self.addReaction(userText = userText,
                        replyText = replyText,
                        optionsBoard = optionsBoard,
                        imageName = imageName,
                        methodExec = methodExec,
                        methodArg = methodArg)
    
    def addReaction(self, userText = None, replyText = None, optionsBoard = None,
                    imageName = None, methodExec = None, methodArg = None):
        
        # Create a dictionary to react properly to received message
        reactDictionary = {}

        # If the user sent a archive, for example, will be stored None value.
        # For this reason, is better to create a separated objects to treat files.  
        reactDictionary[self.userTextKey] = userText

        # Store the array of reply by bot to be sent.
        if (replyText != None):
            reactDictionary[self.replyTextKey] = replyText
        
        # Create keyboard markup based on array of strings, and store it.
        if (optionsBoard != None):
            optionsArray = self.createArrayForButton(optionsBoard)
            optionsMarkup = telegram.ReplyKeyboardMarkup(optionsArray, \
                                resize_keyboard = True, one_time_keyboard = True)
            reactDictionary[self.optionsBoardKey] = optionsMarkup
        
        # Store the path of the image to be sent.
        if (imageName != None):
            reactDictionary[self.imagePathKey] = (botManag.getImagePath() + imageName)
        
        # Store the address of the method to be executed.
        if (methodExec != None):
            reactDictionary[self.methodExecKey] = methodExec
        
        # Store the arguments for the method to be executed.
        if (methodArg != None):
            reactDictionary[self.methodArgKey] = methodArg

        # Append this reation to the list.
        self.reactionList.append(reactDictionary)

    def action(self, bot, update):
        
        chat_id = update.message.chat_id
        username = update.message.from_user.first_name
        message = update.message.text
        
        # Check for all the items in the reaction list
        for item in self.reactionList:
            
            # If there is a prepared reaction to the received message from the
            # user, send its related reply, board markup, image and execute
            # related method, if they are registered beforehand.
            if (item[self.userTextKey] == message):

                if self.replyTextKey in item:
                    for text in item[self.replyTextKey]:
                        bot.sendMessage(chat_id = chat_id, text = text)
                
                if self.optionsBoardKey in item:
                    bot.sendMessage(chat_id = chat_id, text = "⏬⏬⏬⏬⏬",
                                    reply_markup = item[self.optionsBoardKey])
                
                if self.imagePathKey in item:
                    bot.sendPhoto(chat_id = chat_id,
                                  photo = open(item[self.imagePathKey], 'rb'))
                
                if self.methodExecKey in item:
                    if self.methodArgKey in item:
                        item[self.methodExecKey](bot, update, item[self.methodArgKey])
                    else:
                        item[self.methodExecKey](bot, update)

    def createArrayForButton(self, options_array):

        return_array = []
        index = 0

        for _ in options_array:
            item = [telegram.KeyboardButton(options_array[index])]
            return_array.append(item)
            index += 1

        return return_array

# If this file was run directly, exit leaving a message.
if __name__ == "__main__":
    print("This script is not the main script to run.\n")
    print("Please check the documents.\n")
    exit()