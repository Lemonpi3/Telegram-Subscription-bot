import pandas as pd
from telethon import TelegramClient
from Configs import BotSettings
from datetime import datetime,timedelta
from Scripts.Utils import bcolors, get_random_code
from Scripts.SubKicker import SubKicker
from Scripts.SubManager import SubManager, get_subdb

class SubChecker:
    '''
        * Revisa si hay subs vencidos o por vencer.
        * Actualiza a inactivos a los vencidos y llama el kickeo.
        * Avisa a los que se estan por vencer una unica vez hasta renovar.
    '''
    def __init__(self,client:TelegramClient,debug:bool):
        self.client = client
        self.debug=debug
        self.db = self.get_subdb()
        print(f'{bcolors.DEBUG_SUCCESS} <SubChecker> Iniciado')

    async def check_subs(self)->"tuple[int,int]":
        kickeados , advertidos = await self.check_vencimientos_all()
        kickeados = kickeados + await self.check_colados()
        return kickeados , advertidos

    async def check_vencimientos_all(self):
        db = self.db #No tenia ganas de cambiar todo.
        if not db:
            return 0,0
        
        #Vencidos
        cond_kick=(
            (db['User Tier'] != BotSettings.USER_TIER_ADMIN) &
            (db['User Tier'] != BotSettings.USER_TIER_PERMASUB) &
            (db['Status del Servicio'] == 'ACTIVO') &
            (db['Vencimiento'] < datetime.today() + timedelta(1))   
        )
        
        kickeados = db.loc[cond_kick]

        for user_id in kickeados['ID'].unique():
            await SubKicker.kick_user(self.client,int(user_id),razon='Vencido')
            SubManager.update_cols_value(user_id,['Status del Servicio','Codigo'],['INACTIVO',get_random_code()])

        #Advertencia de vencimiento
        cond_warned = (
            (db['User Tier'] != BotSettings.USER_TIER_ADMIN) &
            (db['User Tier'] != BotSettings.USER_TIER_PERMASUB) &
            (db['Status del Servicio'] == 'ACTIVO') &
            (db['Vencimiento'] > datetime.today() + timedelta(1)) &
            (db['Vencimiento'] < datetime.today() + timedelta(2))
        )

        warned = db.loc[cond_warned]
        success_warn = 0
        for user_id in warned['ID'].unique():
            #Para no spamearle a la gente
            if db.loc[db.ID == user_id]['Advertencia Vencimiento'] != 'SI':
                await SubKicker.warn_user_expiration(self.client,int(user_id),db.loc[db.ID == user_id]['Idioma'])
                SubManager.update_cols_value(user_id=user_id,cols=['Advertencia Vencimiento'],values= ['SI'])
                success_warn = success_warn + 1
        
        return len(kickeados), success_warn

    async def check_colados(self):
        chats = pd.read_excel(BotSettings.CHATSDB_LOC)
        count = 0
        for chat in chats[chats.Categoria != BotSettings.PUBLIC_CATEGORY]['ID output'].unique():
            user_list = await self.client.get_participants(int(chat))
            for _user in user_list:
                if not int(_user.id) in self.db.ID.unique():
                    await SubKicker.kick_user(self.client,int(_user.id),razon='Colado')
                    count += 1
                    
        return count

    def get_user_status(self,user_id)->dict:
        df = self.get_subdb()
        user_data = df.loc[df.ID == int(user_id)].iloc[0].to_dict()
        return user_data

    def get_subdb(self)->pd.DataFrame:
        try: 
            db=pd.read_excel(BotSettings.SUBSDB_LOC)
            if not len(db):
                print(f'{bcolors.ERROR} No se encontraron usuarios en subdb.')
                return None
            return db
        except:
            print(f'{bcolors.ERROR_CRITICO} No se encontro subdb.')
            return None