from app.repositories import todo_repository
from .todo_service import TodoService


todo_service = TodoService(todo_repository)
