# 🚀 Asistente de Community Manager - MVP

Una aplicación web completa que automatiza la creación y curación de contenido para Instagram utilizando IA generativa con **Gemini**, **LangChain**, **LangGraph** y **FastAPI**.

## 📋 Características Principales

### 🎯 Generación de Contenido Basada en Contexto (RAG)
- **Entrada por texto**: Palabras clave o temas específicos
- **Análisis de URL**: Perfiles de Instagram o páginas web para analizar estilo
- **Procesamiento de imágenes**: Descripción automática usando Gemini Vision
- **Modo guiado**: Cuestionario para principiantes

### ✨ Funcionalidades de IA
- **5 ideas creativas** para publicaciones de Instagram
- **Copy completo** con gancho, cuerpo, CTA y hashtags
- **Prompts descriptivos** para generación de imágenes
- **Contexto inteligente** usando RAG con LangChain

## 🏗️ Arquitectura Técnica

### Backend
- **FastAPI**: Framework web rápido y moderno
- **Gemini API**: Modelo de IA generativa de Google
- **LangChain**: Orquestación de flujos de IA
- **LangGraph**: Gestión de workflows complejos
- **Python 3.8+**: Lenguaje base

### Frontend
- **HTML5 + CSS3**: Estructura y estilos responsivos
- **JavaScript Vanilla**: Lógica del cliente sin frameworks
- **Diseño responsive**: Optimizado para móviles y desktop

## 📁 Estructura del Proyecto

```
cm_assistant_mvp/
├── backend/
│   ├── main.py              # API FastAPI + integración LangChain/Gemini
│   └── requirements.txt     # Dependencias de Python
├── frontend/
│   ├── index.html          # Interfaz de usuario
│   ├── script.js           # Lógica del frontend
│   └── style.css           # Estilos responsivos
└── README.md               # Documentación del proyecto
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Clave API de Google Gemini

### Paso 1: Clonar el Proyecto
```bash
git clone <url-del-repositorio>
cd cm_assistant_mvp
```

### Paso 2: Configurar el Backend

1. **Navegar al directorio backend**:
```bash
cd backend
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv

# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:

Crear un archivo `.env` en el directorio `backend/`:
```bash
touch .env
```

Agregar tu clave API de Gemini:
```env
GEMINI_API_KEY=tu_clave_api_de_gemini_aqui
```

### Paso 3: Obtener Clave API de Gemini

1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva clave API
3. Copia la clave y agrégala al archivo `.env`

### Paso 4: Ejecutar el Backend

```bash
# Desde el directorio backend/
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor se ejecutará en: `http://localhost:8000`

### Paso 5: Abrir el Frontend

1. **Navegar al directorio frontend**:
```bash
cd ../frontend
```

2. **Abrir con un servidor local** (recomendado):

Opción A - Python (si tienes Python instalado):
```bash
# Python 3
python -m http.server 3000

# Python 2
python -m SimpleHTTPServer 3000
```

Opción B - Node.js (si tienes Node.js instalado):
```bash
npx serve -s . -l 3000
```

Opción C - Abrir directamente:
```bash
# Abrir index.html en tu navegador
open index.html  # Mac
start index.html # Windows
xdg-open index.html # Linux
```

3. **Acceder a la aplicación**:
Abre tu navegador y ve a: `http://localhost:3000`

## 🎮 Uso de la Aplicación

### 1. Seleccionar Tipo de Entrada

#### 📝 Modo Texto
- Ingresa un tema o palabra clave
- Ejemplo: "recetas veganas fáciles para principiantes"

#### 🔗 Modo URL
- Pega la URL de un perfil de Instagram o página web
- La IA analizará el estilo y contenido

#### 🖼️ Modo Imagen
- Sube una imagen (JPG, PNG, etc.)
- La IA describirá la imagen y generará contenido relacionado

#### 🎯 Modo Guiado
- Responde 3 preguntas simples:
  - Nicho o industria
  - Objetivo de la publicación
  - Tono de voz preferido

### 2. Generar Contenido

