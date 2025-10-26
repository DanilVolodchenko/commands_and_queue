from typing import Type, TypeAlias
from collections import defaultdict
from queue import Queue

import commands
from interfaces import ICommand, ICommandHandler

State: TypeAlias = dict[
    Type[ICommand],
    dict[
        Type[Exception],
        Type[ICommandHandler]
    ]
]


class ExceptionHandler:
    state: State = defaultdict(dict)

    @classmethod
    def handler(cls, cmd: Type[ICommand], exc: Type[Exception]) -> ICommandHandler | None:
        try:
            return cls.state[cmd][exc]()
        except KeyError:
            return None

    @classmethod
    def register(cls, cmd: Type[ICommand], exc: Type[Exception], handler: Type[ICommandHandler]) -> None:
        cls.state[cmd][exc] = handler


class LogCommandHandler(ICommandHandler):

    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(commands.LogCommand(cmd, exc))


class RepeatCommandHandler(ICommandHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(commands.RepeatCommand(cmd))


class RepeatOnceHandler(ICommandHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(commands.RepeatOnceCommand(cmd))


class RepeatTwiceHandler(ICommandHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(commands.RepeatTwiceCommand(cmd))
