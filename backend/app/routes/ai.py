from fastapi import APIRouter, HTTPException
from app.schemas import AIAssistRequest, AIAssistResponse
from app.services.ai_service import AIService
import logging

router = APIRouter(prefix="/api/ai", tags=["ai"])
logger = logging.getLogger(__name__)

ai_service = AIService()

@router.post("/assist", response_model=AIAssistResponse)
async def smart_assist(request: AIAssistRequest):
    """Gera descrição e tags com IA"""
    try:
        result = await ai_service.generate_assist(
            title=request.title,
            resource_type=request.resource_type
        )
        return AIAssistResponse(**result)
    except Exception as e:
        logger.error(f"AI Assist Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar descrição com IA. Tente novamente."
        )
