from agents.agent_builder import build_agent
from dotenv import load_dotenv
from utils.logger import setup_logger
import logging
import colorama
from colorama import Fore, Style
import sys

# Initialize colorama and logger
colorama.init()
logger = setup_logger()

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Use ASCII alternative if Unicode not supported
    robot_emoji = '🤖' if sys.stdout.encoding.lower() == 'utf-8' else '[BOT]'
    
    logger.info(f"{Fore.GREEN}{robot_emoji} Starting AI Agent System{Style.RESET_ALL}")
    agent = build_agent()
    logger.info(f"{Fore.CYAN}🤖 Welcome to the LangChain + GROQ Agent!{Style.RESET_ALL}")
    logger.info("Type 'exit' to quit.\n")
    while True:
        user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
        if user_input.lower() in ["exit", "quit"]:
            logger.info(f"{Fore.YELLOW}👋 Farewell, noble seeker of knowledge!{Style.RESET_ALL}")
            break
        try:
            logger.info(f"{Fore.BLUE}New Query: {user_input}{Style.RESET_ALL}")
            result = agent.invoke(user_input)
            if isinstance(result, dict):
                answer = result.get('output', str(result))
                logger.info(f"{Fore.CYAN}Agent: {answer.strip()}\n{Style.RESET_ALL}")
            else:
                logger.info(f"{Fore.CYAN}Agent: {str(result).strip()}\n{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}", exc_info=True)
