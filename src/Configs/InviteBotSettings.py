'''Configs de los textos y ciertos parametros del InviteBot'''
from Configs import BotSettings
from telethon.tl.custom import Button

INVITE_BOT_SESSION_NAME = "InviteBot"

#Pon los grupos en la prioridad que quieras que salgan (el que esta primero sale primero el segundo segundo ... etc)
#Tienen que estar todos los nombres de los grupos outputs aca
ORDEN_LINKS = ['Canal Test Output','me','Channel Test Output']

#--------------CONFIG TEXTOS-----------------
#Lo primero que sale al darle /start
INTRO_TXT = ''' <h1>placeholder titulo</h1>
                <p>placeholder texto</p> '''

INTRO_OPTION_TXT = ''''Seleciona idioma / Select language'''

#-----------------Titulos de menu----------------------------
MAIN_MENU_TITLE = {
                    'ES': '<h1>Bienvenido</h1>',
                    'EN': '<h1>Welcome</h1>'
}

ABOUT_TITLE = {
                'ES': '''Titulo/texto de introduccion del menu principal''',
                'EN': '''Main Menu Title/intro text'''
}

#--------------------TEXTOS-------------------------
SUB_TXT = {
            'ES': f'Comuniquese con @{BotSettings.ADMIN} para contratar una subscripcion',
            'EN': f'Speak to @{BotSettings.ADMIN} in order to purchase a subscription',
}

WHO_TXT = {
            'ES': '''Texto Info del boton quienes somos?''',

            'EN': '''Who are we? button Info text ''',
}

HOW_TXT = {
            'ES': '''Info del boton como''',

            'EN': '''How button info''',
}

REFER_TXT = {
            'ES': f'''Comuniquese con @{BotSettings.ADMIN} para conseguir descuentos de referal''',
            'EN': f'''Contact @{BotSettings.ADMIN} for referal discounts''',
}

RETURN_TXT = {
            'ES': 'Pulsa el boton para volver al menu principal',
            'EN': 'Press the button to return to the main menu',
}
#---------------------BOTONES---------------------------------
#  NO TOCAR LO QUE ESTA LUEGO DE LA COMA (trial,sub,code,status etc)
MENU_BUTTONS = {'ES':[
                        [Button.inline(f"🎁 Prueba gratuita 🎁", 'trial')], 
                        [Button.inline(f"Contratar plan⭐️", 'sub')],
                        [Button.inline(f"Canjear Codigo🔑🔓", 'code')],
                        [Button.inline(f"Saber mas❔", 'about')],
                        [Button.inline(f"Ver tu info del servicio📝", 'status')],
                    ],
                'EN':[
                        [Button.inline(f"🎁 Free trial 🎁", 'trial')], 
                        [Button.inline(f"Buy subscription⭐️", 'sub')],
                        [Button.inline(f"Get channel links🔑🔓", 'code')],
                        [Button.inline(f"About❔", 'about')],
                        [Button.inline(f"Check your status📝", 'status')],
                        ],
                }

ABOUT_BUTTONS = {'ES':[
                        [Button.inline(f"Quienes somos?", 'who')], 
                        [Button.inline(f"Como funciona?", 'how')],
                        [Button.inline(f"Sistema de referencia", 'refer')],
                        [Button.inline(f"Volver↩️", 'back')],
                    ],
                 'EN':[
                        [Button.inline(f"Who are we?", 'who')], 
                        [Button.inline(f"How it works?", 'how')],
                        [Button.inline(f"Refer system", 'refer')],
                        [Button.inline(f"Back↩️", 'back')],
                    ]
                }
RETURN_BUTTONS = {
                'ES': [Button.inline(f"Volver↩️", '')],
                'EN': [Button.inline(f"Return↩️", '')],
}
#-----------------------Mensajes de Reclamar codigo / usar prueba-----------------------------------------------
# NO QUITAR O AÑADIR ->>> {}
USED_TRIAL_MSG = {
                'ES':'Ya usaste la prueba gratuita, bla bla bla',
                'EN':"You already used your free trial, bla bla bla",
}

#primer {} es el codigo, segundo {} la fecha de vencimiento
VALID_TRIAL_ALT_MSG = {
                'ES':'Tu codigo es {} y la prueba vence el {}.\nLo puedes cangear en el menu principal',
                'EN':'Your code is: {} and the trial expires in: {} (Y-M-D)\nYou can exchange it at the main menu.',
}

INVALID_USER_EXTREME_ERROR_MSG = {
                'ES': f'Proceso Invalido porfavor comuniquese con @{BotSettings.ADMIN}',
                'EN': f'Invalid process please consult @{BotSettings.ADMIN}',
}

LINK_GENERATING_MSG = {
                'ES': 'Generando links, esto puede tardar un poco...',
                'EN': 'Generating links, this might take a bit...'
}

LINK_RETRIVAL_MSG = {
                'ES': f'\nRecuerda que duran 12 horas y tienen 1 uso si tienes problemas comunicate con @{BotSettings.ADMIN}',
                'EN': f'\nInvite links are one use and have a lifespan of 12hs\nIf you have any problems contact @{BotSettings.ADMIN}',
}

USER_NOT_IN_DB = {
                'ES': 'No estas en la base de datos',
                'EN': 'You are not in the data base',
}

INVALID_CODE_MSG = {
                'ES': 'Tu codigo Codigo es Invalido/Expirado',
                'EN': 'Your code is Invalid/Expired',
}

VALID_CODE_RETRIVAL_ERROR_MSG = {
                'ES': f'Tu codigo era valido pero hubo un problema generando los links. Comuniquese con @{BotSettings.ADMIN}',
                'EN': f'Your code was valid but there was a problem generating the links. Contact @{BotSettings.ADMIN}'
}

INSERT_CODE_MSG = {
    'ES':'Por favor Envia tu codigo',
    'EN':'Please send your code',
}

#---------Otros mensajes-------------
# NO QUITAR O AÑADIR ->>> {}

# status, plan , vencimiento
USER_STATUS_MSG = { 
                'ES':'Tu status es: {}, tu plan es: {}, vence el: {}',
                'EN':'Your status is: {}, your subscription plan is: {}, expires in: {}'}
#----------------Links--------------------------
# NO QUITAR O AÑADIR ->>> {}
# Las primeras {} son el nombre del canal Las segundas el link 
LINKS_MSG = {
                'ES':'<b>- {} 👉🏻</b> <i><a href="{}"> Unirme al canal </a></i>',
                'EN':'<b>- {} 👉🏻</b> <i><a href="{}"> Join channel </a></i>',
}