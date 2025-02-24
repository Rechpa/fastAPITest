from pydantic import BaseModel
from typing import Optional

# Base schema
class UserBase(BaseModel):
    name: str
    email: str

# Schema for creating a user
class UserCreate(UserBase):
    pass

# Schema for updating a user (all fields optional)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# Schema for returning a user
class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # For Pydantic V2 (previously `orm_mode` in V1)