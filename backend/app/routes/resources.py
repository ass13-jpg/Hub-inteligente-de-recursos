from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas import ResourceResponse, ResourceCreate, ResourceUpdate
from app.models import Resource
from app.database import get_db
import logging

router = APIRouter(prefix="/api/resources", tags=["resources"])
logger = logging.getLogger(__name__)

@router.get("/", response_model=dict)
async def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Lista recursos com paginação"""
    total = db.query(Resource).count()
    items = db.query(Resource).offset(skip).limit(limit).all()
    
    logger.info(f"Listed {len(items)} resources (total: {total})")
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post("/", response_model=ResourceResponse)
async def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    """Cria novo recurso"""
    db_resource = Resource(
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        url=resource.url,
        tags=",".join(resource.tags) if resource.tags else ""
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    
    logger.info(f"Created resource: {db_resource.id} - {db_resource.title}")
    
    return db_resource

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Obtém um recurso específico"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    return resource

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource: ResourceUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um recurso"""
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    
    db_resource.title = resource.title
    db_resource.description = resource.description
    db_resource.resource_type = resource.resource_type
    db_resource.url = resource.url
    db_resource.tags = ",".join(resource.tags) if resource.tags else ""
    
    db.commit()
    db.refresh(db_resource)
    
    logger.info(f"Updated resource: {db_resource.id}")
    
    return db_resource

@router.delete("/{resource_id}")
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """Deleta um recurso"""
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    
    db.delete(db_resource)
    db.commit()
    
    logger.info(f"Deleted resource: {resource_id}")
    
    return {"message": "Recurso deletado com sucesso"}
