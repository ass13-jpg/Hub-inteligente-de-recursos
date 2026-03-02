from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List

class ResourceBase(BaseModel):
    """Schema base para recursos"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    resource_type: str = Field(..., pattern="^(Video|PDF|Link)$")
    url: Optional[str] = None
    tags: Optional[List[str]] = []

class ResourceCreate(ResourceBase):
    """Schema para criação"""
    pass

class ResourceUpdate(ResourceBase):
    """Schema para atualização"""
    pass

class ResourceResponse(ResourceBase):
    """Schema para resposta"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AIAssistRequest(BaseModel):
    """Request para Smart Assist"""
    title: str = Field(..., min_length=1)
    resource_type: str = Field(..., pattern="^(Video|PDF|Link)$")

class AIAssistResponse(BaseModel):
    """Response da IA"""
    description: str
    tags: List[str] = Field(..., max_length=3)
