from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult
from typing import Optional, List, Any, Dict, Union
from pydantic import BaseModel, Field
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = os.getenv("GROQ_API_URL", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "")

class GroqLLM(BaseLanguageModel):
    model: str = Field(default=GROQ_MODEL)
    api_key: str = Field(default=GROQ_API_KEY)
    def _call(self, messages: List[dict], stop=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
        }
        for attempt in range(5):  # Retry up to 5 times
            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=payload)
                if response.status_code == 429:  # Handle rate limiting
                    retry_after = int(response.headers.get("Retry-After", 1))
                    time.sleep(retry_after)
                    continue
                response.raise_for_status()  # Raise an error for HTTP issues
                result = response.json()

                # Validate response structure
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    raise ValueError("Invalid response structure from GROQ API.")
            except (requests.RequestException, ValueError) as e:
                if attempt == 4:  # On the last attempt, raise the error
                    return f"Error: {str(e)}"
                time.sleep(2 ** attempt)  # Exponential backoff

    def invoke(self, prompt: Union[str, Any], stop: Optional[List[str]] = None) -> str:
        # Handle prompt input as a string
        if not isinstance(prompt, str):
            prompt = str(prompt)

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        return self._call(messages)

    def predict(self, text: Union[str, Any], stop: Optional[List[str]] = None) -> str:
        return self.invoke(text, stop)

    def predict_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> BaseMessage:
        content = self._call([{"role": msg.type, "content": msg.content} for msg in messages], stop)
        return BaseMessage(type="assistant", content=content)

    def generate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> LLMResult:
        results = [self.invoke(prompt, stop) for prompt in prompts]
        return LLMResult(generations=[[{"text": result}] for result in results])

    def agenerate_prompt(self, *args, **kwargs):
        raise NotImplementedError("Async methods are not implemented.")

    def apredict(self, *args, **kwargs):
        raise NotImplementedError("Async methods are not implemented.")

    def apredict_messages(self, *args, **kwargs):
        raise NotImplementedError("Async methods are not implemented.")
