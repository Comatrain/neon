from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import UserSchema


async def create_user(
    user: UserSchema,
    db: AsyncSession,
) -> UserSchema:
    model_user = User(**user.model_dump())
    db.add(model_user)
    await db.commit()
    await db.refresh(model_user)
    return user


async def get_user_by_id(user_id: int, db: AsyncSession) -> UserSchema:
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user_model = result.unique().scalars().one()
    user_schema = UserSchema.model_validate(user_model)
    return user_schema


async def get_user_by_name(user_name: str, db: AsyncSession) -> UserSchema:
    stmt = select(User).filter(User.name == user_name)
    result = await db.execute(stmt)
    user_model = result.unique().scalars().one()
    user_schema = UserSchema.model_validate(user_model)
    return user_schema
