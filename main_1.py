from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool, Tool
from langchain_core.language_models import BaseLanguageModel
from langchain_core.callbacks import CallbackManager
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import Runnable
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage
from typing import Optional, List, Any, Dict, Union
import requests

from pydantic import BaseModel, Field
from langchain_core.language_models import BaseLanguageModel

# === GROQ API CONFIG ===
GROQ_API_KEY = ""
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

# === LLM Class Using GROQ ===
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

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        result = response.json()

        return result['choices'][0]['message']['content']

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

# === Tools Using @tool Decorator ===

@tool
def search_tool(query: str) -> str:
    """Search for general knowledge topics like capital cities or people."""
    responses = {
        "capital of France": "The capital of France is Paris.",
        "Einstein": "Albert Einstein was a theoretical physicist known for the theory of relativity."
    }
    for key in responses:
        if key.lower() in query.lower():
            return responses[key]
    return "Sorry, I couldn't find an answer to that."


@tool
def calculator_tool(expression: str) -> str:
    """Evaluate basic math expressions such as 5 + 3 or 12 * 7."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"The result is {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# === Agent Setup ===

def build_agent() -> Runnable:
    # Define LangChain Tools
    tools = [
        Tool.from_function(
            func=search_tool,
            name="search_tool",
            description="Useful for answering factual queries like 'capital of France' or information about people like 'Einstein'."
        ),
        Tool.from_function(
            func=calculator_tool,
            name="calculator_tool",
            description="Useful for evaluating simple math expressions like '2 + 2 * 3'."
        )
    ]

    # Custom LLM wrapper
    llm = GroqLLM()

    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent

# === Main App ===

if __name__ == "__main__":
    agent = build_agent()
    print("🤖 Welcome to the LangChain + GROQ Agent!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Farewell, noble seeker of knowledge!")
            break

        try:
            result = agent.invoke(user_input)
            print(f"Agent: {result}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
