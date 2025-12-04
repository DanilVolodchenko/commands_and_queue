from queue import Queue

from interfaces import ICommand
from handlers import ExceptionHandler, LogHandler


def process(commands_queue: Queue[ICommand]) -> None:
    """Логика работы с командами из очереди."""

    cmd = commands_queue.get()
    try:
        cmd.execute()
    except Exception as exc:
        ExceptionHandler.handler(type(cmd), type(exc), default_handler=LogHandler).handle(cmd, exc, commands_queue)
