"""
Tests de integración completos para workflows de IA
"""
import pytest
import json
import io
from unittest.mock import patch, Mock
from PIL import Image

class TestCompleteWorkflows:
    """Tests de integración completos end-to-end"""
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    @patch('main.requests.get')
    def test_complete_text_workflow(self, mock_requests, mock_chat_class, mock_genai, set_test_env_vars):
        """Test completo del workflow con entrada de texto"""
        from main import (
            process_text_context, generate_ideas, generate_copy, 
            generate_visual_prompt, create_content_workflow, ContentGenerationState
        )
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Mock de respuestas del LLM para cada paso
        context_response = Mock()
        context_response.content = "Contexto procesado: recetas veganas para principiantes"
        
        ideas_response = Mock()
        ideas_response.content = json.dumps([
            {"title": "Batido Verde Energético", "description": "Receta rápida de batido verde"},
            {"title": "Pasta Vegana Cremosa", "description": "Pasta con salsa de anacardos"},
            {"title": "Bowl de Quinoa", "description": "Bowl nutritivo y colorido"},
            {"title": "Smoothie Bowl", "description": "Desayuno saludable y bonito"},
            {"title": "Ensalada Rainbow", "description": "Ensalada colorida y nutritiva"}
        ])
        
        copy_response = Mock()
        copy_response.content = json.dumps({
            "hook": "🌱 ¡Transforma tu cocina en 15 minutos!",
            "body": "Estas recetas veganas son perfectas para principiantes. Fáciles, rápidas y deliciosas. No necesitas ser chef para crear platos increíbles.",
            "cta": "¿Cuál vas a probar primero? ¡Cuéntanos en los comentarios!",
            "hashtags": ["#vegano", "#recetasfaciles", "#saludable", "#plantbased", "#comidavegana"]
        })
        
        visual_response = Mock()
        visual_response.content = "Fotografía profesional de un plato vegano colorido con vegetales frescos, luz natural, vista cenital, estilo minimalista"
        
        # Configurar secuencia de respuestas
        mock_llm.invoke.side_effect = [
            context_response,  # process_text_context
            ideas_response,    # generate_ideas
            copy_response,     # generate_copy (llamado 5 veces)
            copy_response,
            copy_response,
            copy_response,
            copy_response,
            visual_response,   # generate_visual_prompt (llamado 5 veces)
            visual_response,
            visual_response,
            visual_response,
            visual_response
        ]
        
        # Ejecutar workflow completo
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = process_text_context("Recetas veganas fáciles para principiantes")
        
        final_state = workflow.invoke(state)
        
        # Verificaciones
        assert final_state.error is None
        assert len(final_state.ideas) == 5
        assert len(final_state.posts) == 5
        assert len(final_state.visual_prompts) == 5
        
        # Verificar estructura de ideas
        for idea in final_state.ideas:
            assert "title" in idea
            assert "description" in idea
            assert isinstance(idea["title"], str)
            assert isinstance(idea["description"], str)
        
        # Verificar estructura de posts
        for post in final_state.posts:
            assert "hook" in post
            assert "body" in post
            assert "cta" in post
            assert "hashtags" in post
            assert isinstance(post["hashtags"], list)
        
        # Verificar prompts visuales
        for prompt in final_state.visual_prompts:
            assert isinstance(prompt, str)
            assert len(prompt) > 0
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    @patch('main.requests.get')
    @patch('main.BeautifulSoup')
    def test_complete_url_workflow(self, mock_soup, mock_requests, mock_chat_class, mock_genai, set_test_env_vars):
        """Test completo del workflow con entrada de URL"""
        from main import process_url_context, create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Mock de requests para URL
        mock_response = Mock()
        mock_response.content = b"<html><body>Instagram profile content</body></html>"
        mock_requests.return_value = mock_response
        
        # Mock de BeautifulSoup
        mock_soup_instance = Mock()
        mock_soup_instance.get_text.return_value = "Instagram profile content"
        mock_soup.return_value = mock_soup_instance
        
        # Mock de respuestas del LLM
        url_context_response = Mock()
        url_context_response.content = "Análisis del perfil: estilo moderno, audiencia joven, contenido lifestyle"
        
        ideas_response = Mock()
        ideas_response.content = json.dumps([
            {"title": "Post Lifestyle", "description": "Contenido inspiracional"},
            {"title": "Tips Diarios", "description": "Consejos útiles"},
            {"title": "Behind Scenes", "description": "Contenido behind the scenes"},
            {"title": "Motivación Lunes", "description": "Post motivacional"},
            {"title": "Fin de Semana", "description": "Contenido de weekend"}
        ])
        
        # Configurar respuestas del LLM
        mock_llm.invoke.side_effect = [url_context_response, ideas_response] + [Mock(content='{"hook":"Test","body":"Test","cta":"Test","hashtags":["#test"]}')] * 5 + [Mock(content="Visual prompt")] * 5
        
        # Ejecutar workflow
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = process_url_context("https://instagram.com/test_profile")
        
        final_state = workflow.invoke(state)
        
        # Verificaciones
        assert final_state.error is None
        assert len(final_state.ideas) == 5
        assert "lifestyle" in state.context.lower() or "instagram" in state.context.lower()
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    def test_complete_image_workflow(self, mock_chat_class, mock_genai, sample_image, set_test_env_vars):
        """Test completo del workflow con entrada de imagen"""
        from main import process_image_context, create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_genai.GenerativeModel = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Mock de Gemini Vision
        mock_vision_model = Mock()
        mock_vision_response = Mock()
        mock_vision_response.text = "La imagen muestra un plato de comida vegana colorida con vegetales frescos"
        mock_vision_model.generate_content.return_value = mock_vision_response
        mock_genai.GenerativeModel.return_value = mock_vision_model
        
        # Mock de respuestas del LLM para el workflow
        ideas_response = Mock()
        ideas_response.content = json.dumps([
            {"title": "Receta Visual", "description": "Inspirado en la imagen"},
            {"title": "Colores Nutritivos", "description": "Alimentación colorida"},
            {"title": "Plato Perfecto", "description": "Presentación de platos"},
            {"title": "Veggie Power", "description": "Poder de los vegetales"},
            {"title": "Food Art", "description": "Arte culinario"}
        ])
        
        # Configurar respuestas
        mock_llm.invoke.side_effect = [ideas_response] + [Mock(content='{"hook":"Test","body":"Test","cta":"Test","hashtags":["#test"]}')] * 5 + [Mock(content="Visual prompt")] * 5
        
        # Ejecutar workflow
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = process_image_context(sample_image)
        
        final_state = workflow.invoke(state)
        
        # Verificaciones
        assert final_state.error is None
        assert len(final_state.ideas) == 5
        assert "imagen" in state.context.lower() or "plato" in state.context.lower()
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    def test_complete_guided_workflow(self, mock_chat_class, mock_genai, sample_guided_answers, set_test_env_vars):
        """Test completo del workflow con modo guiado"""
        from main import process_guided_context, create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Mock de respuestas del LLM
        ideas_response = Mock()
        ideas_response.content = json.dumps([
            {"title": "Cocina Vegana Básica", "description": "Fundamentos de cocina vegana"},
            {"title": "Ingredientes Esenciales", "description": "Lista de básicos veganos"},
            {"title": "Sustitutos Fáciles", "description": "Alternativas veganas simples"},
            {"title": "Menú Semanal", "description": "Planificación de comidas"},
            {"title": "Tips para Empezar", "description": "Consejos para principiantes"}
        ])
        
        # Configurar respuestas
        mock_llm.invoke.side_effect = [ideas_response] + [Mock(content='{"hook":"Test","body":"Test","cta":"Test","hashtags":["#test"]}')] * 5 + [Mock(content="Visual prompt")] * 5
        
        # Ejecutar workflow
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = process_guided_context(sample_guided_answers)
        
        final_state = workflow.invoke(state)
        
        # Verificaciones
        assert final_state.error is None
        assert len(final_state.ideas) == 5
        assert sample_guided_answers["niche"] in state.context
        assert sample_guided_answers["objective"] in state.context
        assert sample_guided_answers["tone"] in state.context

