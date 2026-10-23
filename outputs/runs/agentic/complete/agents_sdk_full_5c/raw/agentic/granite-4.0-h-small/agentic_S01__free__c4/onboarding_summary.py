from pydantic import BaseModel

class SummaryRequest(BaseModel):
    user_id: str = Field(..., description="Cognito user identifier")
    email: str = Field(..., description="Registered email address")
    locale: str = Field(..., description="User locale (e.g., en, es, fr)")
    first_name: str = Field(..., description="First name from user attributes")
    profile_text: str = Field(..., description="Moderated profile bio")

class SummaryResponse(BaseModel):
    summary: str = Field(..., description="Human‑readable onboarding state for support")

def onboarding_summary(req: SummaryRequest) -> str:
    """Summarizes onboarding state for support agents.

    Constructs a concise paragraph with user identifiers, language, name, profile content,
    and any pending actions (e.g., password reset in progress). In a real system this
    could call an internal ticketing/search API; here we simply format a string.
    """
    pending = "Password reset requested" if req.email.endswith("_temp") else "None"
    return (f"User ID: {req.user_id} | Email: {req.email} | Locale: {req.locale} | Name: {req.first_name} |"
            f" Profile: "{req.profile_text[:70]}..." | Pending actions: {pending}")