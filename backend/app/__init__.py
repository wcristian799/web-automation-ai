from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes.news_summarizer import bp as summarizer_bp
    app.register_blueprint(summarizer_bp)

    return app
