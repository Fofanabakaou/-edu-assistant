from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    texte: str

@app.get("/")
def read_root():
    return {"message": "edu-assistant est en ligne"}

@app.post("/ask")
def poser_question(question: Question):
    return {"question_recue": question.texte}