1. Completa la información según el modo seleccionado
2. Haz clic en "✨ Generar Contenido"
3. Espera mientras la IA procesa tu solicitud

### 3. Revisar Resultados

La aplicación generará:

- **📋 Resumen del contexto**: Análisis de tu entrada
- **💡 5 ideas creativas**: Títulos y descripciones para posts
- **✍️ Posts completos**: Copy con gancho, cuerpo, CTA y hashtags
- **🎨 Prompts para imágenes**: Descripciones para generar visuales

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales

```env
# Archivo .env en backend/
GEMINI_API_KEY=tu_clave_api_aqui
LANGSMITH_API_KEY=tu_clave_langsmith  # Opcional para debugging
LANGSMITH_TRACING=true                # Opcional para trazabilidad
```

### Personalización del Modelo

En `backend/main.py`, puedes ajustar:

```python
# Cambiar modelo de Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # o "gemini-pro-vision"
    google_api_key=GEMINI_API_KEY,
    temperature=0.7      # Creatividad (0.0 - 1.0)
)
```

## 🧪 Testing y Desarrollo

### Verificar la Instalación

1. **Backend**:
```bash
curl http://localhost:8000/
# Debería responder: {"message": "CM Assistant MVP API is running"}
```

2. **Frontend**:
Abre el navegador y verifica que la interfaz se carga correctamente.

### Debugging

#### Backend
- Los logs aparecen en la consola donde ejecutaste `python main.py`
- Usa el endpoint `/docs` para la documentación automática de la API: `http://localhost:8000/docs`

#### Frontend
- Abre las Herramientas de Desarrollador (F12)
- Revisa la consola para errores JavaScript
- Verifica la pestaña Network para errores de API

### Estructura de Respuesta de la API

```json
{
  "ideas": [
    {
      "title": "Título de la idea",
      "description": "Descripción breve"
    }
  ],
  "posts": [
    {
      "hook": "Gancho atractivo",
      "body": "Cuerpo del mensaje",
      "cta": "Llamada a la acción",
      "hashtags": ["#hashtag1", "#hashtag2"]
    }
  ],
  "visual_prompts": [
    {
      "description": "Prompt descriptivo para imagen"
    }
  ],
  "context_summary": "Resumen del contexto analizado"
}
```

## 🐛 Solución de Problemas

### Error: "GEMINI_API_KEY environment variable is required"
- **Solución**: Verifica que el archivo `.env` existe y contiene la clave API correcta.

### Error: "ModuleNotFoundError"
- **Solución**: Asegúrate de tener el entorno virtual activado y ejecuta `pip install -r requirements.txt`.

### Error de CORS en el frontend
- **Solución**: Asegúrate de ejecutar el frontend en un servidor local, no abriendo el archivo HTML directamente.

### La aplicación no se conecta al backend
- **Solución**: Verifica que el backend esté ejecutándose en `http://localhost:8000` y que no haya conflictos de puertos.

### Error: "API quota exceeded"
- **Solución**: Verifica los límites de tu clave API de Gemini en Google AI Studio.

## 🚀 Mejoras Futuras

### Funcionalidades Adicionales
- [ ] Programación de publicaciones
- [ ] Análisis de competencia
- [ ] Métricas de engagement
- [ ] Integración con APIs de redes sociales
- [ ] Generación de imágenes con IA
- [ ] Modo colaborativo para equipos

### Optimizaciones Técnicas
- [ ] Cache de respuestas
- [ ] Base de datos para historial
- [ ] Autenticación de usuarios
- [ ] Rate limiting
- [ ] Docker containerization
- [ ] Deploy en la nube

## 📚 Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Guía de LangChain](https://python.langchain.com/)
- [API de Gemini](https://ai.google.dev/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.

## ⭐ Reconocimientos

- **Google Gemini** por el modelo de IA generativa
- **LangChain** por la orquestación de workflows
- **FastAPI** por el framework web robusto
- **Anthropic Claude** por la asistencia en el desarrollo

---

**¡Desarrollado con ❤️ para Community Managers!**

Si tienes preguntas o necesitas ayuda, abre un issue en el repositorio.