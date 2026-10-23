import os

from firebase_admin import credentials, auth


def initialize_app():
    # Initialize the app with a service account, granting admin privileges
    cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_CERT'))
    auth.initialize_app(cred)


def create_user(email, password):
    # Create a new user with email and password
    return auth.create_user(email=email, password=password)


def get_user(uid):
    # Get a user by their UID
    return auth.get_user(uid)


def update_user(uid, **user_properties):
    # Update a user's properties
    return auth.update_user(uid, **user_properties)


def delete_user(uid):
    # Delete a user by their UID
    auth.delete_user(uid)