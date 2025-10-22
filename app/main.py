from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importar los routers
from app.routers import  chat 
# Gemini config
from app.config.genai_client import configure_genai



app = FastAPI(
    title="RAG API",
    version="0.1.0"
)

# Inicializa Gemini al arrancar el servidor
configure_genai()

# Configurar CORS (por ahora abierto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router)



@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API RAG. Visita /docs para ver la documentación interactiva."
    }


