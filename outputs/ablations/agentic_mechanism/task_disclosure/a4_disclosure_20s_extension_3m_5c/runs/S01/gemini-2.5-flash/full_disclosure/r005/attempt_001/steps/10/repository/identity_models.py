
class EmailPasswordSignInRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordSignInResponse:
    def __init__(self, access_token, refresh_token, user_id, email):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.email = email

class EmailPasswordUser:
    def __init__(self, user_id, email, created_at, updated_at):
        self.user_id = user_id
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "userId": self.user_id,
            "email": self.email,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    @staticmethod
    def from_provider_response(response_data):
        return EmailPasswordUser(
            user_id=response_data.get("localId"),
            email=response_data.get("email"),
            created_at=response_data.get("createdAt"),
            updated_at=response_data.get("lastLoginAt"),
        )
