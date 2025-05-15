from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict
from datetime import datetime
import logging

logger = logging.getLogger('agent_logger')

class WeatherInput(BaseModel):
    location: str = Field(description="The city or location to get weather for")

class WeatherTool(BaseTool):
    name: str = "weather_tool"
    description: str = "Get current weather for cities worldwide (simulated data)"
    args_schema: Type[BaseModel] = WeatherInput

    # Mapping of locations to their weather data
    WEATHER_DATA: Dict[str, Dict[str, str]] = {
        "new delhi": {
            "temp": "28°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "details": "Typical pre-monsoon weather"
        },
        "mumbai": {
            "temp": "32°C",
            "condition": "Humid",
            "humidity": "80%",
            "details": "Coastal weather with high humidity"
        },
        "bangalore": {
            "temp": "24°C",
            "condition": "Pleasant",
            "humidity": "55%",
            "details": "Mild temperatures due to elevation"
        },
        "new york": {
            "temp": "72°F (22°C)",
            "condition": "Sunny",
            "humidity": "45%",
            "details": "Clear skies"
        },
    }

    def _run(self, location: str) -> str:
        try:
            # Normalize input
            location_key = location.lower().strip()
            logger.debug(f"Weather request for location: {location_key}")
            print(f"location_key : {location_key}")
            # Handle "india" as a general query
            if location_key.lower() == "india":
                logger.info("Providing weather for major Indian cities")
                print(f"location_key : {location_key}")
                return ("Weather across major Indian cities:\n"
                        "New Delhi: 28°C, Partly Cloudy\n"
                        "Mumbai: 32°C, Humid\n"
                        "Bangalore: 24°C, Pleasant")
            
            # Get weather for specific city
            weather = self.WEATHER_DATA.get(location_key)
            if weather:
                logger.info(f"Found weather data for {location_key}")
                return (f"Weather in {location.title()}:\n"
                        f"Temperature: {weather['temp']}\n"
                        f"Condition: {weather['condition']}\n"
                        f"Humidity: {weather['humidity']}\n"
                        f"Details: {weather['details']}")
            
            logger.warning(f"Location not found: {location_key}")
            return f"Location not found. Available cities: {', '.join(city.title() for city in self.WEATHER_DATA.keys())}"
        except Exception as e:
            logger.error(f"Error in WeatherTool: {str(e)}")
            return f"Error getting weather: {str(e)}"
