# Frontend React - CM Assistant MVP

## Instalación y Setup

### Prerrequisitos
- Node.js (versión 16 o superior)
- npm o yarn

### Instalación
```bash
# Navegar al directorio
cd frontend-react

# Instalar dependencias
npm install

# Iniciar en modo desarrollo
npm start
```

La aplicación se abrirá en `http://localhost:3000`

### Dependencias principales
- **React 18**: Framework principal
- **Swiper**: Carrusel avanzado con soporte para touch/swipe
- **Axios**: Cliente HTTP para las llamadas a la API

## Características

### ✅ Carrusel Robusto
- **Swiper.js**: Biblioteca profesional para carruseles
- **Touch/Swipe**: Soporte nativo para móviles
- **Navegación**: Flechas y puntos indicadores
- **Responsive**: Optimizado para todas las pantallas

### ✅ Gestión de Estado
- **React Hooks**: useState para manejo de estado local
- **Validación**: Validación robusta de formularios
- **Error Handling**: Manejo de errores elegante

### ✅ Componentes Modulares
- **InputSection**: Manejo de todos los tipos de entrada
- **PostsCarousel**: Carrusel con Swiper
- **InstagramPost**: Componente individual de post
- **LoadingSection**: Estado de carga
- **ErrorSection**: Manejo de errores

## Estructura

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── InputSection.js
│   │   ├── LoadingSection.js
│   │   ├── ResultsSection.js
│   │   ├── PostsCarousel.js
│   │   ├── InstagramPost.js
│   │   └── ErrorSection.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Mejoras vs Vanilla JS

1. **Carrusel Robusto**: Swiper.js ofrece mejor funcionalidad que implementaciones manuales
2. **Estado Reactivo**: React maneja actualizaciones de UI automáticamente
3. **Componentes Reutilizables**: Código más organizado y mantenible
4. **Touch/Swipe Nativo**: Mejor experiencia en móviles
5. **Performance**: Renderizado optimizado de React

## API Integration

El frontend se conecta con la API backend en `http://localhost:8000`:
- `POST /api/generate-content`: Genera contenido completo
- Manejo automático de FormData para uploads de imágenes
- Gestión de estados de carga y error

## Desarrollo

```bash
# Modo desarrollo con hot reload
npm start

# Build para producción
npm run build
```

## Características Específicas

### Carrusel de Posts
- Cada post tiene su imagen generada integrada
- Prompt de imagen visible como "alt text"
- Navegación fluida entre posts
- Indicadores de posición

### Responsividad
- Diseño móvil-first
- Carrusel optimizado para touch
- Interfaces adaptativas según dispositivo

### Integración con Backend
- Soporte para las nuevas API keys separadas
- Generación de imágenes con Imagen API
- Contexto limpio sin markdown artifacts