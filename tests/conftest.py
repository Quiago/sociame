"""
Configuración compartida para todos los tests
"""
import os
import sys
import pytest
from unittest.mock import Mock, AsyncMock
from PIL import Image
import io

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

@pytest.fixture
def mock_gemini_api():
    """Mock de la API de Gemini para tests"""
    mock = Mock()
    mock.invoke.return_value = Mock(content="Test response from Gemini")
    return mock

@pytest.fixture
def mock_gemini_vision():
    """Mock de Gemini Vision para tests de imágenes"""
    mock = Mock()
    mock.generate_content.return_value = Mock(text="Test image description")
    return mock

@pytest.fixture
def sample_text_input():
    """Texto de ejemplo para tests"""
    return "Recetas veganas fáciles para principiantes"

@pytest.fixture
def sample_url_input():
    """URL de ejemplo para tests"""
    return "https://instagram.com/test_profile"

@pytest.fixture
def sample_guided_answers():
    """Respuestas del modo guiado para tests"""
    return {
        "niche": "cocina vegana",
        "objective": "educar",
        "tone": "amigable"
    }

@pytest.fixture
def sample_image():
    """Imagen de ejemplo para tests"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

@pytest.fixture
def mock_content_ideas():
    """Ideas de contenido de ejemplo"""
    return [
        {"title": "Idea 1", "description": "Descripción 1"},
        {"title": "Idea 2", "description": "Descripción 2"},
        {"title": "Idea 3", "description": "Descripción 3"},
        {"title": "Idea 4", "description": "Descripción 4"},
        {"title": "Idea 5", "description": "Descripción 5"}
    ]

@pytest.fixture
def mock_posts():
    """Posts de ejemplo"""
    return [
        {
            "hook": "¡Descubre recetas increíbles!",
            "body": "En este post te enseñamos recetas veganas fáciles...",
            "cta": "¡Cuéntanos cuál vas a probar!",
            "hashtags": ["#vegano", "#recetas", "#saludable"]
        }
    ]

@pytest.fixture
def mock_visual_prompts():
    """Prompts visuales de ejemplo"""
    return [
        "Fotografía profesional de un plato vegano colorido, vista cenital, luz natural"
    ]

@pytest.fixture
def set_test_env_vars():
    """Configurar variables de entorno para tests"""
    os.environ["GEMINI_API_KEY"] = "test_api_key_12345"
    yield
    # Cleanup after test
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]