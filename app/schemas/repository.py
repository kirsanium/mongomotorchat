from uuid import uuid4, UUID
from datetime import datetime
import logging
from pymongo import ReturnDocument

from app.conf.config import Config
from app.db.db import AsyncIOMotorClient
from app.models.models import User, UserSecured
from app.common.util import uuid_masker


__db_name = Config.app_settings.get('db_name')
__db_collection = 'users'


async def db_create_user(
    conn: AsyncIOMotorClient,
    name: str,
    password: str
) -> User:
    new_sample_resource = User(
        id=uuid4(),
        name=name,
        password=password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted=False,
    )
    logging.info(
        f'Inserting User {name} into db...'
    )
    await conn[__db_name][__db_collection].insert_one(
        new_sample_resource.mongo()
    )
    logging.info(
        f"User {name} has inserted into db"
    )
    return new_sample_resource


async def db_get_user_with_password(
    conn: AsyncIOMotorClient,
    user_id: UUID
) -> User | None:
    logging.info(f"Getting user {uuid_masker(user_id)}...")
    sample_resource = await conn[__db_name][__db_collection].find_one(
        {'_id': user_id},
    )
    if None is sample_resource:
        logging.info(f"Resource {uuid_masker(user_id)} is None")
    return User.from_mongo(sample_resource)


async def db_get_user_without_password(
    conn: AsyncIOMotorClient,
    user_id: UUID
) -> UserSecured | None:
    logging.info(f"Getting user {uuid_masker(user_id)}...")
    sample_resource = await conn[__db_name][__db_collection].find_one(
        {'_id': user_id},
        {'password': 0}
    )
    if None is sample_resource:
        logging.info(f"Resource {uuid_masker(user_id)} is None")
    return UserSecured.from_mongo(sample_resource)


async def db_get_users_without_password(
    conn: AsyncIOMotorClient,
) -> list[UserSecured]:
    logging.info(f"Getting all users...")
    users: list[UserSecured] = []
    async for user in conn[__db_name][__db_collection].find(
        {},
        {'password': 0}
    ):
        users.append(UserSecured.from_mongo(user))
    for u in users:
        print(u.dict())
    return users


async def db_update_user(
    conn: AsyncIOMotorClient,
    user_id: UUID,
    resource_data: dict
) -> User | None:
    logging.info(
        f'Updating user {uuid_masker(str(user_id))}...'
    )
    user = await conn[__db_name][__db_collection].find_one_and_update(
        {'_id': user_id},
        {'$set': {
            **resource_data,
            "update_time": datetime.utcnow(),
        }},
        return_document=ReturnDocument.AFTER,
    )
    if None is user:
        logging.error(
            f"User {uuid_masker(str(user_id))} not exist"
        )
    else:
        logging.info(
            f'User {uuid_masker(str(user_id))} updated'
        )
    print(user)
    return User.from_mongo(user)


async def db_delete_user(
    conn: AsyncIOMotorClient,
    resource_id: UUID,
) -> bool:
    logging.info(
        f"Deleting User {uuid_masker(str(resource_id))}..."
    )

    result = await conn[__db_name][__db_collection].delete_one(
        {'_id': resource_id}
    )

    if result.deleted_count == 0:
        logging.error(
            f"User {uuid_masker(str(resource_id))} does not exist"
        )
        return False
    else:
        logging.info(
            f'User resource {uuid_masker(str(resource_id))} is deleted'
        )
        return True
