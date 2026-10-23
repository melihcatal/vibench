import os
from supabase import create_client, Client
from identity_models import RegisterRequest, RegisterResponse
from identity_client import get_identity_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def register_user(request: RegisterRequest) -> RegisterResponse:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Check if user already exists
    existing_user = supabase.table("users").select("email").eq("email", request.email).execute()
    if existing_user.data:
        raise ValueError("User already exists")
    
    # Create user in Supabase Auth
    auth_response = supabase.auth.sign_up({
        "email": request.email,
        "password": request.password,
    })
    
    if auth_response.user is None:
        raise ValueError("User registration failed")
    
    # Store additional user metadata
    user_data = {
        "id": auth_response.user.id,
        "email": request.email,
        "locale": request.locale,
        "profile_text": request.profile_text,
    }
    supabase.table("users").insert(user_data).execute()
    
    return RegisterResponse(
        user_id=auth_response.user.id,
        email=request.email,
        locale=request.locale,
    )