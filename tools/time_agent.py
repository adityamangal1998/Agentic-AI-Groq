from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict
from datetime import datetime
import pytz
import logging
from colorama import Fore, Style
# Configure logger with proper level
logger = logging.getLogger('agent_logger.time_tool')
logger.setLevel(logging.INFO)  # Set to INFO to ensure visibility

# Force print function for debugging
def debug_print(msg: str):
    print(f"\n{Fore.YELLOW}[TimeTool Debug]{Style.RESET_ALL} {msg}")

class TimeInput(BaseModel):
    location: str = Field(description="The location (country/city) to get time for")


class TimeTool(BaseTool):
    name: str = "time_tool"
    description: str = "Get current time for any location (e.g., 'India', 'New York', 'London')"
    args_schema: Type[BaseModel] = TimeInput
    # Mapping of common locations to their timezones
    TIMEZONE_MAP: Dict[str, str] = {
        "india": "Asia/Kolkata",
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
        "dubai": "Asia/Dubai",
        "singapore": "Asia/Singapore",
        "hong kong": "Asia/Hong_Kong",
        "moscow": "Europe/Moscow"
    }

    # City to timezone mapping
    CITY_MAP: Dict[str, str] = {
        "pune": "Asia/Kolkata",
        "mumbai": "Asia/Kolkata",
        "delhi": "Asia/Kolkata",
        "bangalore": "Asia/Kolkata",
        "chennai": "Asia/Kolkata",
        "kolkata": "Asia/Kolkata",
        "hyderabad": "Asia/Kolkata",
    }

    def _get_timezone(self, location: str) -> str:
        location = location.lower().strip()
        if location in self.TIMEZONE_MAP:
            return self.TIMEZONE_MAP[location]
        if location in self.CITY_MAP:
            return self.CITY_MAP[location]
        
        raise ValueError(f"[ERROR] LOCATION_NOT_FOUND: '{location}' is not a supported location. "
                        f"Available locations: {', '.join(sorted(set(list(self.TIMEZONE_MAP.keys()) + list(self.CITY_MAP.keys()))))}")


    def _run(self, location: str) -> str:
        return "[TimeTool] This tool is currently disabled for testing purposes. Please check back later."
        # try:
        #     print(f"\n{Fore.CYAN}[TimeTool] Processing request for: {location}{Style.RESET_ALL}")
        #     timezone_str = self._get_timezone(location)
            
        #     if not timezone_str:
        #         all_locations = sorted(set(list(self.TIMEZONE_MAP.keys()) + list(self.CITY_MAP.keys())))
        #         error_msg = (f"[ERROR] LOCATION_NOT_FOUND: '{location}' is not a supported location. "
        #                    f"Available locations: {', '.join(all_locations)}")
        #         print(f"{Fore.RED}[TimeTool] {error_msg}{Style.RESET_ALL}")
        #         return error_msg

        #     tz = pytz.timezone(timezone_str)
        #     current_time = datetime.now(tz)
        #     result = f"[SUCCESS] Current time in {location.title()}: {current_time.strftime('%I:%M:%S %p %Z')}"
        #     print(f"{Fore.GREEN}[TimeTool] {result}{Style.RESET_ALL}")
        #     return result
            
        # except Exception as e:
        #     error_msg = f"[ERROR] PROCESSING_ERROR: {str(e)}"
        #     print(f"{Fore.RED}[TimeTool] {error_msg}{Style.RESET_ALL}")
        #     return error_msg
