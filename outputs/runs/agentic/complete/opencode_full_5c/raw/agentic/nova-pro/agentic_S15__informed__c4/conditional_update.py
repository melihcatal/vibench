from database_client import db
from database_models import Document


def conditional_update(id, update, condition):
    result = db.mycollection.update_one({"_id": id, **condition}, {"$set": update})
    return result.modified_count > 0
