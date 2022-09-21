import os
#Requiere poner las variables de enviroment la primera vez q los corres si lo hosteas manual, si hosteas en nube mira el Dockerfile.

# 1) Crea un archivo llamado .env.bat con el vs code En la carpeta config
# 2) Abrelo con el VsCode y llenalo con esto (sin los #), pon las keys directo sin '' o "":

# set TELETHON_API_ID=Tu ID
# set TELETHON_API_HASH=Tu Hash
# set TELETHON_PHONE=Tu Phone
# set TELETHON_BOT_TOKEN=Tu Bot token para el invite bot
# set TELETHON_SUBMANAGER_BOT_TOKEN = bot token del submanager bot

# 3) Habre una consola de cmd y pon el siguiente comando , si no prueba dandole doble click al archivo supongo que servira tmb.

# call <la ubicacion del .env.bat>

#Ej suponiendo que estes en la carpeta donde se encuentra el Dockerfile el comando seria:

# call src\Configs\.env.bat

#Si lo hiciste por consola deberia imprimirte las variables 1 por 1 

# 4) Reinicia vs code y corre este script con la linea 33 descomentada para checkear.

#En caso de que tengas problemas con esto.
# 1) Reemplaza abajo con lo q corresponda y no toques nada mas.
# 2) En el peor de los casos borra todo y ponelas como siempre:
# api_id = 'Tu ID' .... etc.

api_id = str(os.environ.get('TELETHON_API_ID','Tu ID'))
api_hash = str(os.environ.get('TELETHON_API_HASH','Tu Hash'))
phone = str(os.environ.get('TELETHON_PHONE','Tu Phone'))
bot_token = str(os.environ.get('TELETHON_BOT_TOKEN','Tu token para el invite bot'))
bot_token_submanager = str(os.environ.get('TELETHON_SUBMANAGER_BOT_TOKEN',''))

cloudhost=os.environ.get('CLOUD_HOST')
#Esto esta para fijarte si se cargaron o no, comentalo si no quieres que se muestre al inciar el main.py o en este script
# print(f'ID: {api_id}\nHASH: {api_hash}\nPHONE: {phone}\nBOT_TOKEN_INVITEBOT: {bot_token}\nBOT_TOKEN_SUBMANAGER: {bot_token_submanager}\nCloud: {cloudhost}')

def get_api_keys()-> tuple:
    '''
    returns api_id, api_hash, phone, bot_token
    '''
    return api_id, api_hash, phone, bot_token, bot_token_submanager