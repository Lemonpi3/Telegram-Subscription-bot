import pandas as pd

from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.functions.messages import ExportChatInviteRequest
from datetime import timedelta,datetime

from Configs import InviteBotSettings , BotSettings
from Scripts.SubManager import SubManager
from Scripts.Utils import bcolors, get_random_code

class InviteBot:
    '''Bot publico, se encarga de agregar usuarios prueba, permitirle al usuario ver su status e info de todo'''

    def __init__(self,bot_client:TelegramClient,human_client:TelegramClient):
        self.client = bot_client
        self.human_client = human_client
        
    async def StartBot(self):
        print("<inivteBot> InviteBot Iniciado")

        @self.client.on(events.NewMessage(pattern='/(?i)start')) 
        async def test(event):
            # get the sender
            sender = await event.get_sender()

            # Start a conversation
            async with self.client.conversation(await event.get_chat(), exclusive=True) as conv:
                keyboard = [
                    [Button.inline(f"Español", 'ES')],
                    [Button.inline(f"English", 'EN')],
                ]
                await conv.send_message(message=InviteBotSettings.INTRO_TXT, parse_mode='html')
                await conv.send_message(message=InviteBotSettings.INTRO_OPTION_TXT, buttons=keyboard, parse_mode='html')
                press = await conv.wait_event(events.CallbackQuery(sender.id))
                choice = str(press.data.decode("utf-8"))

                await menu(conv,sender,choice)

                await conv.cancel_all()
                return 

        async def menu(conv,sender,idioma):
            keyboard =InviteBotSettings.MENU_BUTTONS[idioma]
            await conv.send_message(message=InviteBotSettings.MAIN_MENU_TITLE[idioma],buttons=keyboard, parse_mode='html')
            press = await conv.wait_event(events.CallbackQuery(sender.id))
            choice = str(press.data.decode("utf-8"))

            if choice=='trial':
                data, status = SubManager().add_new_user(sender.id,idioma,0,['DEMO'],BotSettings.TRIAL_DAYS,True,sender.username,False)
                if status == 'USED_TRIAL':
                    await conv.send_message(message=InviteBotSettings.USED_TRIAL_MSG[idioma])
                try:
                    codigo = data['Codigo']
                    status = await self.generar_links(conv,sender.id,idioma,codigo)
                except:
                    codigo = data['Codigo']
                    vencimiento = data['Vencimiento']
                    await conv.send_message(message=InviteBotSettings.VALID_TRIAL_ALT_MSG[idioma].format(codigo,vencimiento))
                else:
                    await conv.send_message(message=InviteBotSettings.INVALID_USER_EXTREME_ERROR_MSG[idioma])
                
                await return_to_main_menu(conv,sender,idioma)
                
            elif choice == 'sub':
                await conv.send_message(message=InviteBotSettings.SUB_TXT[idioma])
                await return_to_main_menu(conv,sender,idioma)

            elif choice == 'code':
                await conv.send_message(message=InviteBotSettings.INSERT_CODE_MSG[idioma])
                data = await conv.wait_event(events.NewMessage(sender.id))
                data=data.message

                try:
                    status = await self.generar_links(conv,sender.id,idioma,data.message)
                    
                    if status == 'MISSING_USER':
                        await conv.send_message(message=InviteBotSettings.USER_NOT_IN_DB)
                    elif status == 'INVALID_CODE':
                        await conv.send_message(message='Codigo invalido/expirado')
                except:
                    await conv.send_message(message=InviteBotSettings.INVALID_USER_EXTREME_ERROR_MSG[idioma])
                    raise
                
                await return_to_main_menu(conv,sender,idioma)

            elif choice == 'about':
                await about(conv,sender,idioma)

            elif choice == 'status':
                data = SubManager().get_user_info(sender.id)
                if data:
                    status = data['Status del Servicio']
                    plan = BotSettings.get_tier_names(idioma,data['User Tier'])
                    vencimiento = data['Vencimiento']
                    await conv.send_message(message=InviteBotSettings.USER_STATUS_MSG[idioma].format(status,plan,vencimiento))
                else:
                    await conv.send_message(message=InviteBotSettings.USER_NOT_IN_DB[idioma])

                await return_to_main_menu(conv,sender,idioma)

        async def about(conv,sender,idioma):
            keyboard = InviteBotSettings.ABOUT_BUTTONS[idioma]
            await conv.send_message(message=InviteBotSettings.ABOUT_TITLE[idioma],buttons=keyboard, parse_mode='html')
            press = await conv.wait_event(events.CallbackQuery(sender.id))
            choice = str(press.data.decode("utf-8"))
            if choice=='who':
                await conv.send_message(message=InviteBotSettings.WHO_TXT[idioma],buttons=keyboard)
                await return_to_main_menu(conv,sender,idioma)

            elif choice == 'how':
                await conv.send_message(message=InviteBotSettings.HOW_TXT[idioma],buttons=keyboard)
                await return_to_main_menu(conv,sender,idioma)

            elif choice == 'refer':
                await conv.send_message(message=InviteBotSettings.REFER_TXT[idioma],buttons=keyboard)
                await return_to_main_menu(conv,sender,idioma)

            elif choice == 'back':
                await return_to_main_menu(conv,sender,idioma)

        async def return_to_main_menu(conv,sender,idioma):
                keyboard =InviteBotSettings.RETURN_BUTTONS[idioma]
                await conv.send_message(message=InviteBotSettings.RETURN_TXT[idioma],buttons=keyboard, parse_mode='html')
                press = await conv.wait_event(events.CallbackQuery(sender.id))
                await menu(conv,sender,idioma)

    async def generar_links(self,conv,user_id,idioma,codigo)->str:
        '''Returns MISSING_USER | INVALID_CODE | SUCCESS'''
        sub_df = pd.read_excel(BotSettings.SUBSDB_LOC)
        chat_df = pd.read_excel(BotSettings.CHATSDB_LOC)
        chat_df['Chat output'] = chat_df['Chat output'].astype("category")
        chat_df['Chat output'] = chat_df['Chat output'].cat.set_categories(InviteBotSettings.ORDEN_LINKS)
        user_data = None

        try:
            user_data = sub_df.loc[sub_df.ID==user_id].iloc[0]
            print(user_data)
        except:
            return 'MISSING_USER'

        if codigo != user_data['Codigo']:
            await conv.send_message(message= InviteBotSettings.INVALID_CODE_MSG[idioma])
            return 'INVALID_CODE'

        canales = []
        canales_id = []

        for categoria in user_data['Categorias'].split('-'):
            #Todos los canales para ES, Solo EN para EN
            if user_data['Idioma'] != 'EN':
                canales = canales + list(chat_df[chat_df['Categoria']==categoria].sort_values('Chat output')['Chat output'].values)
                canales_id = canales_id + list(chat_df[chat_df['Categoria']==categoria].sort_values('Chat output')['ID output'].values)
            else:
                canales = canales + list(chat_df[(chat_df['Categoria']==categoria) & (chat_df.Idioma == 'EN')]['Chat output'].values)
                canales_id = canales_id + list(chat_df[(chat_df['Categoria']==categoria) & (chat_df.Idioma == 'EN')]['ID output'].values)

        print(canales,canales_id)
        canales = list(dict.fromkeys(canales))
        canales_id = list(dict.fromkeys(canales_id))

        await conv.send_message(message=InviteBotSettings.LINK_GENERATING_MSG[idioma])
        links = []

        for grupo in canales_id:
            try:
                link = await self.human_client(ExportChatInviteRequest(int(grupo),expire_date=(datetime.today() + timedelta(hours=12))))
                link = link.link
                links.append(link)
            except:
                print(f'{bcolors.ERROR} No se pudo crear link para {grupo}')
        
        temp = [InviteBotSettings.LINKS_MSG[idioma].format(canal,link) for canal,link in zip(canales,links)]

        msg='\n'.join(temp)+InviteBotSettings.LINK_RETRIVAL_MSG[idioma]
        await conv.send_message(message=msg,parse_mode='html')

        new_code = get_random_code()
        print(f'nuevo codigo: {new_code}, links {links}')
        sub_df.loc[sub_df.ID == int(user_id),['Codigo']] = new_code
        sub_df.to_excel(BotSettings.SUBSDB_LOC,index=False)

        return 'SUCCESS'