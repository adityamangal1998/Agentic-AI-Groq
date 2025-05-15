from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import logging
from colorama import Fore, Style

# Configure logger with tool-specific name
logger = logging.getLogger('agent_logger.calculator')

class CalculatorInput(BaseModel):
    expression: str = Field(description="The math expression to evaluate")

class CalculatorTool(BaseTool):
    name: str = "calculator_tool"
    description: str = "Useful for evaluating simple math expressions like '2 + 2 * 3'."
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            logger.info(f"{Fore.YELLOW}[Calculator Tool] Processing: {expression}{Style.RESET_ALL}")
            expression = expression.strip()
            if not all(char.isdigit() or char in "+-*/(). " for char in expression):
                logger.warning(f"{Fore.RED}Invalid characters in expression: {expression}{Style.RESET_ALL}")
                return "Error: Invalid characters in expression"
            result = eval(expression, {"__builtins__": {}})
            logger.info(f"{Fore.GREEN}Result: {result}{Style.RESET_ALL}")
            return f"The result is {result}"
        except Exception as e:
            logger.error(f"{Fore.RED}Calculator error: {str(e)}{Style.RESET_ALL}", exc_info=True)
            return f"Error: {str(e)}"
