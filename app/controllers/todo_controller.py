import logging
from flask import Blueprint, redirect, request, jsonify, url_for, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from markupsafe import escape
from http import HTTPStatus
from marshmallow import ValidationError
from app.schemas import todo_schema
from app.services import todo_service

blueprint  = Blueprint('todo', __name__)
LOG = logging.getLogger(__name__)

@blueprint.route('/', methods=['GET','POST'])
@jwt_required()
def index():
    if(request.method == 'GET'):
        LOG.info('TODO :: GET')
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        return todo_service.find(page, size)
    elif (request.method == 'POST'):
        LOG.info('TODO :: POST')
        return todo_service.save(request.get_json())
            

@blueprint.route('/<id>', methods=['GET','PUT', 'DELETE'])
@jwt_required()
def by_id(id):
    if(request.method == 'GET'):
        return todo_service.find_by_id(id)
    elif (request.method == 'PUT'):
        return todo_service.update(id, request.get_json())
    elif (request.method == 'DELETE'):
        return todo_service.delete(id)