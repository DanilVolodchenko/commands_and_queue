import abc
from queue import Queue


class ICommand(abc.ABC):

    @abc.abstractmethod
    def execute(self) -> None:
        """Выполняет какую-то команду."""

    def __str__(self) -> str:
        return self.__class__.__name__


class IHandler(abc.ABC):

    @abc.abstractmethod
    def handle(self, cmd: ICommand, exc: Exception, queue: Queue[ICommand]) -> None:
        """Метод для обработки."""

    def __str__(self) -> str:
        return self.__class__.__name__
