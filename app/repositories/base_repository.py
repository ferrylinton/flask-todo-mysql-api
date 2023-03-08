from flask import Flask, redirect, request, jsonify, url_for, abort
from http import HTTPStatus
from mysql.connector import Error

class BaseRepository(object):

    def __init__(self, db):
        self.db = db

    def find_by_id(self, find_by_id_sql, id):
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(find_by_id_sql, (id,))

            return cursor.fetchone()
        except Exception as err:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def find(self, find_sql, count_sql, page, size):

        result = {
            'data': [],
            'total' : 0,
            'page': page,
            'size': size
        }

        try:
            connection = self.db.get_connection()

            cursor = connection.cursor(dictionary=True)
            cursor.execute(find_sql, (size, (page-1)))
            result['data'] = cursor.fetchall()

            cursor.execute(count_sql)
            result['total'] = cursor.fetchone()['total']

            return result
        except Error as sqle:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST, description=str(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def save(self, insert_sql, find_by_id_sql, data):
        try:
            connection = self.db.get_connection()
            connection.autocommit = False
            cursor = connection.cursor(dictionary=True)

            # insert new data
            cursor.execute(insert_sql, data)

            if cursor.rowcount:
                print(f'{cursor.rowcount} row(s) is inserted')
            
            
            # get new data
            cursor.execute(find_by_id_sql, (cursor.lastrowid,))
            row = cursor.fetchone()
            connection.commit()

            return row
        except Exception as err:
            connection.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self, update_sql, find_by_id_sql, id, data):
        try:
            connection = self.db.get_connection()
            connection.autocommit = False
            cursor = connection.cursor(dictionary=True)

            cursor.execute(find_by_id_sql, (id,))
            row = cursor.fetchone()

            if row:
                data['id'] = id
                cursor.execute(update_sql, data)
                connection.commit()
                
                cursor.execute(find_by_id_sql, (id,))
                return cursor.fetchone()
            else:
                return None

        except Error as err:
            connection.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete(self, delete_sql, find_by_id_sql, id):
        try:
            connection = self.db.get_connection()
            connection.autocommit = False
            cursor = connection.cursor(dictionary=True)

            cursor.execute(find_by_id_sql, (id,))
            row = cursor.fetchone()

            if row:
                print(delete_sql)
                print(find_by_id_sql)
                print(id)
                cursor.execute(delete_sql, (id,))
                connection.commit()
                return row
            else:
                return None

        except Error as err:
            connection.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()