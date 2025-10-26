import commands
from interfaces import ICommandHandler


class DefaultCommandHandler(ICommandHandler):
    def handle(self) -> None:
        self.queue.put(commands.WriteLogCommand(self.cmd, self.exc))


class LogCommandHandler(ICommandHandler):
    def handle(self) -> None:
        self.queue.put(commands.LogCommand(self.cmd, self.exc))


class RepeatCommandHandler(ICommandHandler):
    def handle(self) -> None:
        self.queue.put(commands.RepeatCommand(self.cmd))


class RepeatOnceHandler(ICommandHandler):
    def handle(self) -> None:
        self.queue.put(commands.RepeatOnceCommand(self.cmd))


class RepeatTwiceHandler(ICommandHandler):
    def handle(self) -> None:
        self.queue.put(commands.RepeatTwiceCommand(self.cmd))
