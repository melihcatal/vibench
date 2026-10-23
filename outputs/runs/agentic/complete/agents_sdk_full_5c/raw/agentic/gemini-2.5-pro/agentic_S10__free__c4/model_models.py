from pydantic import BaseModel, Field
from typing import Optional

# Shared model name for the same-scenario tasks
GEMINI_MODEL_NAME = "gemini-1.5-flash"

class UserInfo(BaseModel):
    """Represents extracted user information."""
    name: str = Field(description="The full name of the user.")
    email: Optional[str] = Field(description="The email address of the user.", default=None)
    age: Optional[int] = Field(description="The age of the user.", default=None)
