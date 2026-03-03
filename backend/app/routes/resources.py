from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import logging
from app.database import SessionLocal
from app.models import Resource

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/resources", tags=["Resources"])

class ResourceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    resource_type: str
    url: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    resource_type: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    resource_type: str
    url: Optional[str]
    tags: Optional[str]

    class Config:
        from_attributes = True

@router.get("/", response_model=dict)
async def list_resources(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """
    Lista todos os recursos com paginação
    """
    try:
        db = SessionLocal()
        total = db.query(Resource).count()
        resources = db.query(Resource).offset(skip).limit(limit).all()
        db.close()
        
        return {
            "data": {
                "items": [
                    {
                        "id": r.id,
                        "title": r.title,
                        "description": r.description,
                        "resource_type": r.resource_type,
                        "url": r.url,
                        "tags": r.tags
                    }
                    for r in resources
                ],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        }
    except Exception as e:
        logger.error(f"Erro ao listar recursos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_resource(resource: ResourceCreate):
    """
    Cria um novo recurso
    """
    try:
        db = SessionLocal()
        
        # Converter tags de lista para string
        tags_str = ", ".join(resource.tags) if resource.tags else None
        
        db_resource = Resource(
            title=resource.title,
            description=resource.description,
            resource_type=resource.resource_type,
            url=resource.url,
            tags=tags_str
        )
        
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        
        result = {
            "id": db_resource.id,
            "title": db_resource.title,
            "description": db_resource.description,
            "resource_type": db_resource.resource_type,
            "url": db_resource.url,
            "tags": db_resource.tags
        }
        
        db.close()
        
        return {"data": result}
    except Exception as e:
        logger.error(f"Erro ao criar recurso: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{resource_id}", response_model=dict)
async def get_resource(resource_id: int):
    """
    Obtém um recurso específico
    """
    try:
        db = SessionLocal()
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        db.close()
        
        if not resource:
            raise HTTPException(status_code=404, detail="Recurso não encontrado")
        
        return {
            "data": {
                "id": resource.id,
                "title": resource.title,
                "description": resource.description,
                "resource_type": resource.resource_type,
                "url": resource.url,
                "tags": resource.tags
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar recurso: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{resource_id}", response_model=dict)
async def update_resource(resource_id: int, resource: ResourceUpdate):
    """
    Atualiza um recurso existente
    """
    try:
        db = SessionLocal()
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        
        if not db_resource:
            db.close()
            raise HTTPException(status_code=404, detail="Recurso não encontrado")
        
        if resource.title:
            db_resource.title = resource.title
        if resource.description:
            db_resource.description = resource.description
        if resource.resource_type:
            db_resource.resource_type = resource.resource_type
        if resource.url:
            db_resource.url = resource.url
        if resource.tags:
            db_resource.tags = ", ".join(resource.tags)
        
        db.commit()
        db.refresh(db_resource)
        
        result = {
            "id": db_resource.id,
            "title": db_resource.title,
            "description": db_resource.description,
            "resource_type": db_resource.resource_type,
            "url": db_resource.url,
            "tags": db_resource.tags
        }
        
        db.close()
        
        return {"data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar recurso: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{resource_id}")
async def delete_resource(resource_id: int):
    """
    Deleta um recurso
    """
    try:
        db = SessionLocal()
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        
        if not db_resource:
            db.close()
            raise HTTPException(status_code=404, detail="Recurso não encontrado")
        
        db.delete(db_resource)
        db.commit()
        db.close()
        
        return {"message": "Recurso deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar recurso: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))