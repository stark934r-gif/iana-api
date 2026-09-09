from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(title="Iana Cloud API", version="1.0")

# Llave secreta para proteger tu servicio en la nube
API_KEY = "tu_clave_secreta_super_segura"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Acceso no autorizado")

class ChatRequest(BaseModel):
    prompt: str
    persona: str = "Ayrton"

@app.get("/")
def home():
    return {"status": "Iana Cloud está activa y operativa"}

@app.post("/chat")
def chat_with_iana(request: ChatRequest, api_key: str = Security(verify_api_key)):
    # Aquí es donde más adelante conectaremos la lógica de Iana
    respuesta = f"[{request.persona} - Cloud]: Recibí tu mensaje: '{request.prompt}'. Todo funcionando correctamente."
    return {"response": respuesta}