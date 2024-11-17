import logging
import unittest
from io import StringIO

from pytracelog.logging.handlers import (
    StdoutHandler,
    StderrHandler,
    TracerHandler,
)


# Базовый класс для тестов обработчиков
class BaseHandlerTest(unittest.TestCase):

    def setUp(self, handler_class):
        # Создание объекта StringIO для захвата вывода
        self.capture = StringIO()
        
        # Создание обработчика
        self.handler = handler_class(stream=self.capture)
        
        # Настройка логгера
        self.logger = logging.getLogger("TestLogger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        # Удаление обработчика после тестов
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def verify_output(self, expected_in, expected_not_in):
        #Проверяем, что сообщения присутствуют или отсутствуют в захваченном выводе.
        captured_output = self.capture.getvalue()
        for msg in expected_in:
            self.assertIn(msg, captured_output)
        for msg in expected_not_in:
            self.assertNotIn(msg, captured_output)

# Тесты для обработчика StdoutHandler
class TestStdoutHandler(BaseHandlerTest):

    def setUp(self):
        super().setUp(StdoutHandler)
    
    def test_info_message(self):
        """Проверяем, корректную работу StdoutHandler"""
        self.logger.info("test info message")
        self.logger.warning("test warning message")
        self.logger.error("test error message")
        self.logger.critical("test critical message")
        self.verify_output(
            expected_in=["test info message", "test warning message"],
            expected_not_in=["test error message", "test critical message"]
        )

# Тесты для обработчика StderrHandler
class TestStderrHandler(BaseHandlerTest):

    def setUp(self):
        super().setUp(StderrHandler)

    def test_stderr_message(self):
        """Проверяем, корректную работу StderrHandler"""
        self.logger.error("test error message")
        self.logger.critical("test critical message")
        self.logger.info("test info message")
        self.logger.warning("test warning message")
        self.verify_output(
            expected_in=["test error message", "test critical message"],
            expected_not_in=["test info message", "test warning message"]
        )


# Тесты для обработчика TracerHandler
class TestTracerHandler(unittest.TestCase):
    def setUp(self):
        self.handler = TracerHandler()
        self.logger = logging.getLogger("TestLogger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.logger.removeHandler(self.handler)

    def test_error_message_with_exception(self):
        """Проверяем, корректную работу TracerHandler"""
        try:
            1 / 0
        except ZeroDivisionError as e:
            with self.assertLogs("TestLogger", level='ERROR') as log:
                self.logger.error("error message with an exception", exc_info=e)

        # Проверяем, что в логе присутствует сообщение об ошибке и информация об исключении
        self.assertIn("error message with an exception", log.output[0])
        self.assertIn("ZeroDivisionError", log.output[0])



# if __name__ == '__main__':
#     unittest.main(verbosity=2, exit=False)
