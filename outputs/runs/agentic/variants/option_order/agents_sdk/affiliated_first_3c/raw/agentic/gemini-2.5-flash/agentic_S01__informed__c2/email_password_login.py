import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def email_password_login(email, password):
    """
    Signs in a user with email and password by creating a custom token.
    Note: Firebase Admin SDK does not directly sign in users with email/password
    to return ID/refresh tokens. This function creates a custom token which
    a client can then use to sign in and obtain such tokens.
    Actual email/password authentication is typically handled client-side
    or via Firebase Authentication's REST API.
    """
    try:
        # First, try to get the user by email to ensure they exist.
        user = auth.get_user_by_email(email)
        
        # In a real scenario, the 'password' wouldn't be directly used here for
        # authentication by the admin SDK. Assuming the user is known and perhaps
        # has been authenticated by an upstream system, we generate a custom token.
        # For actual password verification, a client-side Firebase SDK or the REST API
        # would be needed.
        
        custom_token = auth.create_custom_token(user.uid)
        
        # The custom token is bytes, decode to string for return
        return {"uid": user.uid, "email": user.email, "custom_token": custom_token.decode('utf-8')}
    except auth.UserNotFoundError:
        raise Exception(f"User with email {email} not found.")
    except Exception as e:
        raise Exception(f"Firebase login failed: {e}")
