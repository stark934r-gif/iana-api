from google import genai
from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI(title="Iana Cloud API", version="1.0")

client = genai.Client(api_key="GEMINI_API_KEY")

API_KEY = "tu_clave_secreta_super_segura"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Acceso no autorizado")

class ChatRequest(BaseModel):
    prompt: str
    persona: str = "Iana"

@app.post("/chat")
def chat_with_iana(request: ChatRequest, api_key: str = Security(verify_api_key)):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=request.prompt,
        config={
            "system_instruction": f"Eres {request.persona}, un asistente virtual inteligente, amigable y directo. Responde siempre en español."
        }
    )
    return {"response": response.text}

# Monta los archivos estáticos para que lea tu index.html (asegúrate de tener una carpeta o los archivos en la raíz)
app.mount("/", StaticFiles(directory=".", html=True), name="static")
