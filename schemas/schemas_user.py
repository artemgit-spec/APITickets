from pydantic import BaseModel, EmailStr
 


class CreateUser(BaseModel):
    name: str = "user"
    password: str = "user"
    mail_user: EmailStr
    is_admin: str = "user"
    
class AuthUser(BaseModel):
    username: str
    password: str
