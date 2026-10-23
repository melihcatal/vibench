import os

class DatabaseClient:
    def __init__(self):
        self.api_key = os.getenv('NOSQL_DB_API_KEY')
        self.base_url = 'https://api.managednosql.com/v1'

    def get_client(self):
        if not self.api_key:
            raise ValueError('API key not set')
        return NoSQLClient(api_key=self.api_key, base_url=self.base_url)

class NoSQLClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def fetch_document(self, document_id):
        # Example method to fetch a document
        url = f'{self.base_url}/documents/{document_id}'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def upsert_document(self, document):
        # Example method to upsert a document
        url = f'{self.base_url}/documents'
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=document)
        response.raise_for_status()
        return response.json()

import requests