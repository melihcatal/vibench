from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class PasswordReset(BaseModel):
    email: str