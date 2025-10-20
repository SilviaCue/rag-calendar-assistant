RAG Comercial Inteligente - Asistente Técnico-Comercial de Productos Siemens

Este proyecto implementa un sistema completo RAG (Retrieval Augmented Generation) orientado al análisis técnico-comercial de productos eléctricos de baja tensión, utilizando como base los catálogos oficiales de Siemens.

El sistema permite consultar, comparar y analizar productos (por ejemplo, interruptores automáticos, fusibles, relés, unidades de disparo, etc.), así como detectar nuevas referencias, cambios de precios o características, mediante búsqueda semántica y generación contextual con IA.

Está diseñado para apoyar a equipos comerciales, distribuidores o técnicos de preventa, respondiendo en lenguaje natural a preguntas como:

“¿Qué diferencia hay entre el interruptor 3VA y el 3WA?”
“¿Qué modelo tiene mayor poder de corte a 500 V AC?”
“¿Qué unidad de disparo incluye comunicación Profinet?”
---

### Tecnologías usadas
- FastAPI (backend principal)
- FAISS (almacenamiento vectorial)
- HuggingFace sentence-transformers y Gemini (embeddings)
- Gemini API 1.5 Pro (generación de texto)
- PyMuPDF, python-docx, pandas (lectura de PDF, Word, Excel)
- pytesseract (OCR integrado para PDFs escaneados e imágenes)
- Google Calendar (consulta y cálculo automático de vacaciones, creación de eventos)
- Sistema de notificaciones en Calendar:
- Email inmediato al crear un evento (forzado con MailApp.sendEmail)
- Recordatorio automático 24 h antes del evento
- Swagger UI para documentación interactiva

> Nota: El código tiene preparado soporte para OpenAI (embeddings/generación) y para futuros cambios de modelo, pero actualmente NO está en uso (ni requiere clave API de OpenAI).

---

### Estructura del proyecto
```
idearium_rag_fastapi/
├── app/
│   ├── admin/
│   ├── config/
│   ├── models/
│   ├── providers/
│   ├── routers/
│   └── services/
├── storage/
│   ├── docs_raw/
│   ├── docs_chunks/
│   └── vector_index/
├── secret_keys.json
├── main.py
├── requirements.txt
└── README.md
```

---

### Flujo de trabajo

#### Carga de documentos
- Se colocan en `storage/docs_raw/`
- Soporte: PDF, DOCX, XLS/XLSX, MD, imágenes
- El endpoint `/upload-all/` procesa y trocea todos los documentos (soporta subcarpetas)
- OCR automático si el documento no tiene texto (PDF escaneado, imágenes)

#### Indexado semántico
- El texto extraído se convierte en embeddings usando Gemini o HuggingFace
- Se almacena en FAISS junto a metadatos de origen

#### Consultas
El endpoint /chat/ permite preguntas en lenguaje natural como:
“¿Qué diferencia hay entre los interruptores 3VA y 3WA?”
“¿Qué fusible cubre aplicaciones de 500V?”
“¿Qué modelos admiten comunicación Modbus o Profinet?”

Recupera los fragmentos más relevantes del catálogo Siemens y genera una respuesta contextualizada (por defecto Gemini 1.5 Pro)

Permite también crear alertas automáticas o eventos en Google Calendar cuando se detectan nuevas referencias, bajadas de precio o lanzamientos:

"Crea una alerta si hay nuevos productos en el catálogo de baja tensión"
"Avísame si hay un cambio en la gama 3VA"

Endpoints disponibles para gestión documental y consultas:
/upload-one/ → Subir y procesar un único documento (PDF/DOCX).
/upload-multiple/ → Subir y procesar varios documentos en lote.
/download/{filename} → Descargar un documento original desde storage/docs_raw/.
/chat/ → Consultas técnicas o comerciales sobre productos Siemens (catálogos, comparativas, alertas, calendario).


