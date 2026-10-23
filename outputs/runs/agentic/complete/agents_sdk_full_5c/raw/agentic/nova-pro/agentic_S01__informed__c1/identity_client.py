import os
from firebase_admin import auth, credentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/serviceAccountKey.json'
cred = credentials.Certificate('path/to/serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)

def get_client():
    return auth