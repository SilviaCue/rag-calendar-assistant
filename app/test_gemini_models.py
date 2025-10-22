import google.generativeai as genai
from app.config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Listar los modelos disponibles
modelos = genai.list_models()

for m in modelos:
    print(m.name)
