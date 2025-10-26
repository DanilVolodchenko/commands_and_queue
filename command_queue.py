from typing import Optional
from queue import Queue

from interfaces import ICommand


class CommandQueueSingleton(Queue[ICommand]):
    __instance: Optional['CommandQueueSingleton'] = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
