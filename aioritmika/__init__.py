'''Штука для ботов в алге'''
from typing import Literal
from warnings import warn
import asyncio
import aiohttp
import json

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
    def __init__(self, login: str, password: str, prefix: str = "", timeout: float = 5, storage: str|None = 'aioritmika_data.json'):
        '''
        Создать бота

        Аргументы:
        login - Логин для входа в алгу/имя бота
        password - Пароль для входа в алгу
        prefix - Префикс команд
        timeout - Задержка между проверками комментариев
        storage - Путь к файлу, куда будет сохраняться/загружаться информация об обработанных комментариях (чтобы один комментарий не обпабатывать дважды). Если None, хранит информацию в переменной (сбрасываеться при перезагрузке скрипта)
        '''
        if type(login) != str:
            raise TypeError('login is not `str`')
        if type(password) != str:
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
        self.running = False

    def command(self, name: str|None = None):
        '''
        Декоратор для добавления команды в бота

        Аргументы:
        name - Имя команды, если None - имя функции
        '''
        def decor(coro):
            self.commands[self.prefix + (name if name is not None else coro.__name__)] = coro
            return coro
        return decor
