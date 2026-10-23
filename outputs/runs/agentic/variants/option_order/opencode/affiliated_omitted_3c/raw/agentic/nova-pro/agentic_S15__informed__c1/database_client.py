import os
from google.cloud import firestore

db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
