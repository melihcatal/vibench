import firebase_admin
from firebase_admin import auth


def refresh_session(id_token, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    refreshed_token = auth.refresh_id_token(id_token, app=app)
    return refreshed_token
