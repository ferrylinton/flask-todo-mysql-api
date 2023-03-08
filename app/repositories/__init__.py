from app import connection_pool as db
from .todo_repository import TodoRepository


todo_repository = TodoRepository(db)
