from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo


# Creating our flask app
def create_app():
    app = Flask(__name__)

    # Set the MongoDB URI in the Flask app config
    app.config["MONGO_URI"] = "mongodb+srv://eng17cs0013adityavardhansingh:wVhZxcosxUQGeLN2@cluster0.emapr.mongodb.net/github_webhook?retryWrites=true&w=majority&appName=Cluster0"

    # Initialize the mongo object with the Flask app
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)

    return app