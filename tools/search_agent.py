from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Type

class SearchInput(BaseModel):
    query: str = Field(description="The search query string")

class SearchTool(BaseTool):
    name: str = "search_tool"
    description: str = "Useful for answering factual queries like 'capital of France' or information about people like 'Einstein'."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        responses: Dict[str, str] = {
            "capital of France": "The capital of France is Paris.",
            "Einstein": "Albert Einstein was a theoretical physicist known for the theory of relativity."
        }
        for key in responses:
            if key.lower() in query.lower():
                return responses[key]
        return "Sorry, I couldn't find an answer to that."
