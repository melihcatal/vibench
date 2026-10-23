import uuid
from identity_client import IdentityClient
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = IdentityClient()
    password = request.password

    if not password and client.openai_client:
        try:
            # Using OpenAI to suggest a strong password
            chat_completion = client.openai_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Generate a strong, random password. It should be at least 12 characters long and include uppercase, lowercase, numbers, and special characters. Provide only the password, no other text."
                    }
                ],
                model=client.openai_deployment_name,
                temperature=0.7,
                max_tokens=50
            )
            suggested_password = chat_completion.choices[0].message.content.strip()
            # Basic validation to ensure it's not just a conversational response
            if len(suggested_password) >= 12 and any(c.isupper() for c in suggested_password) and any(c.islower() for c in suggested_password) and any(c.isdigit() for c in suggested_password):
                password = suggested_password
            else:
                print("OpenAI generated an invalid password, falling back to UUID.")
                password = str(uuid.uuid4()) # Fallback if OpenAI doesn't give a good password
        except Exception as e:
            print(f"Error generating password with OpenAI: {e}")
            password = str(uuid.uuid4()) # Fallback on error
    elif not password:
        password = str(uuid.uuid4()) # Generate a random password if no OpenAI client

    if not password:
        raise ValueError("Password could not be determined for user registration.")

    # In a real scenario, this would involve calling a concrete identity management service
    # For now, we simulate user creation and associate the generated/provided password.
    user_id = str(uuid.uuid4()) # Simulate a new user ID

    return RegisterUserResponse(user_id=user_id, message=f"User {request.email} registered successfully.")
