import firebase_admin
from firebase_admin import auth


def refresh_session(token, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    try:
        decoded_token = auth.verify_id_token(token, app=app)
        uid = decoded_token['uid']
        new_token = auth.create_custom_token(uid).decode('utf-8')
        return {"new_token": new_token}
    except auth.AuthError as e:
        return {"error": str(e)}