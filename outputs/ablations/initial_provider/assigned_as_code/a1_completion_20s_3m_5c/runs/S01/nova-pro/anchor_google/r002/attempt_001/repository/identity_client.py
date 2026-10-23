import os
import firebase_admin


def get_config():
    return {
        "project_id": os.getenv('FIREBASE_PROJECT_ID')
    }


def initialize_firebase_app(config):
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    return app
