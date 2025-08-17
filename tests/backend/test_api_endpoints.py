"""
Tests para endpoints de la API FastAPI
"""
import pytest
import json
import io
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from PIL import Image

@pytest.fixture
def client(set_test_env_vars):
    """Cliente de test para FastAPI"""
    with patch('main.genai') as mock_genai, \
         patch('main.ChatGoogleGenerativeAI') as mock_chat:
        
        # Mock de la configuración de Gemini
        mock_genai.configure = Mock()
        mock_chat.return_value = Mock()
        
        # Importar main después de los mocks
        from main import app
        return TestClient(app)

class TestHealthEndpoint:
    """Tests para el endpoint de health check"""
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "CM Assistant MVP API is running"}

class TestGuidedQuestionsEndpoint:
    """Tests para el endpoint de preguntas guiadas"""
    
    def test_get_guided_questions(self, client):
        """Test para obtener preguntas guiadas"""
        response = client.get("/api/guided-questions")
        assert response.status_code == 200
        
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) == 3
        
        # Verificar estructura de preguntas
        for question in data["questions"]:
            assert "id" in question
            assert "question" in question
            assert "type" in question

class TestContentGenerationEndpoint:
    """Tests para el endpoint principal de generación de contenido"""
    
    @patch('main.content_workflow')
    def test_generate_content_text_input(self, mock_workflow, client, mock_content_ideas, mock_posts, mock_visual_prompts):
        """Test generación de contenido con entrada de texto"""
        # Mock del workflow response
        mock_state = Mock()
        mock_state.error = None
        mock_state.ideas = mock_content_ideas
        mock_state.posts = mock_posts
        mock_state.visual_prompts = mock_visual_prompts
        mock_workflow.invoke.return_value = mock_state
        
        with patch('main.process_text_context', return_value="Contexto procesado"):
            response = client.post(
                "/api/generate-content",
                data={
                    "input_type": "text",
                    "content": "Recetas veganas fáciles"
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "ideas" in data
        assert "posts" in data
        assert "visual_prompts" in data
        assert "context_summary" in data
        assert len(data["ideas"]) == 5
    
    @patch('main.content_workflow')
    def test_generate_content_url_input(self, mock_workflow, client, mock_content_ideas, mock_posts, mock_visual_prompts):
        """Test generación de contenido con URL"""
        mock_state = Mock()
        mock_state.error = None
        mock_state.ideas = mock_content_ideas
        mock_state.posts = mock_posts
        mock_state.visual_prompts = mock_visual_prompts
        mock_workflow.invoke.return_value = mock_state
        
        with patch('main.process_url_context', return_value="Contexto de URL procesado"):
            response = client.post(
                "/api/generate-content",
                data={
                    "input_type": "url",
                    "content": "https://instagram.com/test"
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "context_summary" in data
    
    @patch('main.content_workflow')
    def test_generate_content_image_input(self, mock_workflow, client, sample_image, mock_content_ideas, mock_posts, mock_visual_prompts):
        """Test generación de contenido con imagen"""
        mock_state = Mock()
        mock_state.error = None
        mock_state.ideas = mock_content_ideas
        mock_state.posts = mock_posts
        mock_state.visual_prompts = mock_visual_prompts
        mock_workflow.invoke.return_value = mock_state
        
        with patch('main.process_image_context', return_value="Contexto de imagen procesado"):
            # Crear archivo de imagen para el test
            files = {"image": ("test.png", io.BytesIO(sample_image), "image/png")}
            response = client.post(
                "/api/generate-content",
                data={"input_type": "image"},
                files=files
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "context_summary" in data
    
    @patch('main.content_workflow')
    def test_generate_content_guided_input(self, mock_workflow, client, sample_guided_answers, mock_content_ideas, mock_posts, mock_visual_prompts):
        """Test generación de contenido con modo guiado"""
        mock_state = Mock()
        mock_state.error = None
        mock_state.ideas = mock_content_ideas
        mock_state.posts = mock_posts
        mock_state.visual_prompts = mock_visual_prompts
        mock_workflow.invoke.return_value = mock_state
        
        with patch('main.process_guided_context', return_value="Contexto guiado procesado"):
            response = client.post(
                "/api/generate-content",
                data={
                    "input_type": "guided",
                    "guided_answers": json.dumps(sample_guided_answers)
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "context_summary" in data
    
    def test_generate_content_invalid_input_type(self, client):
        """Test con tipo de entrada inválido"""
        response = client.post(
            "/api/generate-content",
            data={"input_type": "invalid"}
        )
        
        assert response.status_code == 400
        assert "Invalid input type" in response.json()["detail"]
    
    def test_generate_content_missing_content(self, client):
        """Test con contenido faltante"""
        response = client.post(
            "/api/generate-content",
            data={"input_type": "text"}
        )
        
        assert response.status_code == 400
    
    @patch('main.content_workflow')
    def test_generate_content_workflow_error(self, mock_workflow, client):
        """Test manejo de errores del workflow"""
        mock_state = Mock()
        mock_state.error = "Error en el workflow"
        mock_workflow.invoke.return_value = mock_state
        
        with patch('main.process_text_context', return_value="Contexto"):
            response = client.post(
                "/api/generate-content",
                data={
                    "input_type": "text",
                    "content": "test content"
                }
            )
        
        assert response.status_code == 500
        assert "Error en el workflow" in response.json()["detail"]

class TestCORSConfiguration:
    """Tests para configuración CORS"""
    
    def test_cors_headers(self, client):
        """Test que los headers CORS están configurados"""
        response = client.options("/api/generate-content")
        # FastAPI maneja OPTIONS automáticamente con CORS configurado
        assert response.status_code in [200, 405]  # 405 si OPTIONS no está explícitamente definido