from pydantic import BaseModel

class UserRegistration(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str

class RefreshResponse(BaseModel):
    access_token: str
    id_token: str

class ResetTicket(BaseModel):
    reset_password_ticket_id: str