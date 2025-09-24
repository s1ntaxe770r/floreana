import requests
from typing import Dict, List, Optional


class WeatherAPIClient:
    """A fictional weather API client for demonstration purposes."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.weather.example.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def get_current_weather(self, city: str) -> Dict:
        """Get current weather for a city."""
        url = f"{self.base_url}/current"
        params = {"city": city}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "city": city}
    
    def get_forecast(self, city: str, days: int = 5) -> Dict:
        """Get weather forecast for a city."""
        url = f"{self.base_url}/forecast"
        params = {"city": city, "days": days}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "city": city, "days": days}
    
    def get_cities_by_country(self, country: str) -> List[str]:
        """Get list of cities in a country."""
        url = f"{self.base_url}/cities"
        params = {"country": country}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("cities", [])
    k   except requests.RequestException:
            return []
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working."""
        url = f"{self.base_url}/validate"
        
        try:
            response = self.session.get(url)
            return response.status_code == 200
        except requests.RequestException:
            return False
