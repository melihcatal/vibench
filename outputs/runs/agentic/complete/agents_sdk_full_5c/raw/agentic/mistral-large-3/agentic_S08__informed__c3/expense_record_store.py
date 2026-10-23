import os
from typing import Dict, Any
from ibmcloudant import CouchDbSessionAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense) -> Dict[str, Any]:
    """
    Persists normalized expense records in IBM Cloudant.
    """
    url = os.getenv("IBM_CLOUDANT_URL")
    apikey = os.getenv("IBM_CLOUDANT_APIKEY")
    db_name = os.getenv("IBM_CLOUDANT_DB_NAME", "expenses")

    authenticator = CouchDbSessionAuthenticator(url, apikey)
    client = CloudantV1(authenticator=authenticator)

    document = expense.dict()
    response = client.post_document(db=db_name, document=document)

    return {
        "id": response.result["id"],
        "rev": response.result["rev"],
    }