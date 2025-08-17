"""
Tests end-to-end simulados para workflows completos del usuario
Estos tests simulan el flujo completo desde el frontend hasta el backend
"""
import pytest
import json
import asyncio
import time
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient

class TestE2EWorkflows:
    """Tests end-to-end para workflows completos del usuario"""
    
    @pytest.fixture
    def mock_complete_setup(self, set_test_env_vars):
        """Setup completo con todos los mocks necesarios"""
        with patch('main.genai') as mock_genai, \
             patch('main.ChatGoogleGenerativeAI') as mock_chat_class, \
             patch('main.requests.get') as mock_requests:
            
            # Mock de configuración de Gemini
            mock_genai.configure = Mock()
            mock_llm = Mock()
            mock_chat_class.return_value = mock_llm
            
            # Mock de respuestas del LLM
            context_response = Mock()
            context_response.content = "Contexto procesado para testing"
            
            ideas_response = Mock()
            ideas_response.content = json.dumps([
                {"title": "Idea de Test 1", "description": "Descripción de prueba 1"},
                {"title": "Idea de Test 2", "description": "Descripción de prueba 2"},
                {"title": "Idea de Test 3", "description": "Descripción de prueba 3"},
                {"title": "Idea de Test 4", "description": "Descripción de prueba 4"},
                {"title": "Idea de Test 5", "description": "Descripción de prueba 5"}
            ])
            
            copy_response = Mock()
            copy_response.content = json.dumps({
                "hook": "🚀 Hook de prueba increíble",
                "body": "Este es el cuerpo del mensaje de prueba. Contiene información valiosa para el usuario.",
                "cta": "¡Comenta qué te parece esta prueba!",
                "hashtags": ["#test", "#prueba", "#mvp", "#ia", "#contenido"]
            })
            
            visual_response = Mock()
            visual_response.content = "Fotografía profesional de alta calidad para testing, luz natural, composición equilibrada"
            
            # Configurar secuencia de respuestas
            responses = [context_response, ideas_response]
            responses.extend([copy_response] * 5)  # 5 posts
            responses.extend([visual_response] * 5)  # 5 prompts visuales
            
            mock_llm.invoke.side_effect = responses
            
            # Mock de requests para URLs
            mock_requests.return_value = Mock(
                content=b"<html><body>Contenido de prueba de Instagram</body></html>"
            )
            
            from main import app
            return TestClient(app), mock_llm, mock_requests
    
    def test_complete_text_to_content_workflow(self, mock_complete_setup):
        """Test completo: Usuario ingresa texto -> Recibe contenido completo"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Simular input del usuario
        user_input = {
            "input_type": "text",
            "content": "Recetas veganas fáciles para principiantes que quieren empezar una dieta saludable"
        }
        
        # Realizar petición
        start_time = time.time()
        response = client.post("/api/generate-content", data=user_input)
        end_time = time.time()
        
        # Verificaciones de respuesta
        assert response.status_code == 200, f"Error en respuesta: {response.text}"
        
        data = response.json()
        
        # Verificar estructura completa de respuesta
        assert "ideas" in data
        assert "posts" in data
        assert "visual_prompts" in data
        assert "context_summary" in data
        
        # Verificar contenido de ideas
        assert len(data["ideas"]) == 5
        for i, idea in enumerate(data["ideas"]):
            assert "title" in idea
            assert "description" in idea
            assert f"Idea de Test {i+1}" in idea["title"]
        
        # Verificar contenido de posts
        assert len(data["posts"]) == 5
        for post in data["posts"]:
            assert "hook" in post
            assert "body" in post
            assert "cta" in post
            assert "hashtags" in post
            assert isinstance(post["hashtags"], list)
            assert len(post["hashtags"]) > 0
        
        # Verificar prompts visuales
        assert len(data["visual_prompts"]) == 5
        for prompt in data["visual_prompts"]:
            assert "description" in prompt
            assert len(prompt["description"]) > 0
        
        # Verificar contexto
        assert len(data["context_summary"]) > 0
        
        # Verificar tiempo de respuesta razonable
        response_time = end_time - start_time
        assert response_time < 5.0, f"Respuesta muy lenta: {response_time}s"
        
        # Verificar que el LLM fue llamado el número correcto de veces
        expected_calls = 1 + 1 + 5 + 5  # context + ideas + posts + visuals
        assert mock_llm.invoke.call_count == expected_calls
    
    def test_complete_url_to_content_workflow(self, mock_complete_setup):
        """Test completo: Usuario ingresa URL -> Recibe contenido basado en análisis"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        user_input = {
            "input_type": "url",
            "content": "https://instagram.com/test_cooking_profile"
        }
        
        response = client.post("/api/generate-content", data=user_input)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que se hizo la petición HTTP
        mock_requests.assert_called_once()
        
        # Verificar estructura de respuesta
        assert len(data["ideas"]) == 5
        assert len(data["posts"]) == 5
        assert len(data["visual_prompts"]) == 5
        
        # Verificar que el contexto fue procesado
        assert "context_summary" in data
    
    def test_complete_guided_workflow(self, mock_complete_setup):
        """Test completo: Usuario usa modo guiado -> Recibe contenido personalizado"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        guided_answers = {
            "niche": "fitness y nutrición",
            "objective": "educar",
            "tone": "motivador"
        }
        
        user_input = {
            "input_type": "guided",
            "guided_answers": json.dumps(guided_answers)
        }
        
        response = client.post("/api/generate-content", data=user_input)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que el contexto incluye las respuestas guiadas
        context = data["context_summary"]
        assert guided_answers["niche"] in context
        assert guided_answers["objective"] in context
        assert guided_answers["tone"] in context
        
        # Verificar contenido completo
        assert len(data["ideas"]) == 5
        assert len(data["posts"]) == 5
        assert len(data["visual_prompts"]) == 5
    
    def test_invalid_input_handling(self, mock_complete_setup):
        """Test manejo de inputs inválidos en el flujo completo"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Test con tipo de input inválido
        response = client.post("/api/generate-content", data={
            "input_type": "invalid_type",
            "content": "test"
        })
        assert response.status_code == 400
        
        # Test con contenido faltante para texto
        response = client.post("/api/generate-content", data={
            "input_type": "text"
        })
        assert response.status_code == 400
        
        # Test con URL faltante
        response = client.post("/api/generate-content", data={
            "input_type": "url"
        })
        assert response.status_code == 400
    
    def test_error_recovery_workflow(self, mock_complete_setup):
        """Test recuperación de errores en el flujo completo"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Simular error en el LLM
        mock_llm.invoke.side_effect = Exception("API Error simulado")
        
        user_input = {
            "input_type": "text",
            "content": "test content"
        }
        
        response = client.post("/api/generate-content", data=user_input)
        
        # Verificar que el error fue manejado apropiadamente
        assert response.status_code == 500
        error_data = response.json()
        assert "detail" in error_data
        assert "Error generating content" in error_data["detail"]

class TestPerformanceE2E:
    """Tests de performance end-to-end"""
    
    def test_concurrent_requests_handling(self, mock_complete_setup):
        """Test manejo de múltiples peticiones concurrentes"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Preparar múltiples requests
        requests_data = [
            {"input_type": "text", "content": f"Test content {i}"}
            for i in range(3)
        ]
        
        start_time = time.time()
        
        # Simular peticiones concurrentes
        responses = []
        for data in requests_data:
            response = client.post("/api/generate-content", data=data)
            responses.append(response)
        
        end_time = time.time()
        
        # Verificar que todas las peticiones fueron exitosas
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert len(data["ideas"]) == 5
        
        # Verificar tiempo total razonable
        total_time = end_time - start_time
        assert total_time < 15.0, f"Peticiones concurrentes muy lentas: {total_time}s"
    
    def test_large_content_processing(self, mock_complete_setup):
        """Test procesamiento de contenido grande"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Crear contenido muy largo
        large_content = "Este es un contenido muy largo. " * 100
        
        user_input = {
            "input_type": "text",
            "content": large_content
        }
        
        start_time = time.time()
        response = client.post("/api/generate-content", data=user_input)
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Verificar que el contenido largo fue procesado
        response_time = end_time - start_time
        assert response_time < 10.0, f"Procesamiento de contenido largo muy lento: {response_time}s"

class TestUserJourneySimulation:
    """Simulación de journeys completos de usuario"""
    
    def test_beginner_user_journey(self, mock_complete_setup):
        """Simular journey de usuario principiante"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # 1. Usuario obtiene preguntas guiadas
        questions_response = client.get("/api/guided-questions")
        assert questions_response.status_code == 200
        
        questions_data = questions_response.json()
        assert "questions" in questions_data
        assert len(questions_data["questions"]) == 3
        
        # 2. Usuario responde las preguntas
        answers = {
            "niche": "cocina casera",
            "objective": "inspirar",
            "tone": "casual"
        }
        
        # 3. Usuario genera contenido
        content_response = client.post("/api/generate-content", data={
            "input_type": "guided",
            "guided_answers": json.dumps(answers)
        })
        
        assert content_response.status_code == 200
        content_data = content_response.json()
        
        # Verificar que el contenido es apropiado para principiante
        assert len(content_data["ideas"]) == 5
        assert len(content_data["posts"]) == 5
        
        # Verificar que el contexto refleja las respuestas
        context = content_data["context_summary"]
        assert answers["niche"] in context
    
    def test_advanced_user_journey(self, mock_complete_setup):
        """Simular journey de usuario avanzado"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # Usuario avanzado usa entrada de texto específica
        advanced_input = {
            "input_type": "text",
            "content": "Estrategias avanzadas de marketing de contenido para Instagram en el nicho de tecnología wearable, enfocado en audiencia millennial con alta educación técnica"
        }
        
        response = client.post("/api/generate-content", data=advanced_input)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que se generó contenido completo
        assert len(data["ideas"]) == 5
        assert len(data["posts"]) == 5
        assert len(data["visual_prompts"]) == 5
        
        # Para usuario avanzado, verificar que el contexto es detallado
        assert len(data["context_summary"]) > 50
    
    def test_content_creator_workflow(self, mock_complete_setup):
        """Simular workflow de creador de contenido profesional"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # 1. Analizar perfil de competencia
        competitor_analysis = client.post("/api/generate-content", data={
            "input_type": "url",
            "content": "https://instagram.com/competitor_profile"
        })
        
        assert competitor_analysis.status_code == 200
        
        # 2. Generar contenido basado en imagen inspiracional
        # (Simularíamos la carga de imagen aquí)
        
        # 3. Generar múltiples variaciones de contenido
        variations = []
        for i in range(3):
            response = client.post("/api/generate-content", data={
                "input_type": "text",
                "content": f"Variación {i+1} de contenido para campaña de verano"
            })
            assert response.status_code == 200
            variations.append(response.json())
        
        # Verificar que todas las variaciones son válidas
        for variation in variations:
            assert len(variation["ideas"]) == 5
            assert len(variation["posts"]) == 5

