"""
Tests para las funciones de IA y procesamiento de contexto
"""
import pytest
import json
from unittest.mock import patch, Mock, MagicMock
from PIL import Image
import io

class TestContextProcessing:
    """Tests para funciones de procesamiento de contexto"""
    
    @patch('main.llm')
    def test_process_text_context(self, mock_llm, sample_text_input, set_test_env_vars):
        """Test procesamiento de contexto de texto"""
        from main import process_text_context
        
        # Mock de la respuesta del LLM
        mock_response = Mock()
        mock_response.content = "Contexto procesado: recetas veganas para principiantes"
        mock_llm.invoke.return_value = mock_response
        
        result = process_text_context(sample_text_input)
        
        assert isinstance(result, str)
        assert "recetas veganas" in result.lower()
        mock_llm.invoke.assert_called_once()
    
    @patch('main.requests.get')
    @patch('main.llm')
    def test_process_url_context_success(self, mock_llm, mock_requests, sample_url_input, set_test_env_vars):
        """Test procesamiento exitoso de URL"""
        from main import process_url_context
        
        # Mock de la respuesta HTTP
        mock_response = Mock()
        mock_response.content = b"<html><body>Test Instagram content</body></html>"
        mock_requests.return_value = mock_response
        
        # Mock de la respuesta del LLM
        mock_llm_response = Mock()
        mock_llm_response.content = "Análisis del perfil de Instagram"
        mock_llm.invoke.return_value = mock_llm_response
        
        result = process_url_context(sample_url_input)
        
        assert isinstance(result, str)
        assert "Instagram" in result
        mock_requests.assert_called_once()
        mock_llm.invoke.assert_called_once()
    
    @patch('main.requests.get')
    def test_process_url_context_error(self, mock_requests, sample_url_input, set_test_env_vars):
        """Test manejo de errores en procesamiento de URL"""
        from main import process_url_context
        
        # Simular error de conexión
        mock_requests.side_effect = Exception("Connection error")
        
        result = process_url_context(sample_url_input)
        
        assert "Error procesando URL" in result
    
    @patch('main.genai.GenerativeModel')
    def test_process_image_context_success(self, mock_model_class, sample_image, set_test_env_vars):
        """Test procesamiento exitoso de imagen"""
        from main import process_image_context
        
        # Mock del modelo Gemini Vision
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Descripción detallada de la imagen"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = process_image_context(sample_image)
        
        assert isinstance(result, str)
        assert "imagen" in result.lower()
        mock_model.generate_content.assert_called_once()
    
    @patch('main.genai.GenerativeModel')
    def test_process_image_context_error(self, mock_model_class, sample_image, set_test_env_vars):
        """Test manejo de errores en procesamiento de imagen"""
        from main import process_image_context
        
        # Simular error en Gemini Vision
        mock_model_class.side_effect = Exception("Vision API error")
        
        result = process_image_context(sample_image)
        
        assert "Error procesando imagen" in result
    
    def test_process_guided_context(self, sample_guided_answers, set_test_env_vars):
        """Test procesamiento de contexto guiado"""
        from main import process_guided_context
        
        result = process_guided_context(sample_guided_answers)
        
        assert isinstance(result, str)
        assert sample_guided_answers["niche"] in result
        assert sample_guided_answers["objective"] in result
        assert sample_guided_answers["tone"] in result

