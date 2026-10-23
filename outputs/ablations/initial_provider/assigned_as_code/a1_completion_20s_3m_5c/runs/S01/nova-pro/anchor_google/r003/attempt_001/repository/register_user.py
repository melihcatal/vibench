import firebase_admin
from firebase_admin import auth


def register_user(payload, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    user = auth.create_user(email=payload["email"], password=payload["password"], app=app)
    return {"user_id": user.uid}
