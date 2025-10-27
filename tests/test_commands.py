from unittest.mock import Mock, patch

import pytest

from commands import LogCommand, RepeatCommand, RepeatOnceCommand, RepeatTwiceCommand


class TestCommand:
    """Класс для тестирования команд."""

    def test_log_command(self, mock_command: Mock, mock_exception_value_error: ValueError) -> None:
        """Тестирование команды LogCommand."""

        with patch('commands.logging') as mock_logging:
            command = LogCommand(mock_command, mock_exception_value_error)

            command.execute()

            assert mock_logging.error.called, 'Метод logging.error должен быть вызван'
            mock_logging.error.assert_called_once(), 'Метод logging.error должен быть вызван один раз'

    def test_log_command_with_exception(self, mock_command: Mock, mock_exception_value_error: ValueError) -> None:
        """Тестирование команды RepeatCommand."""

        mock_command.execute.side_effect = mock_exception_value_error
        command = RepeatCommand(mock_command)

        expected_exc = ValueError

        with pytest.raises(expected_exc):
            command.execute(), f'Должно выбросится исключение {expected_exc}'

    def test_repeat_command(self, mock_command: Mock) -> None:
        """Тестирование команды RepeatCommand."""

        command = RepeatCommand(mock_command)

        command.execute()

        assert mock_command.execute.called, 'Метод execute должен быть вызван'
        mock_command.execute.assert_called_once(), 'Метод execute должен быть вызван один раз'

    def test_repeat_command_with_exception(self, mock_command: Mock, mock_exception_value_error: ValueError) -> None:
        """Тестирование команды RepeatCommand с выбросом исключения."""

        mock_command.execute.side_effect = mock_exception_value_error
        command = RepeatCommand(mock_command)

        expected_exc = ValueError

        with pytest.raises(expected_exc):
            command.execute(), f'Должно выбросится исключение {expected_exc}'

    def test_repeat_once_command(self, mock_command: Mock) -> None:
        """Тестирование команды RepeatOnceCommand."""

        command = RepeatOnceCommand(mock_command)

        command.execute()

        assert mock_command.execute.called, 'Метод execute должен быть вызван'
        mock_command.execute.assert_called_once(), 'Метод execute должен быть вызван один раз'

    def test_repeat_once_command_with_exception(
            self, mock_command: Mock, mock_exception_value_error: ValueError
    ) -> None:
        """Тестирование команды RepeatOnceCommand с выбросом исключения."""

        mock_command.execute.side_effect = mock_exception_value_error
        command = RepeatOnceCommand(mock_command)

        expected_exc = ValueError

        with pytest.raises(expected_exc):
            command.execute(), f'Должно выбросится исключение {expected_exc}'

    def test_repeat_twice_command(self, mock_command: Mock) -> None:
        """Тестирование команды RepeatOnceCommand."""

        command = RepeatTwiceCommand(mock_command)

        command.execute()

        assert mock_command.execute.called, 'Метод execute должен быть вызван'
        mock_command.execute.assert_called_once(), 'Метод execute должен быть вызван один раз'

    def test_repeat_twice_command_with_exception(
            self, mock_command: Mock, mock_exception_value_error: ValueError
    ) -> None:
        """Тестирование команды RepeatOnceCommand с выбросом исключения."""

        mock_command.execute.side_effect = mock_exception_value_error
        command = RepeatTwiceCommand(mock_command)

        expected_exc = ValueError

        with pytest.raises(expected_exc):
            command.execute(), f'Должно выбросится исключение {expected_exc}'