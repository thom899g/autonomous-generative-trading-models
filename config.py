"""
Configuration management for the Autonomous Generative Trading System.
Centralizes all environment variables, constants, and configuration settings.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    type: str = os.getenv("FIREBASE_TYPE", "service_account")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    private_key_id: str = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")
    private_key: str = os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n')
    client_email: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    client_id: str = os.getenv("FIREBASE_CLIENT_ID", "")
    auth_uri: str = os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
    token_uri: str = os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token")
    auth_provider_x509_cert_url: str = os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs")
    client_x509_cert_url: str = os.getenv("FIREBASE_CLIENT_CERT_URL", "")
    universe_domain: str = os.getenv("FIREBASE_UNIVERSE_DOMAIN", "googleapis.com")

@dataclass
class TradingConfig:
    """Trading system configuration"""
    # Exchange configuration
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    
    # Trading parameters
    initial_capital: float = float(os.getenv("INITIAL_CAPITAL", "10000.0"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.02"))
    max_open_positions: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    
    # Timeframes
    data_timeframes: list = ["1m", "5m", "15m", "1h", "4h", "1d"]
    backtest_period_days: int = int(os.getenv("BACKTEST_PERIOD_DAYS", "30"))
    
    # Symbols to trade
    trading_symbols: list = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT"]

@dataclass
class GeneticConfig:
    """Genetic algorithm configuration"""
    population_size: int = int(os.getenv("POPULATION_SIZE", "50"))
    generations: int = int(os.getenv("GENERATIONS", "100"))
    mutation_rate: float = float(os.getenv("MUTATION_RATE", "0.1"))
    crossover_rate: float = float(os.getenv("CROSSOVER_RATE", "0.7"))
    elite_size: int = int(os.getenv("ELITE_SIZE", "5"))
    strategy_complexity_range: tuple = (3, 10)  # Min/max indicators per strategy

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = os.getenv("LOG_FILE", "trading_system.log")

class Config:
    """Main configuration class"""
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.genetic = GeneticConfig()
        self.logging = LoggingConfig()
        
        # Validate critical configurations
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical configuration values"""
        if not self.firebase.project_id:
            raise ValueError("FIREBASE_PROJECT_ID must be set in environment variables")
        
        if not self.trading.api_key or not self.trading.api_secret:
            raise ValueError("Exchange API credentials must be set")

# Global configuration instance
config = Config()