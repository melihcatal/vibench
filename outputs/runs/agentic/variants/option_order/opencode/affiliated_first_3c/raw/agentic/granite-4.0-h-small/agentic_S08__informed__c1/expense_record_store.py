import os
from ibm_cloudant import CloudantClient  # example: IBM Cloudant SDK

# Load provider credentials from env
cloudant_url = os.getenv("IBM_CLOUDANT_URL")
cloudant_apikey = os.getenv("IBM_CLOUDANT_APIKEY")

if not cloudant_url or not cloudant_apikey:
    raise RuntimeError("IBM_CLOUDANT_URL and IBM_CLOUDANT_APIKEY must be set")

client = CloudantClient(
    url=cloudant_url, auth_method="iam", username="", api_key=cloudant_apikey
)


def store_expense(normalized_expense):
    """
    Persist a normalized expense record to Cloudant (managed NoSQL document store).
    Returns the generated document ID.
    """
    database = client.get_database("expenses", auto_create=True)
    doc = {
        "_id": normalized_expense["vendor"] + "_" + normalized_expense["date"],
        "vendor": normalized_expense["vendor"],
        "date": normalized_expense["date"],
        "total": normalized_expense["total"],
        "items": normalized_expense["items"],
    }
    result = database.create_document(doc)
    return result["_id"]