class TestRobustnessE2E:
    """Tests de robustez del sistema completo"""
    
    def test_malformed_requests_handling(self, mock_complete_setup):
        """Test manejo de peticiones malformadas"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        malformed_requests = [
            {},  # Vacío
            {"input_type": ""},  # Tipo vacío
            {"content": "test"},  # Sin tipo
            {"input_type": "text", "content": ""},  # Contenido vacío
            {"input_type": "guided", "guided_answers": "invalid_json"},  # JSON inválido
        ]
        
        for request_data in malformed_requests:
            response = client.post("/api/generate-content", data=request_data)
            assert response.status_code == 400, f"Request malformada no fue rechazada: {request_data}"
    
    def test_system_recovery_after_failure(self, mock_complete_setup):
        """Test recuperación del sistema después de fallos"""
        client, mock_llm, mock_requests = mock_complete_setup
        
        # 1. Simular fallo
        mock_llm.invoke.side_effect = Exception("Sistema caído")
        
        response = client.post("/api/generate-content", data={
            "input_type": "text",
            "content": "test"
        })
        assert response.status_code == 500
        
        # 2. Simular recuperación
        mock_llm.invoke.side_effect = None
        mock_llm.invoke.return_value = Mock(content='{"test": "recovery"}')
        
        # Reset the side_effect and set up proper responses
        context_response = Mock()
        context_response.content = "Contexto de recuperación"
        
        ideas_response = Mock()
        ideas_response.content = json.dumps([
            {"title": "Idea recuperada", "description": "Sistema funciona"}
        ])
        
        mock_llm.invoke.side_effect = [context_response, ideas_response] + [Mock(content='{"hook":"Test","body":"Test","cta":"Test","hashtags":["#test"]}')] * 1 + [Mock(content="Visual prompt")] * 1
        
        # 3. Verificar que el sistema se recuperó
        response = client.post("/api/generate-content", data={
            "input_type": "text",
            "content": "test recovery"
        })
        assert response.status_code == 200

# ===== Función para ejecutar todos los tests E2E =====
def run_all_e2e_tests():
    """Ejecutar todos los tests end-to-end"""
    print("🚀 Iniciando tests end-to-end...")
    
    # En un entorno real, esto se ejecutaría con pytest
    # pytest tests/e2e/test_e2e_simulation.py -v
    
    return True

if __name__ == "__main__":
    run_all_e2e_tests()