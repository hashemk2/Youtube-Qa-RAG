from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.backEnd.model import generateAnswer
from app.backEnd.database import SessionLocal, QueryAnswer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify frontend origin for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder for CSS
app.mount("/static", StaticFiles(directory="/home/hashem/Projects/YouTube Transcript QA RAG System/app/frontEnd/static"), name="static")

# Templates
templates = Jinja2Templates(directory="/home/hashem/Projects/YouTube Transcript QA RAG System/app/frontEnd/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": ""})

@app.post("/ask")
async def ask_question(request: Request):
    try:
        db = SessionLocal()
        data = await request.json()
        video_url = data.get("video_url") 
        question = data.get("question")
        answer = generateAnswer(video_url, question)

        db_entry = QueryAnswer(
            video_url=video_url,
            question=question,
            answer=answer
        )
        db.add(db_entry)
        db.commit()
    except Exception as e: 
        answer = f"Error: {e}"
    finally:
        db.close()
    
    return JSONResponse({"answer": answer})