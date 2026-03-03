from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from app.services.ai_service import get_ai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI"])

class AIAssistRequest(BaseModel):
    title: str
    resource_type: str

@router.post("/assist")
async def assist(request: AIAssistRequest):
    """
    Endpoint para gerar descrição e tags com IA
    """
    try:
        logger.info(f"AI Assist solicitado para: {request.title}")
        
        ai_service = get_ai_service()
        result = ai_service.assist(request.title, request.resource_type)
        
        logger.info(f"AI Assist sucesso para: {request.title}")
        
        return {
            "data": {
                "description": result["description"],
                "tags": result["tags"]
            }
        }
    except ValueError as e:
        logger.error(f"AI Config Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Configuração de IA: {str(e)}")
    except Exception as e:
        logger.error(f"AI Assist Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar com IA: {str(e)}")

@router.get("/health")
async def health():
    """
    Verificar saúde do serviço de IA
    """
    try:
        ai_service = get_ai_service()
        return {
            "status": "healthy",
            "model": ai_service.model_name
        }
    except Exception as e:
        logger.error(f"AI Health Check Failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }