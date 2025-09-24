"""
Unit tests for the WeatherAPIClient using pytest.
"""

import pytest
from unittest.mock import Mock, patch
import requests
from api_client import WeatherAPIClient


class TestWeatherAPIClient:
    """Test cases for WeatherAPIClient."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.client = WeatherAPIClient(api_key="test-key")
    
    def test_client_initialization(self):
        """Test that client initializes correctly."""
        assert self.client.api_key == "test-key"
        assert self.client.base_url == "https://api.weather.example.com"
        assert "Authorization" in self.client.session.headers
    
    def test_client_initialization_custom_url(self):
        """Test client initialization with custom URL."""
        client = WeatherAPIClient(api_key="test-key", base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"
    
    @patch('api_client.requests.Session.get')
    def test_get_current_weather_success(self, mock_get):
        """Test successful current weather request."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "temperature": 22,
            "condition": "Sunny",
            "city": "London"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.get_current_weather("London")
        
        assert result["temperature"] == 22
        assert result["condition"] == "Sunny"
        mock_get.assert_called_once()
    
    @patch('api_client.requests.Session.get')
    def test_get_current_weather_error(self, mock_get):
        """Test current weather request with error."""
        # Mock error response
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = self.client.get_current_weather("London")
        
        assert "error" in result
        assert result["city"] == "London"
    
    @patch('api_client.requests.Session.get')
    def test_get_forecast_success(self, mock_get):
        """Test successful forecast request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "forecast": [
                {"date": "2024-01-01", "condition": "Sunny", "temp": 25},
                {"date": "2024-01-02", "condition": "Cloudy", "temp": 20}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.get_forecast("London", days=2)
        
        assert len(result["forecast"]) == 2
        assert result["forecast"][0]["condition"] == "Sunny"
    
    @patch('api_client.requests.Session.get')
    def test_get_cities_by_country_success(self, mock_get):
        """Test successful cities request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "cities": ["London", "Manchester", "Birmingham"]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.client.get_cities_by_country("UK")
        
        assert len(result) == 3
        assert "London" in result
    
    @patch('api_client.requests.Session.get')
    def test_get_cities_by_country_error(self, mock_get):
        """Test cities request with error."""
        mock_get.side_effect = requests.RequestException("API error")
        
        result = self.client.get_cities_by_country("UK")
        
        assert result == []
    
    @patch('api_client.requests.Session.get')
    def test_validate_api_key_success(self, mock_get):
        """Test successful API key validation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.client.validate_api_key()
        
        assert result is True
    
    @patch('api_client.requests.Session.get')
    def test_validate_api_key_failure(self, mock_get):
        """Test API key validation failure."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        result = self.client.validate_api_key()
        
        assert result is False
    
    @patch('api_client.requests.Session.get')
    def test_validate_api_key_exception(self, mock_get):
        """Test API key validation with exception."""
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = self.client.validate_api_key()
        
        assert result is False


# Parametrized test example
@pytest.mark.parametrize("city,expected_temp", [
    ("London", 22),
    ("Paris", 18),
    ("Tokyo", 25),
])
@patch('api_client.requests.Session.get')
def test_multiple_cities_weather(mock_get, city, expected_temp):
    """Test weather for multiple cities using parametrized test."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "temperature": expected_temp,
        "condition": "Sunny",
        "city": city
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    client = WeatherAPIClient(api_key="test-key")
    result = client.get_current_weather(city)
    
    assert result["temperature"] == expected_temp
    assert result["city"] == city