from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

reponse = client.interactions.create(
    model="gemini-3.8-flash",
    input="Dis bonjour en une phrase"
)

print(reponse.output_text)
