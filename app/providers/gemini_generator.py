import google.generativeai as genai
from app.config.settings import GEMINI_API_KEY
# Proveedor para generación de texto usando Gemini
class GeminiGenerator:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.5-pro")

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()
