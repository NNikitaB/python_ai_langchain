import configparser
import logging
import json
import os
import telethon
import asyncio
from telethon.sync import TelegramClient
from telethon import connection,events,types,Button,custom,functions
from telethon.events.common import EventBuilder
from dotenv import load_dotenv
from openai_llm import MyChatOpenAI


logging.info('readding env')
# Считываем учетные данные
load_dotenv()


# Присваиваем значения внутренним переменным
api_id = os.getenv("API_TG_ID")
api_hash = os.getenv("API_TG_HASH")
username = os.getenv("USERNAME_TG")
token_bot = os.getenv("BOT_TG_TOKEN")

#
#api_token = os.getenv("OPENAI_TOKEN")
api_token = os.getenv("YDX_AI_TOKEN")
folder_id = os.getenv("YDX_FOLDER_ID")


#Пример для прокси
proxy = {
    'proxy_type': 'socks5', # (mandatory) protocol to use (see above)
    'addr': '1.1.1.1',      # (mandatory) proxy IP address
    'port': 5555,           # (mandatory) proxy port number
    'username': 'foo',      # (optional) username if the proxy requires auth
    'password': 'bar',      # (optional) password if the proxy requires auth
    'rdns': True            # (optional) whether to use remote or local resolve, default remote
}


class MyTelegramClient(TelegramClient):
    def __init__(self, session_name, api_id, api_hash):
        super().__init__(session_name, api_id, api_hash)
        self.llm = MyChatOpenAI(api_token=api_token,folder_id=folder_id)
        self.temperature = 0
        # Дополнительные инструкции и инициализация


class MyTelegramClient2(TelegramClient):
    ''' Decorator used to check allowed users '''
    def checked_on(self, event: EventBuilder, allowed_users: dict = {}):
        def decorator(func):
            async def wrapper(event):
                print( event.client.get_me().username)
                if  event.client.get_me().username in allowed_users:
                    print(  event.client.get_me().username)
                    func(event)

            async def callback(event):
                await wrapper(event)

            self.add_event_handler(callback, event)
            return decorator

        return decorator

logging.info('init client bot')
try:
    client = MyTelegramClient(username, api_id, api_hash).start(bot_token=token_bot)
except Exception as e:
    logging.critical("TelegramClient not started")
    logging.critical(str(e))
    exit()

keyboard =[
        #Button.text('Thanks!', resize=True, single_use=True),
        #Button.text('NO!', resize=True, single_use=True),
        Button.inline('Switch llm',data="switch_llm"),
        Button.inline('Switch regime',data="switch_temperature"),
]

# Определяем команды для установки
#commands = [types.BotCommand('start', 'Description of the new command')]
#client(functions.bots.SetBotCommandsRequest(
#        scope=types.BotCommandScopeDefault(),
#        lang_code='en',
#        commands=commands
#    ))

# Определяем команды 
help_commands={'regime': 'set temperature',
                'web': 'turn on/off links',
                'voice': 'turn on/off voice to text',
                'translate': 'turn on/off translator',
                'reset': 'reset context',
                'mode': 'switch LLM',
                'start': 'start',
                'ping': 'get status bot',
                'help': 'show all commands',
            }
str_help_comands = '\n'.join([ f'{k} - {v}' for k,v in help_commands.items()])


logging.info('loading json')

def read_json(path: str):
    with open(path, 'r') as file:
        dc = json.load(file)
        allowed_users = {user['tg_name']: user['name'] for user in dc['users']}
    return allowed_users


allowed_users = read_json('allowed_users.json')
if allowed_users is None:
    logging.warning('json is empty or not readed')





# Функция для обработки входящих сообщений
@client.on(events.NewMessage(pattern="^/start", from_users=allowed_users))
async def start(event):
    await event.reply('''Hello! I'm your personal AI\n Input /help to view commands''')
    

@client.on(events.NewMessage(pattern="^/ping"))
async def ping(event):
    m = await event.reply('Status: Running...')
    await asyncio.sleep(5)
    await client.delete_messages(event.chat_id, [event.id, m.id])


@client.on(events.NewMessage(pattern="^/help", from_users=allowed_users))
async def help(event):
    await event.reply(str_help_comands)


@client.on(events.NewMessage(pattern='^/mode', from_users=allowed_users))
async def mode(event):
    keyboard_markup = keyboard
    await event.respond("NO RELUASED")
    #await event.respond('Settings:',buttons=keyboard_markup)


@client.on(events.NewMessage(pattern='^/regime', from_users=allowed_users))
async def set_regime(event):
    if client.temperature < 0.1:
        client.temperature = 0.95
        client.llm.set_temperature(client.temperature)
    else:
        client.temperature = 0
        client.llm.set_temperature(client.temperature)
    await event.reply(f'regime temperature={client.temperature}')


@client.on(events.NewMessage(pattern='^/reset', from_users=allowed_users))
async def get_setting(event):
    llm.reset()
    client.llm.reset()
    await event.reply('llm reset!')


@client.on(events.NewMessage(pattern='^(?!/).*', from_users=allowed_users))
async def dialog(event):
    msg = event.raw_text
    #print(msg)
    m = client.llm.dialog(msg)
    #print(m)
    await event.reply(m.content)


@client.on(events.NewMessage(pattern='^/web', from_users=allowed_users))
async def get_setting(event):
    await event.reply('web!')
    await event.respond("NO RELUASED")


@client.on(events.NewMessage(pattern='^/voice', from_users=allowed_users))
async def get_setting(event):
    await event.reply('voice!')
    await event.respond("NO RELUASED")


#@client.on(events.CallbackQuery(pattern='^/voice', from_users=allowed_users))
#async def get_setting(event):
#    await event.reply('voice!')


logging.info('start bot')
with client:
    client.loop.run_forever()


