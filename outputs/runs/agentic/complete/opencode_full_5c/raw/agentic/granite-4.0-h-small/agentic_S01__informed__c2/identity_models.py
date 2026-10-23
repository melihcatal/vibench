DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Local request, response models and validation for Email/Password Account Lifecycle

---

# Identity Value Objects

```python
from __future__ import annotations
from typing import TypedDict, Literal
from pydantic import BaseModel
from datetime import datetime


class UserCreateRequest(BaseModel):
    email: str
    password: str
    connection: Literal['Username-Password-Authentication'] = 'Username-Password-Authentication'


class UserCreateResponse(BaseModel):
    user_id: str
    email: str
    created_at: datetime
    last_login: datetime | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: Literal['Bearer']
    expires_in: int
```