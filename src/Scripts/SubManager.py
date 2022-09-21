from enum import Flag
import pandas as pd
from Configs import BotSettings
from Scripts.Utils import bcolors, get_random_code
from datetime import date,datetime,timedelta

class SubManager:
    '''
    * Agrega usuarios nuevos.
    * Edita valores de usuarios
    '''
    def __init__(self,debug:bool=False):
        self.debug=debug

    def update_cols_value(user_id:int,cols:list[str],values:list):
        '''
        #### Updatea el valor de X columnas para un usuario.
        requiere que los parametros esten en lista y ordenados.
        '''
        db = get_subdb()
        for i,col in enumerate(cols):
            db.loc[db.ID == user_id,col]=values[i]
            db.to_excel(BotSettings.SUBSDB_LOC,index=False)

    def add_new_user(self,user_id:int,lenguaje:str,user_tier:int=0,categories:list[str]=['DEMO'],days_to_add=0,prueba=False,name:str=None,remplazar_categorias:bool=False)->tuple[dict,str|None,str]:
        '''Agrega un nuevo usuario al subdb, Retorna un diccionario con lo cargado o None    y el status
        
        Retorna:
        * data del usuario , NEW_USER o UPDATED
        
        * None, USED_TRIAL'''
        db = get_subdb()
        print(db)

        if len(db[db.ID==user_id]):
            print(f'{bcolors.DEBUG_CYAN} <SubManager> Se encontro el usuario en la base de datos intentado Updatear con lo cargado...')
            func_status,msg = self.update_user_status(user_id,lenguaje,user_tier,categories,days_to_add,prueba,remplazar_categorias)
            return func_status,msg

        if prueba:
            uso_prueba='SI'
        else:
            uso_prueba='NO'

        func_status = {
                'ID':int(user_id),
                'User':name, 
                'User Tier':user_tier,
                'Idioma':lenguaje, 
                'Categorias': '-'.join(categories),
                'Fecha Abonado': datetime.today().strftime('%Y-%m-%d'), 
                'Vencimiento':(datetime.today() + timedelta(days=int(days_to_add))).strftime('%Y-%m-%d'),
                'Status del Servicio':'Activo'.upper(),
                'Codigo':get_random_code(),
                'Uso Prueba':uso_prueba,
                }

        db = db.append(func_status,ignore_index=True)
        db.to_excel(BotSettings.SUBSDB_LOC,index=False)

        return func_status,'NEW_USER'

    def update_user_status(
                            self,user_id:int, lenguaje:str, user_tier:int=0, categories:list[str]=['DEMO'], 
                            days_to_add=0, prueba=True, remplazar_categorias=False
                        )->tuple[dict,str|None,str]:
        '''Actualiza el status del usuario y agrega dias.'''
        db = get_subdb()
        cond = db.ID==user_id

        if prueba and db[cond]['Uso Prueba']=='SI':
            return None,'USED_TRIAL'
        
        categorias = str(db[cond]['Categorias'].item()).split('-')

        if prueba:
            uso_prueba='SI'
        else:
            uso_prueba='NO'

        if not remplazar_categorias:
            for cat in categories:
                if cat not in categorias :
                    categorias.append(cat)
        else:
            categorias = categories

        new_data={
            'User Tier':user_tier,
            'Idioma':lenguaje, 
            'Categorias': '-'.join(categorias),
            'Fecha Abonado': datetime.today().strftime('%Y-%m-%d'), 
            'Vencimiento':(datetime.today() + timedelta(days=int(days_to_add))).strftime('%Y-%m-%d'),
            'Status del Servicio':'Activo'.upper(),
            'Codigo':get_random_code(),
            'Uso Prueba':uso_prueba,
            }     

        for col in new_data:
            db.loc[cond,col] = new_data[col]

        db.to_excel(BotSettings.SUBSDB_LOC,index=False)
        new_data['ID'] = user_id

        return new_data, 'UPDATED'

    def get_user_info(self,user_id):
        try:
            db = get_subdb()
            return db[db.ID == user_id].iloc[0].to_dict()
        except:
            return None

def get_subdb()->pd.DataFrame:
        try: 
            db=pd.read_excel(BotSettings.SUBSDB_LOC)
            if not len(db):
                print(f'{bcolors.ERROR} No se encontraron usuarios en subdb.')
                return db
            return db
        except:
            print(f'{bcolors.ERROR_CRITICO} No se encontro subdb.')
            return None