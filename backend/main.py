from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import re
from sympy import sympify

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="INEXORA AI")

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found")
client = OpenAI(api_key=api_key)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

class ImageRequest(BaseModel):
    prompt: str

def evaluate_math(expression):
    try:
        expression = expression.replace('x', '*').replace('÷', '/')
        result = float(sympify(expression).evalf())
        return f"The result of {expression} is {result:.2f}"
    except Exception as e:
        logger.error(f"Math error: {str(e)}")
        return "Sorry, I couldn't evaluate that expression."

def is_math_question(text):
    indicators = ["calculate", "solve", "what is", "what's", "equals", "+", "-", "*", "/"]
    return any(i in text.lower() for i in indicators)

@app.get("/")
def root():
    return {"message": "INEXORA AI is running"}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        question = request.question.strip()
        logger.info(f"Question: {question}")

        # Handle math questions
        if is_math_question(question):
            expression = re.sub(r'[^0-9+\-*/().\s]', '', question)
            if expression:
                return {"answer": evaluate_math(expression)}

        # Use OpenAI for other questions
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are INEXORA, a helpful AI assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        
        return {"answer": response.choices[0].message.content}

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {"answer": "I'm having trouble processing your request. Please try again."}

@app.post("/api/generate-image")
def generate_image(request: ImageRequest):
    try:
        logger.info(f"Generating image for prompt: {request.prompt[:50]}...")
        
        # Validate prompt
        if not request.prompt or len(request.prompt.strip()) < 3:
            return JSONResponse(
                status_code=400,
                content={"error": "Please provide a longer image description"}
            )

        # Call DALL-E API
        response = client.images.generate(
            model="dall-e-2",
            prompt=request.prompt,
            n=1,
            size="512x512",
            quality="standard",
            response_format="url"
        )

        # Validate response
        if not response or not hasattr(response, 'data') or not response.data:
            raise ValueError("Invalid response from image API")

        image_url = response.data[0].url
        logger.info("Image generated successfully")
        
        return {
            "success": True,
            "image_url": image_url
        }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Image generation failed: {error_msg}")
        
        if "billing" in error_msg.lower() or "quota" in error_msg.lower():
            return JSONResponse(
                status_code=402,
                content={"error": "Image generation quota exceeded. Please try again later."}
            )
        
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to generate image. Please try again."}
        )

@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"}
    )
