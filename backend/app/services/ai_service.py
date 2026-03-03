import logging
import os
from typing import Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        model_name = os.getenv('AI_MODEL', 'gemini-pro')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name
        logger.info(f"AI Service iniciado com modelo: {self.model_name}")
    
    def generate_description(self, title: str, resource_type: str) -> Optional[str]:
        """Gera descrição usando IA"""
        try:
            prompt = f"""
            Gere uma descrição concisa e educativa para um recurso educacional com os seguintes detalhes:
            - Título: {title}
            - Tipo: {resource_type}
            
            A descrição deve ter 2-3 frases, ser clara e informativa.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            logger.error(f"[AI Error] {str(e)}")
            raise
    
    def generate_tags(self, title: str, description: str) -> list:
        """Gera tags usando IA"""
        try:
            prompt = f"""
            Baseado no título e descrição abaixo, gere 3-5 tags relevantes em português.
            Retorne apenas as tags separadas por vírgula, sem numeração.
            
            Título: {title}
            Descrição: {description}
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            tags = [tag.strip() for tag in response.text.split(',')]
            return tags
        except Exception as e:
            logger.error(f"[AI Error] {str(e)}")
            raise
    
    def assist(self, title: str, resource_type: str) -> dict:
        """Assist completo com descrição e tags"""
        try:
            description = self.generate_description(title, resource_type)
            tags = self.generate_tags(title, description)
            
            return {
                "description": description,
                "tags": tags
            }
        except Exception as e:
            logger.error(f"[AI Error] {str(e)}")
            raise

# Singleton instance
_ai_service: Optional[AIService] = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service