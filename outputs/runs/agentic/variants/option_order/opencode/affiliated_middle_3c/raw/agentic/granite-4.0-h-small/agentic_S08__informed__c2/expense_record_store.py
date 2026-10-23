from normalize_expense import normalize_expense
import pymongo

# Provider: MongoDB Atlas
# Connection URI may be stored in env var MONGODB_ATLAS_URI
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
client = pymongo.MongoClient(MONGO_URI)
# Use database 'expenses' and collection 'records'
db = client.get_database("expenses")
records_coll = db["records"]


def persist_record(raw_output):
    """
    Persist a normalized expense record into MongoDB.
    The record includes a normalized dict plus raw extraction payload.
    Returns the inserted document ID.
    """
    normalized = normalize_expense(raw_output)
    document = {
        "vendor": normalized["vendor_or_merchant"],
        "date": normalized["date"],
        "total": normalized["total"],
        "subtotal": normalized["subtotal"],
        "tax": normalized["tax"],
        "line_items": normalized["line_items"],
        "notes": normalized["notes"],
        # raw payload is stored for audit
        "raw": raw_output,
        "processed_at": pymongo.MongoClient().server_info()["logicalSessionTimeout"],
    }
    result = records_coll.insert_one(document)
    return str(result.inserted_id)
