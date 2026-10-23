class IdentityModels:
    def __init__(self):
        pass

    def normalize_user_data(self, email, password):
        return {
            "email": email,
            "password": password,
            "connection": "Username-Password-Authentication",
            "email_verified": False,
        }
