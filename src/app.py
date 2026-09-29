# This program creates a small Flask web application with a single /hello route
# that returns "Hello World!". The same application is used in both experiments:
# it runs once with Gunicorn using 20 threads (multithreading), and it runs inside
# 20 separate Docker containers (containers).

from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')

    def hello():
        return 'Hello World!'

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
