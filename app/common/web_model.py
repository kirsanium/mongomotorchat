from pydantic import BaseModel, Field


def to_lower_camel_case(string: str) -> str:
    split_str = string.split('_')
    return split_str[0] + ''.join(word.capitalize() for word in split_str[1:])


class RequestBase(BaseModel):
    class Config:
        alias_generator = to_lower_camel_case


class CreateUserReq(RequestBase):
    name: str
    password: str


class CreateUserResp(BaseModel):
    id: str
    created: bool


class GetUserResp(BaseModel):
    id: str
    name: str


class GetUsersResp(BaseModel):
    users: list[GetUserResp]


class UpdateUserReq(RequestBase):
    name: str | None
    password: str | None
