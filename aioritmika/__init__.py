'''Штука для ботов в алге'''
from typing import Literal
from warnings import warn
import asyncio
import aiohttp

class Bot:
    '''
    Ну да
    
    Аргументы init:
    login - Логин для входа в алгу/имя бота
    password - Пароль для входа в алгу
    prefix - Префикс команд
    timeout - Задержка между проверками комментариев
    '''
    def __init__(self, login: str, password: str, prefix: str = "", timeout: float = 5):
        '''
        Создать бота

        Аргументы:
        login - Логин для входа в алгу/имя бота
        password - Пароль для входа в алгу
        prefix - Префикс команд
        timeout - Задержка между проверками комментариев
        '''
        if type(login) != str:
            raise TypeError('login is not `str`')
        if type(password) != str:
            raise TypeError('password is not `str`')
        self.login = login
        self.password = password
        self.timeout = timeout
        self.prefix = prefix
        self.commands = {}
        self.running = False

    def command(self, name: str|None = None):
        def decor(coro):
            self.commands[self.prefix + (name if name is not None else coro.__name__)] = coro
            return coro
        return decor