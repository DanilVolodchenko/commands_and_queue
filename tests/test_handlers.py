from queue import Queue
from unittest.mock import Mock

from interfaces import ICommand
from handlers import ExceptionHandler, LogHandler, RepeatHandler, RepeatOnceHandler, RepeatTwiceHandler

from commands import LogCommand, RepeatCommand, RepeatOnceCommand, RepeatTwiceCommand


class TestExceptionHandler:
    """Класс для тестирования объекта ExceptionHandler."""

    def test_register(self, mock_command: Mock) -> None:
        """Тестирование метода register."""

        mock_command = Mock()
        ExceptionHandler.register(type(mock_command), ValueError, LogHandler)
        ExceptionHandler.register(type(mock_command), ValueError, LogHandler)

        result = len(ExceptionHandler.state)
        expected_result = 1

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'

    def test_handler(self, mock_command: Mock, mock_exception_value_error: ValueError) -> None:
        """Тестирование метода handler."""

        ExceptionHandler.register(type(mock_command), type(mock_exception_value_error), LogHandler)

        result = type(ExceptionHandler.handler(type(mock_command), type(mock_exception_value_error)))
        expected_result = LogHandler

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'


class TestHandler:
    """Класс для тестирования обработчиков."""

    def test_log_handler(
            self, mock_command: Mock, mock_exception_value_error: ValueError, command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование обработчика LogHandler."""

        handler = LogHandler()
        handler.handle(mock_command, mock_exception_value_error, command_queue)

        result = type(command_queue.get())
        expected_result = LogCommand

        assert command_queue.not_empty, 'Очередь не должна быть пустой'
        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
        assert command_queue.empty(), 'Очередь должна быть пустой'

    def test_repeat_handler(
            self, mock_command: Mock, mock_exception_value_error: ValueError, command_queue: Queue[ICommand]
    ) -> None:
        """Тестирования обработчика RepeatHandler."""

        handler = RepeatHandler()
        handler.handle(mock_command, mock_exception_value_error, command_queue)

        result = type(command_queue.get())
        expected_result = RepeatCommand

        assert command_queue.not_empty, 'Очередь не должна быть пустой'
        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
        assert command_queue.empty(), 'Очередь должна быть пустой'

    def test_repeat_once_handler(
            self, mock_command: Mock, mock_exception_value_error: ValueError, command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование обработчика RepeatOnceHandler."""

        handler = RepeatOnceHandler()
        handler.handle(mock_command, mock_exception_value_error, command_queue)

        result = type(command_queue.get())
        expected_result = RepeatOnceCommand

        assert command_queue.not_empty, 'Очередь не должна быть пустой'
        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
        assert command_queue.empty(), 'Очередь должна быть пустой'

    def test_repeat_twice_handler(
            self, mock_command: Mock, mock_exception_value_error: ValueError, command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование обработчика RepeatTwiceHandler."""

        handler = RepeatTwiceHandler()
        handler.handle(mock_command, mock_exception_value_error, command_queue)

        result = type(command_queue.get())
        expected_result = RepeatTwiceCommand

        assert command_queue.not_empty, 'Очередь не должна быть пустой'
        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
        assert command_queue.empty(), 'Очередь должна быть пустой'
