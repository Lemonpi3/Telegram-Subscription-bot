'''Configs de la app'''
import os

SESSION_NAME = "MainSession"
SUBMANAGER_BOT_SESSION_NAME ='SubManagerBot'

#a quien se le van a dirigir los mensajes pribados
ADMIN = 'admin'

#Para canales publicos tomara los de esta categoria.
PUBLIC_CATEGORY ="PUBLIC"

#El texto que se pega al mensaje q enviar en los chats publicos/promocionales. 1/9/2022 aparece arriba de la señal.
PUBLIC_MSG = '''PH'''  

#Categoria por defecto q se le dara a los usuarios de prueba/no especificados. 
#(Esta categoria se la pones chats en chatdb a los cuales quieras enviar a los prueba)
DEFAULT_CATEGORY = "DEMO" 
#dias de prueba
TRIAL_DAYS = 3
#config de tiers subdb, si quieres mas avisa
USER_TIER_ADMIN = -2
USER_TIER_PERMASUB = -1
USER_TIER_PRUEBA = 0  # este es el tier que esta por defecto
USER_TIER_PREMIUM_1 = 1
USER_TIER_PREMIUM_2 = 2
USER_TIER_PREMIUM_3 = 3 

#Nombre de los tiers usan los valores numericos como indice en español, no toques los numeros, si agregas un tier arriba tienes q agregarlo aca por ej
#USER_TIER_PREMIUM_4 seria:
#                               4 : 'User tier premium 4',
#Esto se usa para DatabaseManager/Submanager/get_user_info (aprox linea 230 del DatabaseManager) para imprimirle al usuario el plan que tiene.
#Tambien sirve como guia para entender la columna user_tier del subdb.xlsx
TIER_DICT_ES = {
    -2 : 'Admin',
    -1 : 'Perma sub',
     0 : 'Prueba',
     1 : 'Premium 1',
     2 : 'Premium 2',
     3 : 'Premium 3',
}
#lo mismo que el de arriba pero en ingles
TIER_DICT_EN = {
    -2 : 'Admin',
    -1 : 'Lifetime sub',
     0 : 'Trial',
     1 : 'Premium 1',
     2 : 'Premium 2',
     3 : 'Premium 3',
}

#Si esta en falso la purga es manual (6/9/22 : esta config no se usa)
AUTO_PURGE = False

#Dias para advertir q se le vence -> ej si esta = 2 le avisara 2 dias antes q se le vence
WARN_DAYS = 2

#El mensaje de advertencia en español
WARN_MSG_ES = '''Pega tu advertencia aqui''' 

#El mensaje de advertencia en ingles
WARN_MSG_EN = '''Pega tu advertencia aqui, en ingles''' 

#Debug toggles
DEBUG_CHATSDB = True
DEBUG_CLIENTDB = True
DEBUG_INVITE_BOT = True

#Si quieres que generen excels vacios por fallas de carga al iniciar(ya sea pq no hay uno o esta corrupto)(6/9/22 : esta config va a ser removida en un futuro.)
GENERATE_EXCEL_CHATSDB = False
GENERATE_EXCEL_CLIENTDB = False

#No tocar nada apartir de aca
#-----------------------------------------------------------------------------------------#
def get_tier_names(idioma:str,tier):
    '''retorna el nombre tier bazado en idioma'''
    if idioma.upper() == 'ES':
        try:
            return TIER_DICT_ES[int(tier)]
        except:
            return 'No se encontro el tier de usuario'
    if idioma.upper() == 'EN':
        try:
            return TIER_DICT_EN[int(tier)]
        except:
            return 'User tier not found'

#Ubicaciones de los excels
if os.environ.get('CLOUD_HOST'):
    print(os.environ.get('CLOUD_HOST'))
    CHATSDB_LOC = './Data/chatsdb.xlsx'
    SUBSDB_LOC = './Data/subsdb.xlsx'
    KICKS_LOGS_LOC = './Data/logKick.xlsx'
    VENTAS_LOG_LOC = './Data/logVentas.xlsx'
else:
    CHATSDB_LOC = '.\src\Data\chatsdb.xlsx'
    SUBSDB_LOC = '.\src\Data\subsdb.xlsx'
    KICKS_LOGS_LOC = '.\src\Data\logKick.xlsx'
    VENTAS_LOG_LOC = '.\src\Data\logVentas.xlsx'