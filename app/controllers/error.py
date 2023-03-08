import logging
from werkzeug.exceptions import InternalServerError, NotFound, Forbidden, HTTPException
from flask import jsonify

LOG = logging.getLogger(__name__)

def error_handlers(app):

    @app.errorhandler(InternalServerError)
    def internal_server_error(error):
        LOG.exception(error);
        response = jsonify({
            "code": error.code,
            "name": error.name,
            "description": error.description,
        })
        response.content_type = "application/json"
        response.status_code = 500
        return response

    @app.errorhandler(NotFound)
    def not_found(error):
        response = jsonify({
            "code": error.code,
            "name": error.name,
            "description": error.description,
        })
        response.content_type = "application/json"
        response.status_code = 404
        return response

    @app.errorhandler(Exception)
    def handle_error(error):
        LOG.exception(error);
        code = 500
        if isinstance(error, HTTPException):
            code = error.code

        response = jsonify({
            "code": code,
            "description": str(error),
        })

        response.content_type = "application/json"
        response.status_code = code
        return response


    @app.errorhandler(Forbidden)
    def forbidden(*args, **kwargs):
        return render_template('errors/403.html'), 403