class TestErrorHandling:
    """Tests para manejo de errores en workflows completos"""
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    def test_workflow_error_handling(self, mock_chat_class, mock_genai, set_test_env_vars):
        """Test manejo de errores en el workflow"""
        from main import create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Simular error en el LLM
        mock_llm.invoke.side_effect = Exception("LLM API Error")
        
        # Ejecutar workflow
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = "contexto de prueba"
        
        final_state = workflow.invoke(state)
        
        # Verificar que el error fue capturado
        assert final_state.error is not None
        assert "Error generating ideas" in final_state.error
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    def test_partial_workflow_failure(self, mock_chat_class, mock_genai, set_test_env_vars):
        """Test falla parcial en el workflow"""
        from main import create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Primera llamada exitosa (ideas), segunda falla (posts)
        ideas_response = Mock()
        ideas_response.content = json.dumps([{"title": "Test", "description": "Test"}])
        
        mock_llm.invoke.side_effect = [ideas_response, Exception("Post generation error")]
        
        # Ejecutar workflow
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = "contexto de prueba"
        
        final_state = workflow.invoke(state)
        
        # Verificar que el error fue capturado en el paso correcto
        assert final_state.error is not None
        assert "Error generating posts" in final_state.error

class TestPerformance:
    """Tests de rendimiento básicos"""
    
    @patch('main.genai')
    @patch('main.ChatGoogleGenerativeAI')
    def test_workflow_execution_time(self, mock_chat_class, mock_genai, set_test_env_vars):
        """Test básico de tiempo de ejecución del workflow"""
        import time
        from main import create_content_workflow, ContentGenerationState
        
        # Mock de configuración
        mock_genai.configure = Mock()
        mock_llm = Mock()
        mock_chat_class.return_value = mock_llm
        
        # Mock respuestas rápidas
        ideas_response = Mock()
        ideas_response.content = json.dumps([{"title": "Test", "description": "Test"}])
        
        mock_llm.invoke.side_effect = [ideas_response] + [Mock(content='{"hook":"Test","body":"Test","cta":"Test","hashtags":["#test"]}')] * 1 + [Mock(content="Visual prompt")] * 1
        
        # Medir tiempo de ejecución
        start_time = time.time()
        
        workflow = create_content_workflow()
        state = ContentGenerationState()
        state.context = "contexto de prueba"
        
        final_state = workflow.invoke(state)
        
        execution_time = time.time() - start_time
        
        # Verificar que se ejecuta en tiempo razonable (mock debería ser muy rápido)
        assert execution_time < 1.0  # Menos de 1 segundo con mocks
        assert final_state.error is None