# Calendar Asistent  
### Asistente inteligente para gestión de calendario con FastAPI y Gemini

Este proyecto implementa un **asistente de calendario inteligente** que permite **consultar y crear eventos en Google Calendar** mediante **lenguaje natural**, utilizando **FastAPI** como backend y **Gemini 1.5 Pro** para interpretar las peticiones del usuario.

El sistema entiende frases como:  
- “Crea una reunión con Marta mañana a las 10”  
- “Muéstrame mis vacaciones de este mes”  
- “¿Cuándo es la próxima entrega del proyecto?”  

y gestiona automáticamente los eventos en el calendario vinculado.

---

### Características principales
- **Integración directa con Google Calendar**  
  - Consulta de reuniones, vacaciones, entregas o festivos  
  - Filtros por día, semana, mes o próximo evento  
  - Creación de eventos desde texto natural  
- **Gemini 1.5 Pro**  
  - Reformulación y comprensión de instrucciones  
  - Generación de respuestas naturales y confirmaciones  
- **Confirmación en dos pasos**  
  - Propuesta inicial del evento  
  - Confirmación del usuario antes de crear  
- **Gestión de invitados**  
  - Invitados automáticos definidos en `ALERT_EMAILS`  
  - Añadir o quitar invitados manualmente en la conversación  
- **Notificaciones automáticas**  
  - Email inmediato al crear (vía Apps Script)  
  - Recordatorio 24 h antes (Google Calendar)

---

### Tecnologías utilizadas
- **FastAPI** — Backend principal  
- **Gemini 1.5 Pro API** — Comprensión y generación de texto  
- **Google Calendar API** — Gestión de eventos  
- **MailApp (Apps Script)** — Envío inmediato de correos  
- **Swagger UI** — Documentación interactiva  

---

### Estructura del proyecto
calendar_asistent/
├── app/
│ ├── config/
│ ├── providers/
│ ├── routers/
│ │ └── chat.py
│ ├── services/
│ └── utils/
├── secret_keys.json
├── main.py
├── requirements.txt
└── README.md

yaml
Copiar código

---

### Configuración inicial

#### 1. Instalar dependencias
```bash
pip install -r requirements.txt
2. Crear archivo secret_keys.json
json
Copiar código
{
  "GEMINI_API_KEY": "tu_clave_gemini",
  "usar_google_calendar": true,
  "ALERT_EMAILS": ["tu_email@empresa.com"]
}
3. Iniciar el servidor FastAPI
bash
Copiar código
uvicorn app.main:app --reload
4. Acceder a la documentación interactiva
http://127.0.0.1:8000/docs

Flujo de trabajo
Interpretación de la intención
Gemini analiza la frase y detecta si el usuario quiere consultar o crear un evento.

Confirmación previa
El sistema propone un resumen del evento antes de crearlo, esperando una respuesta del usuario (ok, vale, crear, etc.).

Creación y notificación

El evento se crea en Google Calendar

Se envía un email inmediato (MailApp)

Se programa recordatorio 24 h antes

Endpoint principal
Endpoint	Descripción
/chat/	Interfaz principal de conversación en lenguaje natural

Ejemplos de uso
Consulta:

“¿Qué tengo programado mañana?”
“¿Cuándo es la próxima reunión con Diego?”

Creación:

“Crea una reunión con Marta el jueves a las 9:30.”
“Programa una entrega para el 25 de octubre a las 12.”

Consideraciones
Requiere permisos de edición sobre el calendario configurado.

Las notificaciones por email se envían desde Apps Script asociado.

Gemini es el modelo activo (OpenAI no está en uso).

Configuración simple y centralizada en secret_keys.json.