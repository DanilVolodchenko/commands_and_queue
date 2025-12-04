from typing import Type, TypeAlias
from collections import defaultdict
from queue import Queue

from interfaces import ICommand, IHandler
from commands import LogCommand, RepeatCommand, RepeatOnceCommand, RepeatTwiceCommand

State: TypeAlias = dict[
    Type[ICommand],
    dict[
        Type[Exception],
        Type[IHandler]
    ]
]


class ExceptionHandler:
    state: State = defaultdict(dict)

    @classmethod
    def handler(
            cls, cmd: Type[ICommand], exc: Type[Exception], *, default_handler: Type[IHandler] = 'LogHandler'
    ) -> IHandler | None:
        """Возвращает обработчика в зависимости от типа команды и исключения."""

        try:
            return cls.state[cmd][exc]()
        except KeyError:
            return default_handler()

    @classmethod
    def register(cls, cmd: Type[ICommand], exc: Type[Exception], handler: Type[IHandler]) -> None:
        cls.state[cmd][exc] = handler


class LogHandler(IHandler):

    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(LogCommand(cmd, exc))


class RepeatHandler(IHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(RepeatCommand(cmd))


class RepeatOnceHandler(IHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(RepeatOnceCommand(cmd))


class RepeatTwiceHandler(IHandler):
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        queue.put(RepeatTwiceCommand(cmd))