class TestContentGeneration:
    """Tests para funciones de generación de contenido"""
    
    @patch('main.llm')
    def test_generate_ideas_success(self, mock_llm, set_test_env_vars):
        """Test generación exitosa de ideas"""
        from main import generate_ideas
        
        # Mock respuesta con JSON válido
        mock_response = Mock()
        mock_response.content = json.dumps([
            {"title": "Idea 1", "description": "Descripción 1"},
            {"title": "Idea 2", "description": "Descripción 2"},
            {"title": "Idea 3", "description": "Descripción 3"},
            {"title": "Idea 4", "description": "Descripción 4"},
            {"title": "Idea 5", "description": "Descripción 5"}
        ])
        mock_llm.invoke.return_value = mock_response
        
        result = generate_ideas("contexto de prueba")
        
        assert isinstance(result, list)
        assert len(result) == 5
        assert all("title" in idea and "description" in idea for idea in result)
        mock_llm.invoke.assert_called_once()
    
    @patch('main.llm')
    def test_generate_ideas_fallback(self, mock_llm, set_test_env_vars):
        """Test fallback cuando JSON es inválido"""
        from main import generate_ideas
        
        # Mock respuesta con JSON inválido
        mock_response = Mock()
        mock_response.content = "respuesta no válida como JSON"
        mock_llm.invoke.return_value = mock_response
        
        result = generate_ideas("contexto de prueba")
        
        assert isinstance(result, list)
        assert len(result) == 5
        # Debe usar el fallback
        assert all("Idea" in idea["title"] for idea in result)
    
    @patch('main.llm')
    def test_generate_copy_success(self, mock_llm, set_test_env_vars):
        """Test generación exitosa de copy"""
        from main import generate_copy
        
        idea = {"title": "Test Idea", "description": "Test description"}
        
        # Mock respuesta con JSON válido
        mock_response = Mock()
        mock_response.content = json.dumps({
            "hook": "Hook atractivo",
            "body": "Cuerpo del mensaje",
            "cta": "Llamada a la acción",
            "hashtags": ["#test1", "#test2", "#test3"]
        })
        mock_llm.invoke.return_value = mock_response
        
        result = generate_copy(idea, "contexto de prueba")
        
        assert isinstance(result, dict)
        assert "hook" in result
        assert "body" in result
        assert "cta" in result
        assert "hashtags" in result
        assert isinstance(result["hashtags"], list)
        mock_llm.invoke.assert_called_once()
    
    @patch('main.llm')
    def test_generate_copy_fallback(self, mock_llm, set_test_env_vars):
        """Test fallback para copy cuando JSON es inválido"""
        from main import generate_copy
        
        idea = {"title": "Test Idea", "description": "Test description"}
        
        # Mock respuesta con JSON inválido
        mock_response = Mock()
        mock_response.content = "respuesta no válida"
        mock_llm.invoke.return_value = mock_response
        
        result = generate_copy(idea, "contexto de prueba")
        
        assert isinstance(result, dict)
        assert "hook" in result
        assert "body" in result
        assert "cta" in result
        assert "hashtags" in result
        # Debe usar el fallback que incluye el título de la idea
        assert idea["title"] in result["hook"]
    
    @patch('main.llm')
    def test_generate_visual_prompt(self, mock_llm, set_test_env_vars):
        """Test generación de prompt visual"""
        from main import generate_visual_prompt
        
        idea = {"title": "Test Idea", "description": "Test description"}
        
        mock_response = Mock()
        mock_response.content = "  Prompt visual detallado para la imagen  "
        mock_llm.invoke.return_value = mock_response
        
        result = generate_visual_prompt(idea, "contexto de prueba")
        
        assert isinstance(result, str)
        assert result.strip() == "Prompt visual detallado para la imagen"
        mock_llm.invoke.assert_called_once()

class TestWorkflowIntegration:
    """Tests para la integración del workflow"""
    
    @patch('main.generate_visual_prompt')
    @patch('main.generate_copy')
    @patch('main.generate_ideas')
    def test_workflow_nodes_integration(self, mock_gen_ideas, mock_gen_copy, mock_gen_visual, set_test_env_vars):
        """Test integración de nodos del workflow"""
        from main import ContentGenerationState, create_content_workflow
        
        # Mock de las funciones de generación
        mock_gen_ideas.return_value = [{"title": "Idea 1", "description": "Desc 1"}]
        mock_gen_copy.return_value = {"hook": "Hook", "body": "Body", "cta": "CTA", "hashtags": ["#test"]}
        mock_gen_visual.return_value = "Visual prompt"
        
        workflow = create_content_workflow()
        
        # Estado inicial
        state = ContentGenerationState()
        state.context = "contexto de prueba"
        
        # Ejecutar workflow
        result = workflow.invoke(state)
        
        assert result.error is None
        assert len(result.ideas) == 1
        assert len(result.posts) == 1
        assert len(result.visual_prompts) == 1
        
        # Verificar que las funciones fueron llamadas
        mock_gen_ideas.assert_called_once_with("contexto de prueba")
        mock_gen_copy.assert_called_once()
        mock_gen_visual.assert_called_once()

class TestValidationFunctions:
    """Tests para funciones de validación"""
    
    def test_valid_inputs(self, set_test_env_vars):
        """Test validación de entradas válidas"""
        # Los tests de validación están principalmente en el frontend
        # Aquí probamos la lógica del backend
        assert True  # Placeholder para validaciones adicionales del backend