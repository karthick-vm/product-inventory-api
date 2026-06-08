from pydantic import BaseModel

class UserCreate(BaseModel):   # For first user registration only
    username: str
    password: str


# class LoginRequest(BaseModel):
#     username: str
#     password: str

#   ^
#   |
# Using OAuth2PasswordRequestForm instead of LoginRequest
# because OAuth2PasswordBearer expects form-data (username/password)
# and integrates with Swagger Authorize button automatically.