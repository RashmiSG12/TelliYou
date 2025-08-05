from langchain.llms.base import LLM
from typing import Optional, List
import os
import google.generativeai as genai
from pydantic import Field, PrivateAttr
from dotenv import load_dotenv

# Step 1: Load the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # If gemini.py is in a subfolder, load from parent
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class GeminiLLM(LLM):
    api_key: Optional[str] = Field(default=None)
    model_name: str = Field(default="gemini-2.0-flash")
    
    _model: genai.GenerativeModel = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = self.api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(self.model_name)
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._model.generate_content(contents=prompt)
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            text_parts = [part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')]
            text = "".join(text_parts)
            return text
        else:
            return ""

    @property
    def _llm_type(self) -> str:
        return "gemini"
