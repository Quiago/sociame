"""
Community Manager Assistant MVP - FastAPI Backend
Integrates Gemini AI with LangChain/LangGraph for content generation
"""

import os
from typing import Optional, List, Dict, Any, TypedDict
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
import json

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import google.generativeai as genai
from google import genai as new_genai
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from google.genai import types

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="CM Assistant MVP", description="Community Manager Content Generation Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini APIs
GEMINI_TEXT_API_KEY = os.getenv("GEMINI_TEXT_API_KEY")
GEMINI_IMAGE_API_KEY = os.getenv("GEMINI_IMAGE_API_KEY")



if not GEMINI_TEXT_API_KEY:
    raise ValueError("GEMINI_TEXT_API_KEY environment variable is required")
if not GEMINI_IMAGE_API_KEY:
    raise ValueError("GEMINI_IMAGE_API_KEY environment variable is required")

# Configure text generation
genai.configure(api_key=GEMINI_TEXT_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_TEXT_API_KEY)

# Initialize GenAI client for Imagen
client = new_genai.Client(api_key=GEMINI_IMAGE_API_KEY)

# Pydantic models for request/response
class ContentRequest(BaseModel):
    input_type: str  # "text", "url", "guided"
    content: Optional[str] = None
    guided_answers: Optional[Dict[str, str]] = None

class ContentIdea(BaseModel):
    title: str
    description: str

class PostContent(BaseModel):
    hook: str
    body: str
    cta: str
    hashtags: List[str]

class VisualPrompt(BaseModel):
    description: str
    image_url: Optional[str] = None

class ContentResponse(BaseModel):
    ideas: List[ContentIdea]
    posts: List[PostContent]
    visual_prompts: List[VisualPrompt]
    context_summary: str

# LangGraph State Definition
class ContentGenerationState(TypedDict):
    context: str
    ideas: List[Dict[str, str]]
    posts: List[Dict[str, Any]]
    visual_prompts: List[str]
    error: Optional[str]

# Context Processing Functions
def process_text_context(text: str) -> str:
    """Process plain text input to extract key themes and context"""
    prompt = f"""
    Analiza el siguiente texto y extrae los temas principales, el tono y el contexto relevante 
    para crear contenido de redes sociales para Instagram:
    
    Texto: {text}
    
    Proporciona un resumen conciso del contexto en texto plano, sin formato markdown, 
    que incluya:
    - Tema principal
    - Audiencia objetivo
    - Tono sugerido
    - Palabras clave importantes
    
    Responde con texto corrido, sin asteriscos, guiones, ni ningún tipo de formato markdown.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    # Clean markdown artifacts
    clean_content = response.content.strip()
    clean_content = clean_content.replace('*', '').replace('#', '').replace('-', '').replace('_', '')
    clean_content = ' '.join(clean_content.split())  # Remove extra whitespace
    return clean_content

def process_url_context(url: str) -> str:
    """Extract context from Instagram profile URL or webpage"""
    try:
        # Fetch webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()[:2000]  # Limit to first 2000 chars
        
        prompt = f"""
        Analiza el contenido de esta página web y extrae información relevante para crear 
        contenido similar para Instagram:
        
        URL: {url}
        Contenido: {text_content}
        
        Proporciona un análisis en texto plano, sin formato markdown, del:
        - Estilo de contenido
        - Audiencia objetivo
        - Temas principales
        - Tono de comunicación
        
        Responde con texto corrido, sin asteriscos, guiones, ni ningún tipo de formato markdown.
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        # Clean markdown artifacts
        clean_content = response.content.strip()
        clean_content = clean_content.replace('*', '').replace('#', '').replace('-', '').replace('_', '')
        clean_content = ' '.join(clean_content.split())  # Remove extra whitespace
        return clean_content
        
    except Exception as e:
        return f"Error procesando URL: {str(e)}. Usando contexto genérico."

