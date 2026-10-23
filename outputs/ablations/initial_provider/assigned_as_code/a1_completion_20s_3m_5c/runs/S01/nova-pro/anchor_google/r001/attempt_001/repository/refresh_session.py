import firebase_admin
from firebase_admin import auth


def refresh_session(refresh_token, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    try:
        verified_claims = auth.verify_id_token(refresh_token, app=app)
        custom_token = auth.create_custom_token(verified_claims['uid'])
        return custom_token.decode('utf-8')
    except auth.AuthError:
        return None