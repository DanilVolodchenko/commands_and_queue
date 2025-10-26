import abc
from queue import Queue


class ICommand(abc.ABC):

    @abc.abstractmethod
    def execute(self) -> None:
        """Выполняет какую-то команду."""

    def __str__(self) -> str:
        return f'Команда {self.__class__.__name__}'


class ICommandHandler(abc.ABC):

    def __init__(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        self.cmd = cmd
        self.exc = exc
        self.queue = queue

    @abc.abstractmethod
    def handle(self) -> None:
        """Метод для обработки."""