def process_image_context(image_data: bytes) -> str:
    """Process uploaded image to extract context using Gemini Vision"""
    try:
        # Initialize Gemini Vision model with correct API key
        genai.configure(api_key=GEMINI_TEXT_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Convert bytes to PIL Image
        image = Image.open(BytesIO(image_data))
        
        prompt = """
        Analiza esta imagen y describe detalladamente lo que ves para crear contenido de Instagram relacionado.
        Proporciona un análisis en texto plano, sin formato markdown, que incluya:
        - Descripción visual detallada
        - Posible audiencia objetivo
        - Temas o conceptos que la imagen sugiere
        - Emociones que transmite
        - Ideas de contenido relacionado
        
        Responde con texto corrido, sin asteriscos, guiones, ni ningún tipo de formato markdown.
        """
        
        response = model.generate_content([prompt, image])
        # Clean markdown artifacts
        clean_content = response.text.strip()
        clean_content = clean_content.replace('*', '').replace('#', '').replace('-', '').replace('_', '')
        clean_content = ' '.join(clean_content.split())  # Remove extra whitespace
        return clean_content
        
    except Exception as e:
        return f"Error procesando imagen: {str(e)}. Usando descripción genérica."

def process_guided_context(answers: Dict[str, str]) -> str:
    """Process guided questionnaire answers to create context"""
    niche = answers.get("niche", "general")
    objective = answers.get("objective", "entretener")
    tone = answers.get("tone", "amigable")
    
    context = f"""
    Contexto del usuario:
    - Nicho/Industria: {niche}
    - Objetivo de la publicación: {objective}
    - Tono de voz preferido: {tone}
    
    Crear contenido de Instagram optimizado para esta audiencia y objetivos específicos.
    """
    
    return context

# Content Generation Functions
def generate_ideas(context: str) -> List[Dict[str, str]]:
    """Generate 5 Instagram post ideas based on context"""
    prompt = f"""
    Basándote en el siguiente contexto, genera exactamente 5 ideas creativas y atractivas para publicaciones de Instagram.
    
    Contexto: {context}
    
    Para cada idea, proporciona:
    - Un título atractivo (máximo 8 palabras)
    - Una descripción breve (máximo 25 palabras)
    
    Responde SOLO con un JSON válido, sin texto adicional:
    [
        {{"title": "Título de la idea 1", "description": "Descripción breve de la primera idea"}},
        {{"title": "Título de la idea 2", "description": "Descripción breve de la segunda idea"}},
        {{"title": "Título de la idea 3", "description": "Descripción breve de la tercera idea"}},
        {{"title": "Título de la idea 4", "description": "Descripción breve de la cuarta idea"}},
        {{"title": "Título de la idea 5", "description": "Descripción breve de la quinta idea"}}
    ]
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        # Limpiar la respuesta y extraer solo el JSON
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        ideas_json = json.loads(content)
        if len(ideas_json) == 5 and all("title" in idea and "description" in idea for idea in ideas_json):
            return ideas_json
        else:
            raise ValueError("No se generaron 5 ideas válidas")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        # Fallback genérico basado en el contexto
        import re
        # Extraer palabras clave del contexto
        keywords = re.findall(r'\b\w+\b', context.lower())
        main_topic = keywords[0] if keywords else "contenido"
        
        return [
            {"title": f"Guía completa de {main_topic}", "description": f"Todo lo que necesitas saber sobre {main_topic}"},
            {"title": f"Tips esenciales de {main_topic}", "description": f"Consejos prácticos y útiles para {main_topic}"},
            {"title": f"Secretos de {main_topic}", "description": f"Trucos poco conocidos sobre {main_topic}"},
            {"title": f"Errores comunes en {main_topic}", "description": f"Qué evitar al hacer {main_topic}"},
            {"title": f"Inspiración para {main_topic}", "description": f"Ideas creativas relacionadas con {main_topic}"}
        ]

def generate_copy(idea: Dict[str, str], context: str) -> Dict[str, Any]:
    """Generate Instagram copy for a specific idea"""
    prompt = f"""
    Crea un copy completo para Instagram basado en esta idea:
    
    Título: {idea['title']}
    Descripción: {idea['description']}
    Contexto: {context}
    
    El copy debe incluir:
    1. Hook inicial (primera línea atractiva, máximo 15 palabras)
    2. Cuerpo del mensaje (desarrollo de la idea, máximo 150 palabras)
    3. Llamada a la acción clara y específica
    4. 3-5 hashtags relevantes
    
    Responde SOLO con JSON válido:
    {{
        "hook": "Hook atractivo aquí",
        "body": "Cuerpo del mensaje desarrollado...",
        "cta": "Llamada a la acción específica",
        "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"]
    }}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        copy_json = json.loads(content)
        return copy_json
    except (json.JSONDecodeError, KeyError, TypeError):
        # Fallback genérico basado en la idea
        import re
        # Determinar hashtags relevantes basados en el contexto
        keywords = re.findall(r'\b\w+\b', context.lower())
        topic_tags = [f"#{word.capitalize()}" for word in keywords[:3] if len(word) > 3]
        generic_tags = ["#Instagram", "#Contenido", "#Tips"]
        hashtags = topic_tags + generic_tags
        
        return {
            "hook": f"✨ ¿Sabías todo esto sobre {idea['title']}?",
            "body": f"{idea['description']}. En este post te comparto información valiosa que te va a ayudar a entender mejor este tema. Es perfecto para aplicar en tu día a día.",
            "cta": "¿Qué opinas? ¡Cuéntame en los comentarios!",
            "hashtags": hashtags[:5]  # Máximo 5 hashtags
        }

