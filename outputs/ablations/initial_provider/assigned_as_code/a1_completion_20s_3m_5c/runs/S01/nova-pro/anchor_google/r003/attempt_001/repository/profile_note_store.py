import firebase_admin
from firebase_admin import firestore


def store_profile_note(user_id, note, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    db = firestore.client(app=app)
    user_ref = db.collection('users').document(user_id)
    user_ref.set({
        'notes': firestore.ArrayUnion([note])
    }, merge=True)