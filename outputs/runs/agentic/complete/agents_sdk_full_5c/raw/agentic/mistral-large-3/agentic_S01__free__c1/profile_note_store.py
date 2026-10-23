import os
from pydantic import BaseModel
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class ProfileNoteRequest(BaseModel):
    user_id: str
    note: str
    metadata: dict


class ProfileNoteResponse(BaseModel):
    success: bool
    note_id: str


def store_profile_note(request: ProfileNoteRequest) -> ProfileNoteResponse:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    data = {
        "user_id": request.user_id,
        "note": request.note,
        "metadata": request.metadata,
    }
    
    response = supabase.table("user_notes").insert(data).execute()
    
    if response.error:
        raise ValueError(f"Failed to store note: {response.error.message}")
    
    return ProfileNoteResponse(
        success=True,
        note_id=response.data[0]["id"]
    )