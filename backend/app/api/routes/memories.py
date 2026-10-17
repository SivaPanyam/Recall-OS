
from fastapi import APIRouter, HTTPException, status

from app.models.schemas import (
    MemoryCreate,
    MemoryListResponse,
    MemoryResponse,
)
from app.services import memory_service


router = APIRouter(prefix="/memories", tags=["Memories"])


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_memory(payload: MemoryCreate) -> MemoryResponse:
    memory = memory_service.create_memory(
        content=payload.content,
        memory_type=payload.memory_type,
    )
    return MemoryResponse.model_validate(memory)


@router.get("", response_model=MemoryListResponse)
def list_memories() -> MemoryListResponse:
    memories = memory_service.list_memories()

    return MemoryListResponse(
        memories=memories,
        count=len(memories),
    )


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(memory_id: str) -> MemoryResponse:
    memory = memory_service.get_memory(memory_id)

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    return MemoryResponse.model_validate(memory)
