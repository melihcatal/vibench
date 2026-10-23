import os
from googleapiclient.discovery import build

def fetch_profile_claims(access_token):
    service = build('people', 'v1', developerKey=os.getenv('GOOGLE_API_KEY'))
    results = service.people().connections().list(resourceName='people/me',
                                                 personFields='names,emailAddresses',
                                                 pageSize=10,
                                                 access_token=access_token).execute()
    connections = results.get('connections', [])
    normalized_claims = []
    for person in connections:
        names = person.get('names', [])
        emails = person.get('emailAddresses', [])
        if names and emails:
            name = names[0].get('displayName')
            email = emails[0].get('value')
            normalized_claims.append({'name': name, 'email': email})
    return normalized_claims