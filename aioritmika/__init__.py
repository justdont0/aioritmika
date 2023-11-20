'''Штука для ботов в алге'''
from warnings import warn
import asyncio
import aiohttp
import json
from .errors import *
from discord.ext import tasks


class Bot:
    '''
    Ну да

    Аргументы init:
    login - Логин для входа в алгу/имя бота
    password - Пароль для входа в алгу
    prefix - Префикс команд
    timeout - Задержка между проверками комментариев
    storage - Путь к файлу, куда будет сохраняться/загружаться информация об обработанных комментариях (чтобы один комментарий не обпабатывать дважды). Если None, хранит информацию в переменной (сбрасываеться при перезагрузке скрипта)
    '''
    def __init__(self, login: str, password: str, prefix: str = "", timeout: float = 5, storage: str | None = 'aioritmika_data.json'):
        '''
        Создать бота

        Аргументы:
        login - Логин для входа в алгу/имя бота
        password - Пароль для входа в алгу
        prefix - Префикс команд
        timeout - Задержка между проверками комментариев
        storage - Путь к файлу, куда будет сохраняться/загружаться информация об обработанных комментариях (чтобы один комментарий не обпабатывать дважды). Если None, хранит информацию в переменной (сбрасываеться при перезагрузке скрипта)
        '''
        if login is not str:
            raise TypeError('login is not `str`')
        if password is not str:
            raise TypeError('password is not `str`')
        self.login = login
        self.password = password
        self.timeout = timeout
        self.prefix = prefix
        self.storage = storage
        if storage is None: self.temp_storage = {}
        else:
            try: self.temp_storage = json.load(open(storage, 'r'))
            except: self.temp_storage = {}
        self.commands = {}
        self.events = {}
        self.running = False

    def command(self, name: str | None = None):
        '''
        Декоратор для добавления команды в бота (вызывайте со скобками, типа @bot.command())

        Аргументы:
        name - Имя команды, если None - имя функции
        '''
        def decor(coro):
            self.commands[self.prefix + (name if name is not None else coro.__name__)] = coro
            return coro
        return decor

    def event(self, coro):
        '''
        Декоратор для обработки события вручную
        (P.S.: при обработке on_message, обязательно используйте process_commands на сообщении)

        Аргументы:
        Их нет. Не используйте скобки, вызывая этот декоратор (@bot.event)
        '''
        if coro.__name__ not in ['on_message', 'on_ready']:
            warn('В библиотеке нет этого события, поэтому оно не будет вызываться.', NonExistingEvent)
            return coro
        self.events[coro.__name__] = coro
        return coro

    def run(self, project_id: int):
        '''
        Запустить бота

        Аргументы:
        project_id - айди проекта, под которым будет работать бот
        '''
        @tasks.loop(seconds=self.timeout)
        async def dat_loop():
            async with asyncio.Session() as s:
                s.post('')
