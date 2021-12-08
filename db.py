import databases
import ormar
import sqlalchemy
import uuid

database = databases.Database("sqlite:///db.sqlite")
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class Users(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    
    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    pub_id: uuid.UUID = ormar.UUID(uuid_format='hex')
    email: str = ormar.String(max_length=64, unique=True)
    password: str = ormar.String(max_length=128)
    is_active: bool = ormar.Boolean(default=True)
