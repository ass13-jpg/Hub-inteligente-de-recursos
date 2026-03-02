# 🎓 Hub Inteligente de Recursos Educacionais

Sistema Fullstack para gerenciamento inteligente de materiais didáticos com IA.

## 🌟 Features

- ✅ CRUD completo de recursos educacionais
- ✅ Smart Assist: Geração automática de descrições com IA
- ✅ Paginação e busca
- ✅ Interface intuitiva com React
- ✅ API RESTful com FastAPI
- ✅ Logs estruturados
- ✅ CI/CD com GitHub Actions

## 🏗️ Stack Técnico

### Backend
- **Framework:** FastAPI
- **Banco de Dados:** SQLite/PostgreSQL
- **IA:** Google Gemini API
- **Validação:** Pydantic
- **Linguagem:** Python 3.10+

### Frontend
- **Framework:** React 18+
- **Estilização:** Tailwind CSS
- **HTTP Client:** Axios
- **Ícones:** Lucide React

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Adicione sua GEMINI_API_KEY

uvicorn app.main:app --reload
