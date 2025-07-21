import os
import re
import mistune
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

# Lấy API Key từ biến môi trường
GEMINI_API_KEY = "AIzaSyAUMkuhN4KxQQoOCWd6bX0rsuIBP0fGNBE"

# Khởi tạo client Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

class SEORequest(BaseModel):
    prompt: str  # Nhận dữ liệu từ body JSON

@app.post("/generate-seo-article/")
async def generate_seo_article(request: SEORequest):
    try:
        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=request.prompt)],
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
        )
        
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text
        
        markdown_renderer = mistune.create_markdown(renderer=mistune.HTMLRenderer())
        html_content = markdown_renderer(response_text)
        content=html_content
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))