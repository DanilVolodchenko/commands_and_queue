from typing import Type, TypeAlias
from collections import defaultdict

import commands
from interfaces import ICommand, ICommandHandler
from command_queue import CommandQueueSingleton
import handlers

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
    def handler(cls, cmd: ICommand, exc: Exception) -> ICommandHandler:
        command_queue = CommandQueueSingleton()
        cmd_type: Type[ICommand] = type(cmd)
        exc_type: Type[Exception] = type(exc)
        try:
            return cls.state[cmd_type][exc_type](cmd, exc, command_queue)
        except KeyError:
            return handlers.DefaultCommandHandler(cmd, exc, command_queue)

    @classmethod
    def register(cls, cmd: Type[ICommand], exc: Type[Exception], handler: Type[ICommandHandler]) -> None:
        cls.state[cmd][exc] = handler


class MoveCommand(ICommand):
    def execute(self) -> None:
        print('Выполнение команды MoveCommand')
        raise ValueError('Move error')


def main() -> None:
    commands_queue = CommandQueueSingleton()

    ExceptionHandler.register(MoveCommand, ValueError, handler=handlers.RepeatTwiceHandler)
    ExceptionHandler.register(commands.RepeatTwiceCommand, ValueError, handler=handlers.RepeatOnceHandler)
    # ExceptionHandler.register(commands.RepeatOnceCommand, ValueError, handler=handlers.LogCommandHandler)
    # ExceptionHandler.register(commands.RepeatOnceCommand, ValueError, handler=handlers.LogCommandHandler)
    commands_queue.put(MoveCommand())

    while True:
        cmd = commands_queue.get()
        try:
            cmd.execute()
        except Exception as exc:
            handler = ExceptionHandler.handler(cmd, exc)
            if handler:
                handler.handle()
            else:
                print(f'Обработчик для {cmd} не найден')


if __name__ == '__main__':
    main()
