from fastapi import APIRouter, Depends, Response
import logging
from uuid import UUID
from app.db.db import get_db, AsyncIOMotorClient
from app.schemas.repository import db_create_user, db_get_users_without_password,\
    db_get_user_without_password, db_update_user, db_delete_user
from app.common.util import uuid_masker
from app.common.error import UnprocessableError
from app.common.web_model import CreateUserReq, CreateUserResp, GetUserResp, UpdateUserReq, GetUsersResp


router = APIRouter()


@router.post('/', include_in_schema=False, status_code=201)
@router.post('', response_model=CreateUserResp, status_code=201,
             responses={
                 400: {}
             }
             )
async def create_user(
    req: CreateUserReq,
    db: AsyncIOMotorClient = Depends(get_db)
):
    logging.info('Receive create user request')

    user_db = await db_create_user(
        db,
        req.name,
        req.password #TODO
    )

    return CreateUserResp(id=str(user_db.id), created=True)


@router.get('/{id}', include_in_schema=False, status_code=200)
@router.get('/{id}', response_model=GetUserResp, status_code=200,
            responses={
                400: {}
            }
            )
async def get_user(
    id: UUID,
    db: AsyncIOMotorClient = Depends(get_db),
) -> GetUserResp:
    logging.info(
        f'Receive get user {uuid_masker(id)} request'
    )

    user = await db_get_user_without_password(
        db,
        id
    )

    if None is user:
        return Response(status_code=404)

    return GetUserResp(id=str(user.id), name=user.name)


@router.get('/', include_in_schema=False, status_code=200)
@router.get('', response_model=GetUsersResp, status_code=200,
            responses={
                400: {}
            }
            )
async def get_users(
    db: AsyncIOMotorClient = Depends(get_db),
) -> GetUsersResp:
    logging.info(
        f'Receive get users {uuid_masker(id)} request'
    )

    users = await db_get_users_without_password(
        db
    )
    return GetUsersResp(users=[GetUserResp(id=str(u.id), name=u.name) for u in users])


@router.put('/{user_id}', include_in_schema=False, status_code=200)
@router.put('/{user_id}', status_code=200,
            responses={
                400: {}
            }
            )
async def update_sample_resource(
    user_id: UUID,
    user_data: UpdateUserReq,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Receive update user {uuid_masker(user_id)} request'
    )

    user = await db_update_user(
        db,
        user_id,
        user_data.dict(exclude_none=True)
    )
    if user is None:
        raise UnprocessableError([])

    return {}


@router.delete('/{user_id}', include_in_schema=False, status_code=200)
@router.delete('/{user_id}', status_code=200,
               responses={
                   400: {}
               }
               )
async def delete_sample_resource(
    user_id: UUID,
    db: AsyncIOMotorClient = Depends(get_db),
):
    logging.info(
        f'Receive delete user {uuid_masker(user_id)} request'
    )

    deleted = await db_delete_user(
        db,
        user_id,
    )
    
    return deleted
