from googleapiclient.discovery import build


def fetch_profile_claims(access_token):
    service = build('people', 'v1', developerKey='YOUR_API_KEY')
    people_service = service.people()
    response = people_service.get(resourceName='people/me', personFields='names,emailAddresses').execute(http=access_token)
    
    profile_claims = {
        'name': response.get('names', [{}])[0].get('displayName', ''),
        'email': response.get('emailAddresses', [{}])[0].get('value', '')
    }
    return profile_claims