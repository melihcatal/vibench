import os
import requests


def store_expense_record(record):
    response = requests.post(os.getenv('DOCUMENT_STORE_ENDPOINT'), json=record)
    if response.status_code!= 200:
        raise Exception('Document store service error')