from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from typing import Union
import re

class CustomOutputParser(AgentOutputParser):
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        # Check for final answer first
        if "Final Answer:" in text:
            final_answer = text.split("Final Answer:")[-1].strip()
            return AgentFinish(return_values={"output": final_answer}, log=text)
        # Parse out action and action input
        action_match = re.search(r'Action: (.*?)[\n]', text)
        input_match = re.search(r'Action Input: (.*?)[\n]', text)
        if action_match and input_match:
            action = action_match.group(1).strip()
            action_input = input_match.group(1).strip()
            return AgentAction(tool=action, tool_input=action_input, log=text)
        # If no action or input found, treat as final answer
        return AgentFinish(return_values={"output": text.strip()}, log=text)