#### Integración directa con Google Calendar
- Consulta de eventos existentes: vacaciones, reuniones, festivos, entregas, sprints
- Filtros dinámicos: día, semana, mes, próximo evento
- Creación automática de eventos:
  - **Título sugerido por IA** (el usuario puede **confirmarlo o cambiarlo** antes de crear)
  - **Confirmación en dos pasos**:
    1) Propuesta inicial con fecha/hora y **título sugerido**  
    2) **Confirmación final** para crear (`ok`, `vale`, `sí`, `confirmo`, `crear`, `crea`)
  - **Invitados**:
    - Se añaden automáticamente los definidos en `ALERT_EMAILS` (archivo `secret_keys.json`)
    - El usuario puede **añadir o quitar** invitados por email en cualquier momento:
      - `añade: persona@ejemplo.com, otra@ejemplo.com`
      - `quita: persona@ejemplo.com`
  - Email inmediato al crear
  - Recordatorio 24 h antes (automático en Calendar)


#### Consultas técnicas y comparativas
El sistema puede analizar catálogos de productos en formato texto o imagen y responder a preguntas en lenguaje natural, combinando información textual con diagramas, tablas o fotografías de producto.
Gracias al módulo Gemini Multimodal, también interpreta etiquetas, logotipos, símbolos eléctricos o tablas técnicas incluidas en los catálogos.

Ejemplos de consultas posibles:

“¿Cuál es la corriente nominal del 3VA1163?”
“¿Qué interruptor sustituye al modelo 3VL?”
“¿Qué gamas cubren hasta 1000 A?”
“¿Qué diferencias visuales hay entre el 3VA y el 3WA en el catálogo?”
“Identifica el tipo de bornas o conexiones que aparecen en la imagen de la página 42.”

Además, el asistente permite comparar familias de producto, identificar cambios de diseño o funciones entre versiones, y sugerir equivalentes técnicos o comerciales según aplicación o rango de tensión.


---

### Ejecución del proyecto

**Instalar dependencias:**
```
pip install -r requirements.txt
```

**Configurar claves API:**
Crear el archivo `secret_keys.json`:
```json
{
  "GEMINI_API_KEY": "tu_clave_gemini",
  "HUGGINGFACE_API_KEY": "tu_clave_huggingface",
  "usar_google_sheets": false,
  "usar_google_calendar": true,
  "usar_excel_local": false,
  "ALERT_EMAILS": ["tu_email@empresa.com"]
}
```
No es necesario poner la clave OpenAI salvo que quieras probar la integración en el futuro.
ALERT_EMAILS: lista de correos que recibirán siempre la invitación inmediata al crear un evento.

**Arrancar FastAPI:**
```
uvicorn app.main:app --reload
```

**Acceso a Swagger UI:**
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Funcionalidades destacadas (2025)
- **Soporte multiformato**: PDF, Word, Excel, Markdown, imágenes (con OCR).
- **Carga masiva**: `/upload-all/` soporta carpetas y subcarpetas.
- **Onboarding inteligente**: emails de bienvenida generados solo con el manual interno.
- **Gestión de vacaciones avanzada**:
  - Integración en tiempo real con Google Calendar
  - Consulta por persona y año
  - Filtros por día, semana, mes
- **Gestión de calendario extendida**:
  - Categorías: vacaciones, reuniones, festivos, entregas, sprints
  - Creación de reuniones/eventos directamente desde preguntas en lenguaje natural
  - Notificación inmediata por email + recordatorio 24 h antes
- **Consultas RAG seguras**:
  - Respuestas naturales, contextuales y basadas únicamente en documentos internos
  - Cero invención de datos
- **Embeddings configurables**: Gemini o HuggingFace
- **Selector dinámico de modelo generador** (fácil cambio futuro)
- **OCR automático** (requiere Tesseract instalado en Windows/Linux)

#### Gestión y limpieza de índice vectorial:
```
python -m app.admin.reset_vector_store
```

---

### Consideraciones actuales
- **El sistema NO usa OpenAI por defecto** → Gemini es el modelo activo.
- **Para la creación de eventos necesitas**:
  - Calendar compartido o propio donde el script tenga permisos de edición
  - Configurar `ALERT_EMAILS` en `secret_keys.json`
  - El correo inmediato lo envía **MailApp** desde Google Apps Script
  - El recordatorio 24h lo gestiona **Google Calendar**
- **Requiere instalación de Tesseract OCR** en Windows/Linux  
  - [Descargar aquí](https://github.com/tesseract-ocr/tesseract)
