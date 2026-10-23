import firebase_admin
from firebase_admin import auth


def get_identity_client(config):
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    return auth.Client(app=app)