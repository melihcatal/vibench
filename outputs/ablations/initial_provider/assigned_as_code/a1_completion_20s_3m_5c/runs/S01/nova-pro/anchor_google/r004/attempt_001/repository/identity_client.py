import firebase_admin
from firebase_admin import auth


def get_app(config):
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    return app


def normalize_user(user):
    return {
        'uid': user.uid,
        'email': user.email,
        'password': user.password
    }