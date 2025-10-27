import logging

from interfaces import ICommand


class LogCommand(ICommand):
    def __init__(self, cmd: ICommand, exc: Exception) -> None:
        self.cmd = cmd
        self.exc = exc

    def execute(self) -> None:
        logging.error(
            f'Произошла ошибка при выполнении команды {self.cmd} ({self.exc.__class__.__name__}): {self.exc}'
        )


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
