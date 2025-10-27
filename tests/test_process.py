from queue import Queue
from unittest.mock import Mock, patch

from interfaces import ICommand
from main import process
from handlers import ExceptionHandler
from commands import LogCommand, RepeatCommand, RepeatOnceCommand, RepeatTwiceCommand
from handlers import LogHandler, RepeatHandler, RepeatOnceHandler, RepeatTwiceHandler


class TestProcess:
    """Тестирование функции process."""

    def test_with_mock(
            self,
            mock_command: Mock,
            mock_handler: Mock,
            mock_exception_value_error: ValueError,
            command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование только через mock объекты."""

        mock_command_extra = Mock(spec=ICommand)

        # Регистрируем мок объект как [Mock][ValueError] = Mock
        ExceptionHandler.register(type(mock_command_extra), type(mock_exception_value_error), type(mock_handler))

        mock_command_extra(mock_command, mock_exception_value_error)

        command_queue.put(mock_command_extra)

        process(command_queue)

        mock_command_extra.execute.assert_called_once(), 'Метод execute у объекта из очереди должен быть вызван один раз'
        mock_command.execute.assert_not_called(), 'Метод execute у переданного объекта не должна быть вызвана'

    def test_with_mock_with_exception(
            self,
            mock_command: Mock,
            mock_handler: Mock,
            mock_exception_value_error: ValueError,
            command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование функции process, если при вызове execute у команды из очереди произойдет исключение."""

        mock_command_extra = Mock(spec=ICommand)

        # Регистрируем мок объект как [Mock][ValueError] = Mock
        ExceptionHandler.register(type(mock_command_extra), type(mock_exception_value_error), type(mock_handler))

        mock_command_extra(mock_command, mock_exception_value_error)
        mock_command_extra.execute.side_effect = mock_exception_value_error

        command_queue.put(mock_command_extra)

        # Мокаем метод handler объекта ExceptionHandler, чтобы проверить, что метод handle будет вызван
        with patch.object(ExceptionHandler, 'handler') as mock_handler_method:
            mock_handler_method.return_value = mock_handler
            process(command_queue)

        call_count_mock_command_extra = mock_command_extra.execute.call_count
        expected_call_count_mock_command_extra = 1

        call_count_mock_command = mock_command.execute.call_count
        expected_call_count_mock_command = 0

        call_count_mock_handler = mock_handler.handle.call_count
        expected_call_count_mock_handler = 1

        assert call_count_mock_command_extra == expected_call_count_mock_command_extra, f'Ожидаемый результат: {expected_call_count_mock_command_extra}, полученный результат: {call_count_mock_command_extra}'
        assert call_count_mock_command == expected_call_count_mock_command, f'Ожидаемый результат: {expected_call_count_mock_command}, полученный результат: {call_count_mock_command}'
        assert call_count_mock_handler == expected_call_count_mock_handler, f'Ожидаемый результат: {expected_call_count_mock_handler}, полученный результат: {call_count_mock_handler}'

    def test_with_log_command(
            self, mock_command: Mock, mock_exception_value_error: ValueError, command_queue: Queue[ICommand]
    ) -> None:
        """Тестирование функции main, где в очереди команда LogCommand."""

        with patch('commands.logging') as mock_logging:
            ExceptionHandler.register(LogCommand, ValueError, LogHandler)
            command_queue.put(LogCommand(mock_command, mock_exception_value_error))

            process(command_queue)

            call_count_mock_logging = mock_logging.error.call_count
            expected_call_count_mock_logging = 1

            assert call_count_mock_logging == expected_call_count_mock_logging, f'Ожидаемый результат: {expected_call_count_mock_logging}, полученный результат: {call_count_mock_logging}'

    def test_command_called_count_2(
            self, mock_command: Mock, mock_handler, mock_exception_value_error: ValueError,
            command_queue: Queue[ICommand]
    ) -> None:
        """
        Тестирование функциональности, если будет зарегистрирована команда RepeatCommand,
        то команда из очереди должна быть вызвана 2 раза.
        """

        mock_command.execute.side_effect = mock_exception_value_error

        ExceptionHandler.register(RepeatCommand, ValueError, LogHandler)
        ExceptionHandler.register(type(mock_command), ValueError, RepeatHandler)

        command_queue.put(mock_command)

        while not command_queue.empty():
            process(command_queue)

        result = mock_command.execute.call_count
        expected_result = 2

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'

    def test_command_called_count_2_(
            self, mock_command: Mock, mock_handler, mock_exception_value_error: ValueError,
            command_queue: Queue[ICommand]
    ) -> None:
        """
        Тестирование функциональности, если будет зарегистрирована команда RepeatOnceCommand,
        то команда из очереди должна быть вызвана 2 раза.
        """

        mock_command.execute.side_effect = mock_exception_value_error

        ExceptionHandler.register(RepeatOnceCommand, ValueError, LogHandler)
        ExceptionHandler.register(type(mock_command), ValueError, RepeatOnceHandler)

        command_queue.put(mock_command)

        while not command_queue.empty():
            process(command_queue)

        result = mock_command.execute.call_count
        expected_result = 2

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'

    def test_command_called_count_3(
            self, mock_command: Mock, mock_handler, mock_exception_value_error: ValueError,
            command_queue: Queue[ICommand]
    ) -> None:
        """
        Тестирование функциональности, если будет зарегистрирована команда RepeatTwiceCommand,
        то команда из очереди должна быть вызвана 3 раза.
        """

        mock_command.execute.side_effect = mock_exception_value_error

        ExceptionHandler.register(RepeatOnceCommand, ValueError, LogHandler)
        ExceptionHandler.register(RepeatTwiceCommand, ValueError, RepeatOnceHandler)
        ExceptionHandler.register(type(mock_command), ValueError, RepeatTwiceHandler)

        command_queue.put(mock_command)

        while not command_queue.empty():
            process(command_queue)

        result = mock_command.execute.call_count
        expected_result = 3

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
