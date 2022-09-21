import string
import random
import pandas as pd
client = None

def get_random_code(largo=10) -> str:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(largo))

async def get_chat_ids(data: pd.Series, _client, debug=False) -> pd.Series:
    '''
    Takes a column/series with the names of the chats and returns a series with the ids.
    '''
    out=None

    try:
        client=_client
        dialogs = await _client.get_dialogs()
        out = data.copy()
    except:
        print(f'{bcolors.WARNING}ERROR{bcolors.ENDC} <Utils/get_chat_ids>: No se pudo encontrar el cliente/data')
        raise

    for i,chat in enumerate(out):
        if debug:
            print(f'{bcolors.OKBLUE}DEBUG{bcolors.ENDC} <Utils/get_chat_ids>: Procesando {chat} {i+1}/{len(out)}')
        try:
            out[i] = await client.get_peer_id(chat)
            out[i] = int(out[i])
        except:
            print(f'{bcolors.WARNING}ERROR{bcolors.ENDC} <Utils/get_chat_ids>: No se pudo sacar la id de: {chat}')

    return out

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    ERROR_CRITICO = f'{FAIL}ERROR CRITICO{ENDC}'
    ERROR = f'{WARNING}ERROR{ENDC}'
    DEBUG_BLUE = f'{OKBLUE}DEBUG{ENDC}'
    DEBUG_CYAN = f'{OKCYAN}DEBUG{ENDC}'
    DEBUG_SUCCESS = f'{OKGREEN}SUCCESS{ENDC}'
    DEBUG_WARN = f'{WARNING}WARN{ENDC}'

