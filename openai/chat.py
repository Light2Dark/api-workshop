import openai

import uvicorn

from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


app = FastAPI()

@app.get("/ai_comments")
async def get_ai_response(prompt: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
    )
    
    return {
        "prompt": prompt,
        "response": response.choices[0].text
    }

if __name__ == "__main__":
    uvicorn.run('chat:app', host="localhost", port=5001, reload=True)