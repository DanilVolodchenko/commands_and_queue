from unittest import mock

from handlers import ExceptionHandler, LogCommandHandler


class TestExceptionHandler:
    def test_register(self) -> None:
        """Тестирование метода register."""

        mock_command = mock.Mock()
        ExceptionHandler.register(type(mock_command), ValueError, LogCommandHandler)
        ExceptionHandler.register(type(mock_command), ValueError, LogCommandHandler)

        len_state = len(ExceptionHandler.state)

        expected_result = 1

        assert len_state == 1, f'Ожидаемый результат: {expected_result}, полученный результат: {len_state}'

    def test_handler(self) -> None:
        mock_command = mock.Mock(side_effect=ValueError('Mock object raises exception'))
        ExceptionHandler.register(type(mock_command), ValueError, LogCommandHandler)

        result = type(ExceptionHandler.handler(type(mock_command), ValueError))

        expected_result = LogCommandHandler

        assert result == expected_result, f'Ожидаемый результат: {expected_result}, полученный результат: {result}'
