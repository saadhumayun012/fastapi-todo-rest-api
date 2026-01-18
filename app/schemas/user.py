from pydantic import BaseModel, Field

# validete the user request
class CreateUserRequest(BaseModel):
    email: str = Field(...)
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str
    password: str = Field(min_length=4, max_length=20)
    role: str
    phone_number: str = Field(...)

#password change
class PasswordChangeRequest(BaseModel):
    password: str = Field(min_length=1)
    new_password: str = Field(min_length=4, max_length=20)

class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(...)