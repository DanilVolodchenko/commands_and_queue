from queue import Queue

from interfaces import ICommand
from handlers import ExceptionHandler, LogCommandHandler, RepeatOnceHandler


class MoveCommand(ICommand):
    def __init__(self):
        self.attempt = 0

    def execute(self) -> None:
        print(f'Выполнение команды MoveCommand {self.attempt}')
        self.attempt += 1
        raise ValueError('Move error')


def main() -> None:
    commands_queue = Queue[ICommand]()
    while True:
        cmd = commands_queue.get()
        try:
            cmd.execute()
        except Exception as exc:
            handler = ExceptionHandler.handler(type(cmd), type(exc))
            if handler:
                handler.handle(cmd, exc, commands_queue)
            else:
                # Если обработчик не найден, то записывает ошибку в лог
                LogCommandHandler().handle(cmd, exc, commands_queue)


if __name__ == '__main__':
    main()
