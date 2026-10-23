from alibabacloud_idaas_eiam import Client as IDaaSClient
from alibabacloud_idaas_eiam.api import CreateUserRequest


def register_user(email, password):
    client = IDaaSClient(
        access_key_id="your_access_key_id", access_key_secret="your_access_key_secret"
    )
    request = CreateUserRequest()
    request.user_name = email
    request.password = password
    response = client.create_user(request)
    return response
