import os
from auth0.management import Auth0
from auth0.authentication import Auth0Authentication

class IdentityClient:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.api_audience = os.getenv("AUTH0_API_AUDIENCE")

        if not all([self.domain, self.client_id, self.client_secret, self.api_audience]):
            raise ValueError("Auth0 environment variables (AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_API_AUDIENCE) must be set.")

        self.management = Auth0(self.domain, self.client_secret)
        self.authentication = Auth0Authentication(self.domain, self.client_id)

    def signup(self, email, password, connection="Username-Password-Authentication"):
        # This uses the Management API to create a user. For actual signup flow, you might use
        # a more user-facing method or a specific signup endpoint from Auth0's SDK for web/mobile apps.
        # This example focuses on server-side user creation for demonstration.
        try:
            user = self.management.users.create({
                "email": email,
                "password": password,
                "connection": connection,
                "email_verified": False # Typically email verification happens after signup
            })
            return {"success": True, "user_id": user["user_id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email, password):
        try:
            token_response = self.authentication.login(
                username=email,
                password=password,
                audience=self.api_audience,
                scope="openid profile email"
            )
            return {"success": True, "access_token": token_response["access_token"], "id_token": token_response["id_token"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def change_password(self, user_id, new_password):
        try:
            self.management.users.update(
                user_id,
                {"password": new_password}
            )
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def reset_password_link(self, email, connection="Username-Password-Authentication"):
        try:
            # This method initiates a password reset email to the user.
            # It returns a link that the user can use to reset their password.
            response = self.authentication.request_password_reset(
                email=email,
                connection=connection
            )
            # The response usually contains a message confirming the email was sent or a URL if configured.
            # Auth0's typical flow sends an email directly.
            return {"success": True, "message": "Password reset email initiated."}
        except Exception as e:
            return {"success": False, "error": str(e)}

