from firebase_admin import auth
from identity_client import get_firebase_app


def send_password_reset_email(email: str):
    app = get_firebase_app()
    try:
        link = auth.generate_password_reset_link(email, app=app)
        # In a real app, you would email this link to the user.
        # For this example, we just return it.
        return {"password_reset_link": link}
    except auth.UserNotFoundError:
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}
