from .base_repository import BaseRepository

class TodoRepository(BaseRepository):

    INSERT_SQL = 'INSERT INTO t_todo (task, is_done, created_by, created_date) VALUES(%(task)s, %(is_done)s, %(created_by)s, %(created_date)s)'
    FIND_SQL = 'SELECT * FROM t_todo ORDER BY created_date limit %s offset %s'
    COUNT_SQL = 'SELECT count(id) as total FROM t_todo'
    FIND_BY_ID_SQL = 'SELECT * FROM t_todo WHERE id=%s'
    UPDATE_SQL = 'UPDATE t_todo SET is_done=%(is_done)s, last_modified_by=%(last_modified_by)s, last_modified_date=%(last_modified_date)s WHERE id=%(id)s'
    DELETE_SQL = 'DELETE FROM t_todo WHERE id=%s'

    def __init__(self, db):
        BaseRepository.__init__(self, db)

    def find_by_id(self, id):
        return super().find_by_id(self.FIND_BY_ID_SQL, id)

    def find(self, page, size):
        return super().find(self.FIND_SQL, self.COUNT_SQL, page, size)

    def save(self, data):
        return super().save(self.INSERT_SQL, self.FIND_BY_ID_SQL, data)

    def update(self, id, data):
        return super().update(self.UPDATE_SQL, self.FIND_BY_ID_SQL, id, data)

    def delete(self, id):
        return super().delete(self.DELETE_SQL, self.FIND_BY_ID_SQL, id)