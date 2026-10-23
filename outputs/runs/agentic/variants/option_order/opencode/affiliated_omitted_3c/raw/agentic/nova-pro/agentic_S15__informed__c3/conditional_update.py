from database_client import db

def conditional_update(id, update, condition):
    db.documents.update_one({'_id': id, condition}, {'$set': update})