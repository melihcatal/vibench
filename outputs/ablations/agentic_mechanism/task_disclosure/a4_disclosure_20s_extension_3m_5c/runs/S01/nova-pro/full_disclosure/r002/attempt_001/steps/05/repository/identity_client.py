from firebase_admin import auth, credentials

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('path/to/serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)

# Helper function to create a new user
def create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except auth.AuthError as e:
        print(f'Error creating user: {e}')
        return None

# Helper function to get a user by email
def get_user_by_email(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except auth.AuthError as e:
        print(f'Error getting user: {e}')
        return None

# Helper function to delete a user
def delete_user(uid):
    try:
        auth.delete_user(uid)
        return True
    except auth.AuthError as e:
        print(f'Error deleting user: {e}')
        return False
