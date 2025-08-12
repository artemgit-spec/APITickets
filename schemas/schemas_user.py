from pydantic import BaseModel, EmailStr
 
 
class CreateUser(BaseModel):
    name: str = "user"
    password: str = "user"
    mail_user: EmailStr
    is_admin: str = "user"
    
        
class InfoUser(BaseModel):
    id: int
    name: str
    is_admin: str
    mail_users: EmailStr
