from identity_client import IdentityClient
from identity_models import RegistrationRequest, RegistrationResponse

def register_user(request: RegistrationRequest) -> RegistrationResponse:
    identity_client = IdentityClient()
    result = identity_client.register(request.email, request.password)
    if "user_id" in result:
        return RegistrationResponse(user_id=result["user_id"], message=result["message"])
    else:
        raise Exception(result.get("error", "Unknown registration error"))
