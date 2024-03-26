from uuid import UUID
from pydantic import constr
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class MongoModel(BaseModel):
    id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
        )

        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed


class Message(MongoModel):
    sender_id: UUID
    content: str


class Conversation(MongoModel):
    users: list[UUID]
    messages: list[Message]


class UserSecured(MongoModel):
    name: constr(max_length=255)


class User(UserSecured):
    password: str
