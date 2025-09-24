#!/usr/bin/env python3
"""
Main script demonstrating the WeatherAPIClient usage.
"""

from api_client import WeatherAPIClient


def main():
    """Main function demonstrating API client usage."""
    # Initialize the client
    client = WeatherAPIClient(api_key="demo-key-123")
    
    print("🌤️  Weather API Client Demo")
    print("=" * 40)
    
    # Test API key validation
    print(f"API Key Valid: {client.validate_api_key()}")
    
    # Get current weather for a city
    city = "London"
    current_weather = client.get_current_weather(city)
    print(f"\nCurrent weather in {city}:")
    print(f"Temperature: {current_weather.get('temperature', 'N/A')}°C")
    print(f"Condition: {current_weather.get('condition', 'N/A')}")
    
    # Get forecast
    forecast = client.get_forecast(city, days=3)
    print(f"\n3-day forecast for {city}:")
    if "forecast" in forecast:
        for day in forecast["forecast"]:
            print(f"  {day['date']}: {day['condition']} - {day['temp']}°C")
    else:
        print("  Forecast data not available")
    
    # Get cities in a country
    country = "UK"
    cities = client.get_cities_by_country(country)
    print(f"\nCities in {country}: {', '.join(cities[:5])}{'...' if len(cities) > 5 else ''}")


if __name__ == "__main__":
    main()