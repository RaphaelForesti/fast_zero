from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = {'from_attributes': True}


class UserSchemaTemp(UserSchema):
    clean_password: Optional[int] = None
    model_config = {'from_attributes': True}


class UserDb(UserSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # created_at: datetime
    # updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoPublic(TodoSchema):
    id: int
    # created_at: datetime
    # updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]
