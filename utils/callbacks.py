from langchain.callbacks.base import BaseCallbackHandler
from colorama import Fore, Style

class ToolCallbackHandler(BaseCallbackHandler):
    def _get_safe_value(self, obj: dict, key: str, default: str = "Unknown") -> str:
        """Safely get value from dictionary"""
        if not obj or not isinstance(obj, dict):
            return default
        return obj.get(key, default)

    def on_chain_start(self, serialized: dict, inputs: dict, **kwargs) -> None:
        chain_name = self._get_safe_value(serialized, 'name')
        print(f"\n{Fore.BLUE}[Chain Started] {chain_name}{Style.RESET_ALL}")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        tool_name = self._get_safe_value(serialized, 'name')
        print(f"\n{Fore.YELLOW}[Tool] {tool_name} - Input: {input_str}{Style.RESET_ALL}")

    def on_tool_end(self, output: str, **kwargs) -> None:
        print(f"{Fore.GREEN}[Tool Output] {output}{Style.RESET_ALL}")

    def on_tool_error(self, error: str, **kwargs) -> None:
        print(f"{Fore.RED}[Tool Error] {error}{Style.RESET_ALL}")
