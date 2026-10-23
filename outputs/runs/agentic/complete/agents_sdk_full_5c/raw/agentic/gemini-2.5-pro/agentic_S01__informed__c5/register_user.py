from identity_client import get_identity_client, get_user_pool_id
from identity_models import NewUser, UserRegistration

def register_user(new_user: NewUser) -> UserRegistration:
    """
    Creates a new user in Amazon Cognito User Pools.
    """
    client = get_identity_client()
    user_pool_id = get_user_pool_id()

    attributes = []
    if new_user.attributes:
        for key, value in new_user.attributes.items():
            attributes.append({'Name': key, 'Value': value})

    response = client.sign_up(
        UserPoolId=user_pool_id,
        Username=new_user.email,
        Password=new_user.password,
        UserAttributes=attributes
    )
    
    return UserRegistration(
        user_id=response['UserSub'],
        confirmed=response['UserConfirmed']
    )
