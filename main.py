from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# MODELOS
class Result(BaseModel):
    video_id: str
    results: dict


# MOCK DATABASE (temporário)
MOCK_DATA = {}


# ROTAS
@app.post("/upload")
async def upload_video(file: UploadFile = File(None)):
    """
    Rota mockada. Gera um video_id e salva dados mockados.
    """
    video_id = str(uuid.uuid4())

    # gerar dados falsos das 16 ferramentas
    MOCK_DATA[video_id] = {
        "pontuacao_geral": 77,
        "qualidade": "Boa",
        "tools": {
            "sorat_core": "Texto otimizado…",
            "sentimento": "Neutro",
            "keyframes": ["frame1", "frame2"],
            "audio": "Claro",
            "ritmo": "Bom",
            # … e assim por diante
        },
    }

    return {"video_id": video_id, "status": "processing"}


@app.get("/result/{video_id}")
async def get_result(video_id: str):
    """
    Retorna os dados mockados das 16 ferramentas.
    """
    if video_id not in MOCK_DATA:
        raise HTTPException(status_code=404, detail="Video_id não encontrado")

    return MOCK_DATA[video_id]


@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    """
    Responde OPTIONS corretamente para CORS.
    """
    return {"status": "ok"}
