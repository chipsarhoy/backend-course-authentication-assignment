import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db

class AppUsers(db.Model):
    __tablename__ = "AppUsers"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="user")

    auth = db.relationship("AuthTokens", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def new_user_obj():
        return AppUsers("", "", "user")

class AppUsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "name", "email", "role"]

    user_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    role = ma.fields.String(dump_default="user")

user_schema = AppUsersSchema()
users_schema = AppUsersSchema(many=True)