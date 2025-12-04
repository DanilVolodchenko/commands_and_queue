from queue import Queue
from unittest.mock import Mock

import pytest

from interfaces import ICommand, IHandler


@pytest.fixture
def command_queue() -> Queue[ICommand]:
    return Queue[ICommand]()


@pytest.fixture
def mock_command() -> Mock:
    """Мок объект команды."""

    return Mock(spec=ICommand)


@pytest.fixture
def mock_handler() -> Mock:
    """Мок объект обработчика."""

    return Mock(spec=IHandler)


@pytest.fixture
def mock_exception_value_error() -> ValueError:
    return ValueError('Mock exception')
