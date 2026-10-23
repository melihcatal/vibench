import os
import openai
from identity_models import RegisterUserRequest, RegisterUserResponse
from identity_client import IdentityClient

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    identity_client = IdentityClient()
    registration_result = identity_client.register_user(request.email, request.password)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    try:
        # Using a chat model to generate a welcome message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates welcome messages."},
                {"role": "user", "content": f"Generate a short welcome message for a new user with email {request.email}."}
            ]
        )
        welcome_message = response.choices[0].message.content.strip()
    except Exception as e:
        welcome_message = f"Welcome! Failed to generate a personalized message: {e}"

    return RegisterUserResponse(
        user_id=registration_result["user_id"],
        email=registration_result["email"],
        message=welcome_message
    )
