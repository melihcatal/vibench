import os
from firebase_admin import auth, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
auth.verify_id_token(cred)

# Create a new user
def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        raise e