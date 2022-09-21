# Telegram-Subscription-bot
Showcase of a project that I did for a client using telethon library, some features have been removed prior to upload due to client demands. 

### Lenguage:
* python
* docker
### Main libraries used: 
* pandas
* telethon

## What the proyect was about

### My client wanted:
* A telegram bot to automatically invite people to my client's channels when they disired as well as working as an information center for the users of this bots 
(About us, What we do, etc)
* A subscription system to manage the trial and diferent tiers of premium users. (kick users when their subscription expire, notify them with promotions, etc) 
* A manual way to add/update subscriptions
* A way to broadcast to the private channels and another one for the public channels (Not in the repo due to client's demand)
* A way to keep track of subscription sales (when, who and how much a subscriber paid)

There were two issues with the proyect and how we solved with my client

>

My client wanted to control and check de databases by himself, and have the hability edit some of them manually if necesary, but didn't know SQL and wasn't in the mood to learn it.
So, bettween testing possible alternatives and getting feedback for alternatives with my client (while telling him the pros an cons of each), we settle down in an excel database. It wasn't a big deal from code perspective
(I had to use pandas and write a couple more lines compared to SQL) and niether from a functionality perspective, since most of the data that was going in was static.
>
The second issue was that my client wasn't totaly sure if he wanted to host it himself on his pc or on the cloud and wasn't giving me a direct choice. So just in case I made
a dockerfile and a few lines in the code to make it self host and easy to port into the cloud at the same time.

## API Keys Setup
### For Python:
Check src\Configs\APIkeys.py for instructions (you can set them in that file or as enviroment variables).
### For Docker:
Set up your keys in the dockerfile, the variable CLOUDHOST must be 1
## Bots Configs:
#### General Bot Settings:
On src\Configs\BotSettings.py you can find all the configs for User tiers, admins, trial days, header msg for public channels msgs and a few more general settings.
#### Invite Bot Settings: 
On src\Configs\InviteBotSettings.py you can find the invitebot dialogs and buttons settings for each language.
#### ChatsDB:
On src\Data\chatsdb.xlsx this excel sheet is used for generating the links and for the broadcast module that it's not included.

## Run it
After setting the keys and chatsdb you can run it in two ways
* Via docker:
1) Navigate with console to the dockerfile directory
2) Build the container image by imputing:
`docker build -t <the name that you want>`
3) Run the container: `docker run -dp 3000:3000 <the name that you set on the previous step>` and the bot should start.

* Via Python:
1) Navigate to the src folder with console and run `pip install -r requirements.txt` to install dependencies (it's recomended to use a new virtual enviroment before installing dependencies).
2) You should be in the same folder as main.py in the console (if not navigate to it) run the command: `python main.py` and the bot should start.
