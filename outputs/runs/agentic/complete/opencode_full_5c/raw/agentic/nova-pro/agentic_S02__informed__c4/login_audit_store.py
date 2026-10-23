import os

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

from pymongo import MongoClient


def login_audit_store(audit_record):
    # MongoDB Atlas storage of audit records
    pass
