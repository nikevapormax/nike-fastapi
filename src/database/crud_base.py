from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select

from src.common.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_one_by_id(self, db, get_id: int) -> Optional[ModelType]:
        get_query = select(self.model).where(self.model.id == get_id)
        return db.scalars(get_query).one()

    def get_list(
        self, db, *, limit: Optional[int] = None, offset: Optional[int] = None, cursor: Optional[str] = None
    ) -> List[ModelType]:
        get_query = select(self.model)

        # pagination에 따라 진행
        if limit and offset:
            get_query = get_query.offset(offset).limit(limit)
        elif cursor:
            # get_query = get_query.where(self.model.id > last_item_id).limit(limit)
            pass

        return db.execute(get_query).scalars().all()

    def create(self, db, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(self, db, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data.get(field))

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update_or_create(self, db, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.merge(db_obj)
        db.commit()
        return db_obj

    def remove(self, db, *, remove_id: int) -> None:
        remove_query = select(self.model).where(self.model.id == remove_id)
        obj = db.scalars(remove_query).one_or_none()

        if obj:
            db.delete(obj)
            db.commit()
