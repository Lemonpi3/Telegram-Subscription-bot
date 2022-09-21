import pandas as pd
from telethon import TelegramClient, events
from telethon.tl.custom import Button
from Configs import BotSettings
from Scripts.SubManager import SubManager
from Scripts.SubChecker import SubChecker
from Scripts.Utils import bcolors
from datetime import datetime

class SubManagerBot:
    '''Maneja manualmente los usuarios de telegram.

    El bot puede:
    * Agregar un usuario premium
    * Checkear estado de usuarios
    * Checkear lo abonado y dividirlo(11/9/2022: No implementado todavia)
    '''
    def __init__(self,bot_client:TelegramClient,human_client:TelegramClient,debug:bool=False):
        self.client= bot_client
        self.human_client= human_client
        self.debug= debug
        self.sub_checker= SubChecker(human_client,debug)
        self.SubManager= SubManager(debug)

    async def StartBot(self):
        @self.client.on(events.NewMessage(pattern='/(?i)start')) 
        async def start(event):
            # get the sender
            sender = await event.get_sender()
            SENDER = sender.id

            # Start a conversation
            async with self.client.conversation(await event.get_chat(), exclusive=True) as conv:
                keyboard = [
                    [Button.inline(f"Agregar Subscripcion Premium", 'NEW_SUB')],
                    [Button.inline(f"Limpiar usuarios vencidos/colados", 'CHECK_SUBS')],
                ]

                await conv.send_message(message='Que quieres hacer?',buttons=keyboard, parse_mode='html')
                press = await conv.wait_event(events.CallbackQuery(SENDER))
                choice = str(press.data.decode("utf-8"))

                if choice=='NEW_SUB':
                    await self.NewUser(conv,SENDER)
                elif choice == 'CHECK_SUBS':
                    await self.CheckUsers(conv,SENDER)

                await conv.cancel_all()
                return
                
        print(f'{bcolors.DEBUG_SUCCESS} <SubManagerBot> Iniciado')

    async def ResetConv(self,conv,sender):
        keyboard = [
                        [Button.inline(f"Agregar/Editar Subscripcion Premium", 'NEW_SUB')],
                        [Button.inline(f"Limpiar usuarios vencidos/colados", 'CHECK_SUBS')],
                    ]

        await conv.send_message(message='Que quieres hacer?',buttons=keyboard, parse_mode='html')
        press = await conv.wait_event(events.CallbackQuery(sender))
        choice = str(press.data.decode("utf-8"))

        if choice=='NEW_SUB':
            await self.NewUser(conv,sender)
        elif choice == 'CHECK_SUBS':
            await self.CheckUsers(conv,sender)
        return

    async def NewUser(self,conv,sender):
        keyboard = [
                [Button.inline(f"Añadir/Editar Nuevo usuario", 'ADD_USER')],
                [Button.inline(f"Volver", 'RETURN')],
            ]
        await conv.send_message(message='CheckSubs Menu',buttons=keyboard, parse_mode='html')
        press = await conv.wait_event(events.CallbackQuery(sender))
        choice = str(press.data.decode("utf-8"))

        if choice=='ADD_USER':
            await conv.send_message(message='Siga los pasos como corresponda, si el usuario ya existe se editara automaticamente', parse_mode='html')
            nuevo_usuario = {}
            await conv.send_message(message='1)Introdusca la ID del usuario', parse_mode='html')
            nuevo_usuario['ID'] = await self.CargarVariable(conv,sender,int)
            await conv.send_message(message='2)Introdusca el lenguaje del usuario (ES o EN)', parse_mode='html')
            nuevo_usuario['lenguaje'] = await self.CargarVariable(conv,sender)
            nuevo_usuario['lenguaje'] = nuevo_usuario['lenguaje'].upper()
            await conv.send_message(message='3)Introdusca el tier del usuario (es un numero): \n-2 = admin\n-1 = permasub\n0=prueba\npremium_X donde X es un numero del 1 al inf = subs premiums (ver botsettings.py para referencia)', parse_mode='html')
            nuevo_usuario['user_tier'] = await self.CargarVariable(conv,sender,int)
            await conv.send_message(message='4)Introdusca las categorias usuario (si es mas de una separadas con "-"\nEj CRYPTO-ACCIONES', parse_mode='html')
            nuevo_usuario['categorias'] = await self.CargarVariable(conv,sender)
            nuevo_usuario['categorias'] = nuevo_usuario['categorias'].upper().split('-')
            await conv.send_message(message='5)Introdusca Dias a Añadir (si quieres quitar pon un numero negativo)', parse_mode='html')
            nuevo_usuario['dias_a_añadir'] = await self.CargarVariable(conv,sender,int)
            await conv.send_message(message='6)Introdusca el nombre del usuario', parse_mode='html')
            nuevo_usuario['name'] = await self.CargarVariable(conv,sender)
            await conv.send_message(message='7)En caso de que se encuentre el usuario, desea sobreescribir las categorias que tenia por las nuevas o agregarlas a las existentes\nResponda SI para sobreescribir o NO para acoplar', parse_mode='html')
            nuevo_usuario['remplazar_categorias'] = await self.CargarVariable(conv,sender)
            nuevo_usuario['remplazar_categorias'] = nuevo_usuario['remplazar_categorias'].upper() == 'SI'
            nuevo_usuario['prueba'] = False

            await conv.send_message(message=f'''
            Se van a agregar estos datos:
            ID:{nuevo_usuario['ID']}
            Idioma:{nuevo_usuario['lenguaje']}
            user_tier:{nuevo_usuario['user_tier']} = {BotSettings.get_tier_names('ES',nuevo_usuario['user_tier'])}
            categorias: {nuevo_usuario['categorias']} (ignora que no esten con el -)
            dias a añadir: {nuevo_usuario['dias_a_añadir']}
            nombre del usuario: {nuevo_usuario['name']}
            remplazar categorias: {nuevo_usuario['remplazar_categorias']} (es true o false)

            Es correcto ? (SI/NO)
            ''', parse_mode='html')
            
            respuesta = await self.CargarVariable(conv,sender)

            if respuesta.upper() != 'SI':
                await conv.send_message(message='Operacion cancelada volviendo al menu de add user...')
                await self.NewUser(conv,sender)
                return

            await conv.send_message(message='Cargando usuario a la base de datos...')
            status,msg = self.SubManager.add_new_user(nuevo_usuario['ID'],nuevo_usuario['lenguaje'],nuevo_usuario['user_tier'],
            nuevo_usuario['categorias'],nuevo_usuario['dias_a_añadir'],nuevo_usuario['prueba'],nuevo_usuario['name'],nuevo_usuario['remplazar_categorias'])
            
            if status:
                try:
                    user_id = status['ID']
                    user_venc = status['Vencimiento']
                    user_code = status['Codigo']
                    await conv.send_message(message=f'Operacion Realizada: {msg}\nSe agrego al usuario.\nSu codigo es {user_code}\nVence el {user_venc}')

                    #Log ventas
                    await conv.send_message(message='Desea agregarlo al log de ventas? (SI/NO)')
                    respuesta = await self.CargarVariable(conv,sender)
                    if respuesta.upper() == 'SI':
                        await conv.send_message(message='Porfavor indique la cantidad(numero)')
                        cantidad = await self.CargarVariable(conv,sender,int)
                        await conv.send_message(message='Porfavor indique la Moneda con la que pago(por ej USDT)')
                        moneda = await self.CargarVariable(conv,sender)
                        datos_a_cargar = {
                            'USER_ID':user_id,
                            'FECHA_ABONADO':datetime.today().isoformat(),
                            'PAGO_CANTIDAD':cantidad,
                            'PAGO_MONEDA':moneda,
                            'DIVIDIDO':'NO',
                            }

                        log_ventas_df=pd.read_excel(BotSettings.VENTAS_LOG_LOC)
                        log_ventas_df.append(datos_a_cargar,ignore_index=True)
                        log_ventas_df.to_excel(BotSettings.VENTAS_LOG_LOC,index=False)
                        await conv.send_message(message='Operacion realizada con exito, volviendo al menu principal...')
                        await self.ResetConv(conv,sender)
                        return
                except:
                    await conv.send_message(message=f'Operacion Realizada: {msg},Se produjo un error al extraer el codigo, id y/o vencimiento del status, revise manualmente subdb para encontrarlo.\nVolviendo al menu principal...')
                    await self.ResetConv(conv,sender)
                    return
        elif choice == 'RETURN':
            await self.ResetConv(conv,sender)
    
    async def CargarVariable(self,conv,sender,dtype:type=str)->str|type:
        cargando=True
        trys = 0
        while cargando:
            try:
                data = await conv.wait_event(events.NewMessage(sender))
                cargando = False
                return dtype(data.message.message)
            except:
                await conv.send_message(message=f'Input invalido, intente de nuevo\nintento {trys} de 3', parse_mode='html')
                trys = trys + 1
            if trys > 3:
                await conv.send_message(message=f'Salteando el input')
                return None

    async def CheckUsers(self,conv,sender):
        keyboard = [
                    [Button.inline(f"Limpiar usuarios vencidos/colados", 'CHECK_SUBS')],
                    [Button.inline(f"Volver", 'RETURN')],
                ]
        await conv.send_message(message='CheckSubs Menu',buttons=keyboard, parse_mode='html')
        press = await conv.wait_event(events.CallbackQuery(sender))
        choice = str(press.data.decode("utf-8"))

        if choice=='CHECK_SUBS':
            await conv.send_message(message='Checkeando subs...', parse_mode='html')
            kickeados, advertidos = await self.sub_checker.check_subs()
            await conv.send_message(message=f'Se kickearon {kickeados} usuarios y se advertieron {advertidos} para mas info vea logKick.',buttons=keyboard[1:], parse_mode='html')
            
            press = await conv.wait_event(events.CallbackQuery(sender))
            choice = str(press.data.decode("utf-8"))
            if choice == 'RETURN':
                await self.ResetConv(conv,sender)

        elif choice == 'RETURN':
            await self.ResetConv(conv,sender)
        
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