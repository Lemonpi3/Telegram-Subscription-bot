import pandas as pd
from Configs import BotSettings
from Scripts.Utils import get_chat_ids, bcolors, get_random_code
from datetime import date,datetime,timedelta

'''
Se encarga de inicializar y controlar el estado de todas las bases de datos.
'''
class ChatsDB:
    '''
    A cargo de controlar el chatsdb.xlsx.
    Solo corre al inicio para verificar que tengan las ids generadas, de no ser asi las genera.
    Si ocurre un error al cargar chatsdb.xlsx y self.create_db = True creara el archivo de nuevo, 
    luego sin importar de self.create_db cerrara el programa.
    '''
    def __init__(self, client,debug , create_db=False):
        self.client = client
        self.debug = debug
        self.create_db = create_db

    async def Init_ChatDB(self):
        '''
        Checkea si existe la base de datos y si todos los inputs y outputs tienen ids
        '''
        dialogs = await self.client.get_dialogs()
        error=False

        try:
            print(f'----{bcolors.OKBLUE}<DataBaseManager/ChatsDB>{bcolors.ENDC} Inicializando ----')
            db=pd.read_excel(BotSettings.CHATSDB_LOC)
        except:
            print(f'{bcolors.WARNING}ERROR{bcolors.ENDC} <DataBaseManager/ChatsDB> No se encontro una base de datos')

            if self.create_db:
                print(f'-- <DataBaseManager/ChatsDB> Generando chatsdb.xlsx en {BotSettings.CHATSDB_LOC}')
                temp = {'Chat input':[], 'Chat output':[], 'ID input':[], 'ID output':[], 'Idioma':[], 'Categoria':[], 'User Tier':[]}
                df = pd.DataFrame(temp)
                df.dropna(inplace=True)
                df.to_excel(BotSettings.CHATSDB_LOC,index=False)

            error = True
            raise
        print(db.head())
        if not len(db):
            print(f'{bcolors.WARNING}ERROR{bcolors.ENDC} <DataBaseManager/ChatsDB> {BotSettings.CHATSDB_LOC} esta vacio')
            error = True

        nulos = db['ID input'].isna().sum() + db['ID output'].isna().sum()

        if nulos > 0:
            print(f'--{bcolors.OKBLUE}<DataBaseManager/ChatsDB>{bcolors.ENDC} Generando IDs --')

            if self.debug:
                print(f'{bcolors.OKCYAN}DEBUG{bcolors.ENDC} {bcolors.OKBLUE}<DataBaseManager/ChatsDB>{bcolors.ENDC} Generando IDs Input')
            db['ID input']= await get_chat_ids(db['Chat input'],self.client,self.debug)

            if self.debug:
                print(f'{bcolors.OKCYAN}DEBUG{bcolors.ENDC} {bcolors.OKBLUE}<DataBaseManager/ChatsDB>{bcolors.ENDC} Generando IDs Output')
            db['ID output']= await get_chat_ids(db['Chat output'],self.client,self.debug)

        if error:
            print(f'{bcolors.FAIL}ERROR CRITICO {bcolors.ENDC}en <DataBaseManager/ChatsDB> Saliendo....')
            quit()

        db.to_excel(BotSettings.CHATSDB_LOC,index=False)

        print(f'----{bcolors.OKGREEN}<DataBaseManager/ChatsDB> Iniciado {bcolors.ENDC}----')

class ClientDB:
    '''Se encarga de iniciar subsdb'''
    def __init__(self, client,debug , create_db=False):
        self.client = client
        self.debug = debug
        self.create_db = create_db
        self.db=None

    def Init_ClientDB(self):
        error = False

        try:
            print(f'----{bcolors.OKBLUE}<DataBaseManager/ClientDB>{bcolors.ENDC} Inicializando ----')
            self.db=pd.read_excel(BotSettings.SUBSDB_LOC)
        except:
            print(f'{bcolors.WARNING}ERROR{bcolors.ENDC} <DataBaseManager/ClientDB> No se encontro una base de datos')

            if self.create_db:
                print(f'-- <DataBaseManager/ClientDB> Generando subsdb.xlsx en {BotSettings.SUBSDB_LOC}')
                temp = {'ID':[], 'User':[], 'User Tier':[], 'Categorias':[], 'Idioma':[],
                         'Fecha Abonado':[], 'Vencimiento':[], 'Status del Servicio':[], 'Codigo':[],'Uso Prueba':[]}
                df = pd.DataFrame(temp)
                df.dropna(inplace=True)
                df.to_excel(BotSettings.SUBSDB_LOC,index=False)

            error = True
            raise

        if error:
            print(f'{bcolors.FAIL}ERROR CRITICO {bcolors.ENDC}en <DataBaseManager/ClientDB> Saliendo....')
            quit()

        print(f'----{bcolors.OKGREEN}<DataBaseManager/ClientDB> Iniciado {bcolors.ENDC} ----')
