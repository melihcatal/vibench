from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import UserRegistration


def create_user(user_data: UserRegistration):
    app = get_firebase_app()
    try:
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name,
            app=app,
        )
        return {"uid": user.uid}
    except Exception as e:
        return {"error": str(e)}
