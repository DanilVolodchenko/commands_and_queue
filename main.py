from queue import Queue

from interfaces import ICommand
from process import process


class MoveCommand(ICommand):
    def execute(self) -> None:
        print('Выполнение MoveCommand')
        raise ValueError('Test')


def main() -> None:
    commands_queue = Queue[ICommand]()

    while True:
        process(commands_queue)


if __name__ == '__main__':
    main()
