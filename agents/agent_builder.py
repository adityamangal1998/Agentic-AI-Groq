import logging
from langchain.agents import initialize_agent, AgentType
from langchain_core.runnables import Runnable
from tools.calculator_agent import CalculatorTool
from tools.search_agent import SearchTool
from tools.time_agent import TimeTool
from tools.weather_agent import WeatherTool
from llm.groq_llm import GroqLLM
from agents.output_parser import CustomOutputParser
from utils.callbacks import ToolCallbackHandler
from colorama import Fore, Style

logger = logging.getLogger('agent_logger.builder')

def build_agent() -> Runnable:
    tools = [
        SearchTool(),
        CalculatorTool(),
        TimeTool(),
        WeatherTool()
    ]
    llm = GroqLLM()

    prefix = """You are a helpful AI assistant. You MUST follow these rules:

1. ALWAYS use the provided tools for getting information.
2. NEVER make up or hallucinate responses.
3. If a tool returns an error message starting with [ERROR], you MUST:
   - Stop processing.
   - Return the error message EXACTLY as your Final Answer.
   - Do NOT try to fix or guess information.
4. Only use information from tool responses.
5. Never make assumptions about locations or data not in the tool's database.

Response Format:
Thought: Explain which tool you'll use and why.
Action: [the exact tool name]
Action Input: [the exact input for the tool]
Observation: [the exact tool response]
Final Answer: [use the EXACT tool response]

Example with error:
Human: What time is it in Mars?
Assistant: 
Thought: I need to check the time using time_tool.
Action: time_tool
Action Input: mars
Observation: [ERROR] LOCATION_NOT_FOUND: 'mars' is not a supported location. Available locations: ...
Final Answer: [ERROR] LOCATION_NOT_FOUND: 'mars' is not a supported location. Available locations: ...

Example with success:
Human: What time is it in London?
Assistant: 
Thought: I need to check the time using time_tool.
Action: time_tool
Action Input: London
Observation: [SUCCESS] Current time in London: 03:30:00 PM BST
Final Answer: [SUCCESS] Current time in London: 03:30:00 PM BST

Begin! Remember: NO making up responses, ONLY use tool outputs."""

    callback_handler = ToolCallbackHandler()
    logger.info("Initializing agent with callback handler")
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        callbacks=[callback_handler],  # Add callback handler
        max_iterations=1,  # Set to 1 to prevent multiple attempts
        early_stopping_method="force",
        handle_parsing_errors=False,
        agent_kwargs={
            "prefix": prefix,
            "output_parser": CustomOutputParser(),
            "metadata": {"name": "Agent Chain"}  # Add metadata for callbacks
        }
    )
    logger.debug("Agent initialized successfully")
    print(f"\n{Fore.GREEN}[Agent]{Style.RESET_ALL} Agent initialized with tools: {[tool.name for tool in tools]}\n")
    return agent
