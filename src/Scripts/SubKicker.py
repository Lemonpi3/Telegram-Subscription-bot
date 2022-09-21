import pandas as pd
from telethon import TelegramClient
from Configs import BotSettings
from datetime import datetime
from Scripts.Utils import bcolors

class SubKicker:
    '''
    * Kickea usuarios de grupos.
    * Alerta usuarios que estan por vencer
    '''
    def __init__(self,debug:bool=False):
        self.debug=debug

    async def warn_user_expiration(client:TelegramClient,user_id:int,idioma:str):
        '''Le avisa al usuario que esta vencerce'''
        if idioma == 'ES':
            await client.send_message(user_id,BotSettings.WARN_MSG_ES)
        if idioma == 'EN':
            await client.send_message(user_id,BotSettings.WARN_MSG_EN)

    async def kick_user(client:TelegramClient,user_id:int,categorias:"list[str]"=None,razon=None):
        '''
        Kickea usuarios del grupo.
        * Si no se pasan categorias se asume que se kickea de todos los grupos
        '''
        chats = pd.read_excel(BotSettings.CHATSDB_LOC)
        log_df = pd.read_excel(BotSettings.KICKS_LOGS_LOC)
        
        #Logueo el usuario
        log_user = {
                        'ID':user_id,
                        'Razon':razon,
                        'Fecha':datetime.today().isoformat(),
                    }

        log_df.append(log_user,ignore_index=True)
        log_df.to_excel(BotSettings.KICKS_LOGS_LOC,index=False)
        #Lo kickeo
        if not categorias:
            for chat in chats[chats.Categoria != BotSettings.PUBLIC_CATEGORY]['ID output'].unique():
                try:
                    await client.kick_participant(int(chat),user_id)
                except:
                    continue
            
            print(f'{bcolors.DEBUG_WARN} Se kickeo {user_id} de todos los grupos. Razon: {razon}')
            return
        