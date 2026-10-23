import boto3

cognito_idp = boto3.client('cognito-idp')

def fetch_and_normalize_profile_claims(access_token):
    try:
        response = cognito_idp.get_user(
            AccessToken=access_token
        )
        user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        normalized_claims = {
            'username': user_attributes.get('username', ''),
            'email': user_attributes.get('email', ''),
            'phone_number': user_attributes.get('phone_number', ''),
            'name': user_attributes.get('name', ''),
            'given_name': user_attributes.get('given_name', ''),
            'family_name': user_attributes.get('family_name', ''),
        }
        return normalized_claims
    except Exception as e:
        print(f'Error fetching profile claims: {e}')
        return None