# OpenCV with Telegram Bot

[![License](https://img.shields.io/github/license/LincolnUehara/bot-opencv-telegram)](https://github.com/LincolnUehara/bot-opencv-telegram/blob/master/LICENSE)
![Maintenance](https://img.shields.io/maintenance/no/2018)

<p align="center">
<img src="https://github.com/LincolnUehara/bot-opencv-telegram/blob/master/scripts/images/OpenCV_plus_Telegram.jpg" width="256">
</p>

### Purpose 

This code was intended to study about python language. In this example the user have interaction with face recognition via OpenCV using Telegram Bot.

### Requirements

* A smartphone with Telegram App.
* Wherever linux system to run this code.

### Configuration instructions

##### BotFather and token

Fisrtly you have to talk with [BotFather](https://telegram.me/botfather) to create a bot and receive its Token. Copy-paste it in `botToken` variable at `startBot.py` file.

Not sure how to get this-so-called "token"? Maybe [this tutorial](https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39) could help ya o/

##### OpenCV

You need to install a bunch of stuffs to run OpenCV in your machine.

Adrian Rosebrock wrote a [wonderful and complete tutorial to install OpenCV](https://www.pyimagesearch.com/opencv-tutorials-resources-guides/). Be careful to not use `sudo` to install tools, otherwise this code will not have permission to access Python and Telegram libraries.

Moreover, a lot of code written by Adrian is used here.

### Operating instructions

##### On the machine where the script will run

Just run the script called `startBot.py`.

##### On Telegram App

Send `/start` to init a conversation with the bot.

Send a picture to bot, and a list of options is send back.

Send `/learn` to do a training with the dataset.

### Author

Lincoln Uehara

### More

* [Bot Code Examples](https://core.telegram.org/bots/samples)

* [Face recognition with OpenCV, Python, and deep learning](https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/)

* [Raspberry Pi Face Recognition](https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/)
