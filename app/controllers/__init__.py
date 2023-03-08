from .error import error_handlers

def register_routes(app):
    
    from .main_controller import blueprint as main_blueprint
    from .todo_controller import blueprint as todo_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(todo_blueprint, url_prefix='/api/todos')

    error_handlers(app)