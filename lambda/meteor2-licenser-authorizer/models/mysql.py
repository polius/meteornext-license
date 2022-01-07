import pymysql
from collections import OrderedDict
from pymysql.cursors import DictCursorMixin, Cursor

class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict

class mysql:
    def __init__(self):
        self._connection = None

    def connect(self, hostname, username, password, port, database):
        self._connection = pymysql.connect(host=hostname, user=username, password=password, port=port, db=database, charset='utf8mb4', use_unicode=True, cursorclass=pymysql.cursors.DictCursor, autocommit=False, connect_timeout=2)

    def close(self):
        try:
            self._sql.close()
        except Exception:
            pass

    def execute(self, query, args=None):
        with self._connection.cursor(OrderedDictCursor) as cursor:            
            cursor.execute(query, args)
            query_result = cursor.fetchall() if cursor.lastrowid is None else cursor.lastrowid
        self._connection.commit()
        return query_result
