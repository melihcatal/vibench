import firebase_admin
from firebase_admin import auth


def refresh_session(id_token, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    verified_id_token = auth.verify_id_token(id_token, app=app)
    new_tokens = auth.create_custom_token(verified_id_token['uid']).decode('utf-8')
    return {"tokens": new_tokens}