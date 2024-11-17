import logging
import unittest
from pytracelog.base import PyTraceLog



# Тесты для TestPyTraceLog
class TestPyTraceLog(unittest.TestCase):

    def test_extend_log_record(self):
        """Проверяем, работу расширения записи лога"""
        # Расширяем лог-запись
        PyTraceLog.extend_log_record(user='test_user', request_id='12345')

        # Создаем логгер и генерируем запись лога
        logger = logging.getLogger('test_logger')
        logger.error('Test log message')

        # Получаем текущую фабрику лог-записи
        record_factory = logging.getLogRecordFactory()
        record = record_factory('test_logger', logging.ERROR, '', 0, 'Test log message', None, None)

        # Проверяем наличие новых атрибутов в записи
        self.assertEqual(record.user, 'test_user')
        self.assertEqual(record.request_id, '12345')



# if __name__ == '__main__':
#     unittest.main(verbosity=2, exit=False)