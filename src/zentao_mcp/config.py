"""Configuration management for Zentao MCP"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load .env file when module is imported
load_dotenv()


@dataclass
class ZentaoConfig:
    """Zentao connection configuration"""
    base_url: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls) -> "ZentaoConfig":
        """Load configuration from environment variables"""
        return cls(
            base_url=os.getenv("ZENTAO_BASE_URL", ""),
            username=os.getenv("ZENTAO_USERNAME", ""),
            password=os.getenv("ZENTAO_PASSWORD", ""),
        )
    
    def is_valid(self) -> bool:
        """Check if all required fields are set"""
        return all([self.base_url, self.username, self.password])
