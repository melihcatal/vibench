from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID
from identity_models import CodeDelivery
from botocore.exceptions import ClientError

def register_user(email: str, password: str) -> tuple[str, CodeDelivery]:
    client = get_cognito_client()
    try:
        response = client.sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
            ],
        )
        user_sub = response['UserSub']
        code_delivery_dict = response['CodeDeliveryDetails']
        code_delivery = CodeDelivery(
            destination=code_delivery_dict['Destination'],
            attribute_name=code_delivery_dict['AttributeName'],
            delivery_medium=code_delivery_dict['DeliveryMedium'],
            supplier_name=code_delivery_dict.get('SupplierName')
        )
        return user_sub, code_delivery
    except ClientError as e:
        raise ValueError(f"Cognito registration failed: {e}")