from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

load_dotenv()

app = FastAPI()
client = genai.Client()

reader = PdfReader("cours/presentation-unix-lect01.pdf")
contenu_cours = ""
for page in reader.pages:
    contenu_cours += page.extract_text()

class Question(BaseModel):
    texte: str

@app.get("/")
def read_root():
    return {"message": "edu-assistant est en ligne"}

@app.post("/ask")
def poser_question(question: Question):
    instructions = (
        "Tu es un assistant pedagogique. Reponds toujours en francais, "
        "meme si le cours source est dans une autre langue. "
        "Base ta reponse uniquement sur le contenu du cours fourni ci-dessous. "
        "Ne donne jamais directement une reponse finale sans exercice : "
        "explique la notion, puis propose systematiquement un petit exercice pratique "
        "pour que l'etudiant applique ce qu'il vient d'apprendre."
    )

    prompt = f"{instructions}\n\nContenu du cours:\n{contenu_cours}\n\nQuestion de l'etudiant:\n{question.texte}"

    reponse = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return {"reponse": reponse.output_text}
