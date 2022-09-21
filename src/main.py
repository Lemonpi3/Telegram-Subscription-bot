from telethon import TelegramClient
from Configs import APIkeys, BotSettings, InviteBotSettings
from Scripts.DataBaseManager import ChatsDB, ClientDB
from Scripts.SubManagerBot import SubManagerBot
from Scripts.InviteBot import InviteBot

api_id, api_hash, phone, bot_token, bot_token_submanager= APIkeys.get_api_keys()

bot_client= TelegramClient(InviteBotSettings.INVITE_BOT_SESSION_NAME, api_id,  api_hash).start(bot_token=bot_token)
submanager_bot_client = TelegramClient(BotSettings.SUBMANAGER_BOT_SESSION_NAME, api_id,  api_hash).start(bot_token=bot_token_submanager)
client=  TelegramClient(BotSettings.SESSION_NAME, api_id,  api_hash, sequential_updates = True).start(phone=phone)

async def main():
    await ChatsDB(client=client,debug=BotSettings.DEBUG_CHATSDB,create_db=BotSettings.GENERATE_EXCEL_CHATSDB).Init_ChatDB()
    ClientDB(client=client,debug=BotSettings.DEBUG_CLIENTDB,create_db=BotSettings.GENERATE_EXCEL_CLIENTDB).Init_ClientDB()
    await InviteBot(bot_client,client).StartBot()
    await SubManagerBot(bot_client=submanager_bot_client,human_client=client).StartBot()

with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()