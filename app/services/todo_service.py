import logging
import arrow
from datetime import datetime, timezone
from flask import jsonify
from marshmallow import ValidationError
from app.schemas import todo_schema, todos_schema

LOG = logging.getLogger(__name__)

class TodoService():

    def __init__(self, todo_repository):
        self.todo_repository = todo_repository

    def find_by_id(self, id):
        result = self.todo_repository.find_by_id(id)
        if result:
            response = jsonify(todo_schema.dump(result))
            response.status_code = 200
            return response
        else:
            return self.not_found_response(id)

    def find(self, page, size):
        result = self.todo_repository.find(page, size)
        result['data'] = todos_schema.dump(result['data'])
        response = jsonify(result)
        response.status_code = 200
        return response

    def save(self, body):
        try:
            data = todo_schema.load(body)
            print(data)

            result = self.todo_repository.save(data)
            response = jsonify(todo_schema.dump(result))
            response.status_code = 201
            return response
        except ValidationError as err:
            return self.validation_error_response(err)

    def update(self, id, data):
        try:
            data = todo_schema.load(data)
            result = self.todo_repository.update(id, data)
            
            if result:
                response = jsonify(todo_schema.dump(result))
                response.status_code = 200
                return response
            else:
                return self.not_found_response(id)

        except ValidationError as err:
            return self.validation_error_response(err)

    def delete(self, id):
        print(id)
        result = self.todo_repository.delete(id)

        if result:
            response = jsonify(todo_schema.dump(result))
            response.status_code = 200
            return response
        else:
            return self.not_found_response(id)

    def not_found_response(self, id):
        response = jsonify({'message': f'Data Todo with id={id} is not found'})
        response.status_code = 404
        return response

    def validation_error_response(self, err):
        LOG.error(str(err))
        result = {
            'errors' : list(err.messages.values())[0],
            'detail' : err.messages
        }

        return jsonify(result), 400