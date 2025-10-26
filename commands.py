import logging
from queue import Queue

from interfaces import ICommand


class WriteLogCommand(ICommand):
    def __init__(self, cmd: ICommand, exc: Exception) -> None:
        self.cmd = cmd
        self.exc = exc

    def execute(self) -> None:
        with open('error_logs.log', 'a') as log_file:
            log_file.write(f'Ошибку `{self.cmd.__class__.__name__}` вызвала команда `{self.cmd}`')


class LogCommand(ICommand):
    def __init__(self, cmd: ICommand, exc: Exception) -> None:
        self.cmd = cmd
        self.exc = exc

    def execute(self) -> None:
        logging.error(
            f'Произошла ошибка при выполнении команды {self.cmd} ({self.exc.__class__.__name__}): {self.exc}'
        )


class PutCmdInQueueCommand(ICommand):
    def __init__(self, cmd: ICommand, queue: Queue[ICommand]) -> None:
        self.cmd = cmd
        self.queue = queue

    def execute(self) -> None:
        self.queue.put(self.cmd)


class RepeatCommand(ICommand):
    def __init__(self, cmd: ICommand) -> None:
        self.cmd = cmd

    def execute(self) -> None:
        self.cmd.execute()


class RepeatOnceCommand(ICommand):

    def __init__(self, cmd: ICommand) -> None:
        self.cmd = cmd

    def execute(self) -> None:
        self.cmd.execute()


class RepeatTwiceCommand(ICommand):
    def __init__(self, cmd: ICommand) -> None:
        self.cmd = cmd

    def execute(self) -> None:
        self.cmd.execute()
