from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class AddTodo(BaseModel):
    name: str
    completed: bool

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        return value.lower().strip()


class TodoResponse(BaseModel):
    id: int
    name: str
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)