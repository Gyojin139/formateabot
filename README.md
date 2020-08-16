# FormateaBot
Code of @FormateaBot in Telegram

## Installation

Execute in bash the commands in the file `requirements.txt`

You will need a token from [BotFather](https://telegram.me/botfather) and the ID of a channel where to send the Inline stickers. 
You can get the second by creating a new channel, introducing the newly created bot and sending a message to the channel. 
Then, the ID of the channel will be displayed in the information of the received message from the bot API.

Introduce the token in a file called `token.txt` and the channel where to send the stickers in a file called `sticker_dumper.txt`

## Running

Execute
```
nohup python3 bot.py &
```