def generate_visual_prompt(idea: Dict[str, str], context: str) -> str:
    """Generate visual description for image generation"""
    prompt = f"""
    Crea un prompt descriptivo detallado para generar una imagen que acompañe esta publicación de Instagram:
    
    Título: {idea['title']}
    Descripción: {idea['description']}
    Contexto: {context}
    
    El prompt debe ser específico y incluir:
    - Descripción visual clara de la escena
    - Estilo fotográfico apropiado (fotografía, ilustración, diseño gráfico, etc.)
    - Colores y iluminación adecuados al tema
    - Composición y encuadre
    - Elementos visuales específicos relacionados con el tema
    
    Responde con un prompt de máximo 80 palabras en inglés, optimizado para generación de imágenes.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def generate_image_with_imagen(prompt: str) -> Optional[str]:
    """Generate image using Google's Imagen API"""
    try:
        print(f"Generating image with prompt: {prompt}")
        
        # Try to generate image using the correct Imagen API syntax
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                  response_modalities=['TEXT', 'IMAGE']
                )
            )

            for part in response.candidates[0].content.parts:
              if part.text is not None:
                print(part.text)
              elif part.inline_data is not None:
                import io
                buffer = io.BytesIO()
                generated_image = Image.open(BytesIO((part.inline_data.data)))
                generated_image.save(buffer, format='PNG')
                image_data = buffer.getvalue()
                generated_image.save("generated_image.png")
                print(f"✅ Imagen API generated image successfully: {len(image_data)} bytes")
                return image_data
                
        except Exception as img_error:
            print(f"Imagen API error: {str(img_error)}")
            print("Falling back to placeholder image...")
        
        # Fallback: Generate a placeholder image for testing
        
        # Create a more attractive placeholder image
        img = Image.new('RGB', (512, 512), color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Add a gradient-like effect
        for y in range(512):
            color_val = int(102 + (126 * y / 512))  # Gradient from #667eea to #764ba2
            draw.rectangle([0, y, 512, y+1], fill=(102, color_val, 234))
        
        # Add text with better formatting
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        
        # Split text into lines
        lines = [
            "🎨 AI Generated Image",
            "",
            "Prompt:",
            prompt[:40] + "..." if len(prompt) > 40 else prompt,
            "",
            "📸 Placeholder Image",
            "Real image generation in progress..."
        ]
        
        y_offset = 150
        for line in lines:
            if font:
                draw.text((30, y_offset), line, fill='white', font=font)
            else:
                draw.text((30, y_offset), line, fill='white')
            y_offset += 25
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        print(f"📸 Fallback placeholder generated: {len(img_data)} bytes")
        return img_data
        
    except Exception as e:
        print(f"Error in image generation: {str(e)}")
        return None

# LangGraph Workflow Definition
def create_content_workflow():
    """Create LangGraph workflow for content generation"""
    
    def process_context_node(state: ContentGenerationState) -> ContentGenerationState:
        """Node to process initial context"""
        try:
            # Context is already processed before entering the workflow
            return state
        except Exception as e:
            return {**state, "error": f"Error processing context: {str(e)}"}
    
    def generate_ideas_node(state: ContentGenerationState) -> ContentGenerationState:
        """Node to generate content ideas"""
        try:
            ideas = generate_ideas(state["context"])
            return {**state, "ideas": ideas}
        except Exception as e:
            return {**state, "error": f"Error generating ideas: {str(e)}"}
    
    def generate_posts_node(state: ContentGenerationState) -> ContentGenerationState:
        """Node to generate post copies"""
        try:
            posts = []
            for idea in state["ideas"]:
                copy = generate_copy(idea, state["context"])
                posts.append(copy)
            return {**state, "posts": posts}
        except Exception as e:
            return {**state, "error": f"Error generating posts: {str(e)}"}
    
    def generate_visuals_node(state: ContentGenerationState) -> ContentGenerationState:
        """Node to generate visual prompts and images"""
        try:
            visual_prompts = []
            for idea in state["ideas"]:
                prompt = generate_visual_prompt(idea, state["context"])
                # Generate actual image
                image_data = generate_image_with_imagen(prompt)
                
                visual_data = {
                    "description": prompt,
                    "image_data": image_data
                }
                visual_prompts.append(visual_data)
            return {**state, "visual_prompts": visual_prompts}
        except Exception as e:
            return {**state, "error": f"Error generating visual prompts: {str(e)}"}
    
    # Create workflow graph
    workflow = StateGraph(ContentGenerationState)
    
    # Add nodes
    workflow.add_node("process_context", process_context_node)
    workflow.add_node("generate_ideas", generate_ideas_node)
    workflow.add_node("generate_posts", generate_posts_node)
    workflow.add_node("generate_visuals", generate_visuals_node)
    
    # Define edges
    workflow.set_entry_point("process_context")
    workflow.add_edge("process_context", "generate_ideas")
    workflow.add_edge("generate_ideas", "generate_posts")
    workflow.add_edge("generate_posts", "generate_visuals")
    workflow.add_edge("generate_visuals", END)
    
    return workflow.compile()

# Initialize workflow
content_workflow = create_content_workflow()

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CM Assistant MVP API is running"}

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(
    input_type: str = Form(...),
    content: Optional[str] = Form(None),
    guided_answers: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    """
    Main endpoint to generate Instagram content based on different input types
    """
    try:
        # Process context based on input type
        if input_type == "text" and content:
            context = process_text_context(content)
        elif input_type == "url" and content:
            context = process_url_context(content)
        elif input_type == "image" and image:
            image_data = await image.read()
            context = process_image_context(image_data)
        elif input_type == "guided" and guided_answers:
            answers = json.loads(guided_answers)
            context = process_guided_context(answers)
        else:
            raise HTTPException(status_code=400, detail="Invalid input type or missing content")
        
        # Initialize workflow state
        initial_state: ContentGenerationState = {
            "context": context,
            "ideas": [],
            "posts": [],
            "visual_prompts": [],
            "error": None
        }
        
        # Run workflow
        final_state = content_workflow.invoke(initial_state)
        
        if final_state.get("error"):
            raise HTTPException(status_code=500, detail=final_state["error"])
        
        # Format response
        visual_prompts_formatted = []
        for visual_data in final_state["visual_prompts"]:
            if isinstance(visual_data, dict):
                # Convert image data to base64 URL if available
                image_url = None
                if visual_data.get("image_data"):
                    import base64
                    image_url = f"data:image/png;base64,{base64.b64encode(visual_data['image_data']).decode()}"
                
                visual_prompts_formatted.append(VisualPrompt(
                    description=visual_data.get("description", ""),
                    image_url=image_url
                ))
            else:
                # Fallback for old format
                visual_prompts_formatted.append(VisualPrompt(description=visual_data))
        
        response = ContentResponse(
            ideas=[ContentIdea(**idea) for idea in final_state["ideas"]],
            posts=[PostContent(**post) for post in final_state["posts"]],
            visual_prompts=visual_prompts_formatted,
            context_summary=context
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.get("/api/guided-questions")
async def get_guided_questions():
    """Get guided questionnaire for beginners"""
    questions = {
        "questions": [
            {
                "id": "niche",
                "question": "¿Sobre qué nicho o industria es tu cuenta?",
                "type": "text",
                "placeholder": "Ej: cocina vegana, fitness, tecnología..."
            },
            {
                "id": "objective",
                "question": "¿Cuál es el objetivo de tu próxima publicación?",
                "type": "select",
                "options": ["entretener", "educar", "vender", "inspirar", "informar"]
            },
            {
                "id": "tone",
                "question": "¿Qué tono de voz prefieres?",
                "type": "select",
                "options": ["divertido", "profesional", "inspirador", "casual", "educativo"]
            }
        ]
    }
    return questions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)