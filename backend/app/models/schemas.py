
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


MemoryType = Literal["learning", "project", "decision", "bug", "fix"]


class RootResponse(BaseModel):
    message: str
    status: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    memory_type: MemoryType

    @field_validator("content")
    @classmethod
    def content_must_not_be_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Content must not be empty or whitespace")
        return value


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content: str
    memory_type: MemoryType
    created_at: datetime
    updated_at: datetime


class MemoryListResponse(BaseModel):
    memories: list[MemoryResponse]
    count: int
