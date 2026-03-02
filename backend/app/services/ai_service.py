import google.generativeai as genai
import json
import logging
import time
from app.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """Serviço de Inteligência Artificial"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.AI_MODEL)
    
    @staticmethod
    def _get_system_prompt():
        """Prompt do assistente pedagógico"""
        return """Você é um Assistente Pedagógico especializado em catalogação de recursos educacionais.

TAREFA: Gerar descrição e tags para materiais didáticos.

INSTRUÇÕES:
1. Analise o título e tipo do material
2. Gere uma descrição clara, concisa (máx 200 caracteres) e educacional
3. Sugira exatamente 3 tags relevantes
4. Responda APENAS em JSON válido, sem markdown ou formatação extra

FORMATO DE RESPOSTA (JSON PURO):
{
    "description": "Descrição clara e educacional do material",
    "tags": ["tag1", "tag2", "tag3"]
}

Importante: Retorne APENAS JSON válido."""

    async def generate_assist(self, title: str, resource_type: str) -> dict:
        """Gera descrição e tags com IA"""
        try:
            start_time = time.time()
            
            prompt = f"""Título: {title}
Tipo: {resource_type}

Gere descrição e tags para este recurso educacional."""
            
            response = self.model.generate_content(
                f"{self._get_system_prompt()}\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    max_output_tokens=200
                )
            )
            
            latency = time.time() - start_time
            response_text = response.text.strip()
            
            # Parser JSON
            try:
                ai_response = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: extrair JSON do response
                ai_response = self._extract_json(response_text)
            
            # Log estruturado
            logger.info(
                f"[AI Request] Title='{title}', Type='{resource_type}', "
                f"TokenUsage={response.usage.total_tokens}, Latency={latency:.2f}s"
            )
            
            return {
                "description": ai_response.get("description", ""),
                "tags": ai_response.get("tags", [])[:3]
            }
            
        except Exception as e:
            logger.error(f"[AI Error] {str(e)}")
            raise

    @staticmethod
    def _extract_json(text: str) -> dict:
        """Extrai JSON de resposta não-estruturada"""
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"description": "", "tags": []}
