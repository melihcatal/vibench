from firebase_admin import auth, credentials


def register_user(email, password):
    user = auth.create_user(email=email, password=password)
    return user.uid
