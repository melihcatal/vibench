from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID
from identity_models import CodeDelivery
from botocore.exceptions import ClientError

def start_password_reset(email: str) -> CodeDelivery:
    client = get_cognito_client()
    try:
        response = client.forgot_password(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=email,
        )
        code_delivery_dict = response['CodeDeliveryDetails']
        return CodeDelivery(
            destination=code_delivery_dict['Destination'],
            attribute_name=code_delivery_dict['AttributeName'],
            delivery_medium=code_delivery_dict['DeliveryMedium'],
            supplier_name=code_delivery_dict.get('SupplierName')
        )
    except ClientError as e:
        raise ValueError(f"Cognito password reset failed: {e}")