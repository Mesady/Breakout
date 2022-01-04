
from psycopg2 import Error
from typing import Optional
from typing import List
from typing import Tuple
from mysql.connector import connect, Error


class ServiceDB:
    def __init__(self):
        self.connection = connect(host="localhost", user="peter", password="PASSWORd", database="messady")
        self.cursor = self.connection.cursor()


    def execute_select(
            self, table: str,
            joins: Optional[List[Tuple[str, str, str]]] = None,
            fields: Optional[List[str]] = None,
            group_by: Optional[str] = None,
            order_by: Optional[str] = None,
            **where
    ):
        fields = ['*'] if fields is None else fields
        query = f'SELECT {", ".join(fields)} FROM {table}'
        if joins:
            query += ' JOIN ' + ' JOIN '.join([f'{tab} AS {short} ON {rule}' for tab, short, rule in joins])
        if where:
            query += ' WHERE ' + ' AND '.join([f'{x}={y}' for x, y in where.items()])
        if group_by:
            query += f' GROUP BY {group_by}'
        if order_by:
            query += f' ORDER BY {order_by} DESC'
        query += ';'
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except (Exception, Error) as error:
            print("Запрос на выборку не удался: ", error)
            self.connection.rollback()
            return None

    def execute_insert(self,table,fields,values):
        query = 'INSERT INTO '
        query += table + '('
        query += fields + ') VALUES ('
        query += values + ');'
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return
        except (Exception, Error) as error:
            print("Вставка не удалась: ", error)
            self.connection.rollback()
            return error

    def execute_update(self,table,fields,condition):
        query = 'UPDATE '
        query += table + ' SET '
        query += fields + ' WHERE '
        query += condition + ';'
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return
        except (Exception, Error) as error:
            print("Обновление не удалось: ", error)
            self.connection.rollback()
            return error
