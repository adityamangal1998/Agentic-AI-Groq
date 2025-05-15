import logging
import sys
from datetime import datetime
import os
from colorama import Fore, Style

class ForceLogger(logging.Logger):
    def _log(self, level, msg, args, **kwargs):
        if level >= self.getEffectiveLevel():
            print(f"{msg % args}")  # Force print output
        super()._log(level, msg, args, **kwargs)

def setup_logger():
    # Register custom logger class
    logging.setLoggerClass(ForceLogger)
    
    # Create base logger
    logger = logging.getLogger('agent_logger')
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Console handler setup
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    # File handler setup
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.FileHandler(
        f'logs/agent_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)
    
    # Ensure propagation
    logger.propagate = True
    
    return logger
