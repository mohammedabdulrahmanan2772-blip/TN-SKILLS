import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# API and Model Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# Server Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_URL = os.getenv("BACKEND_URL", f"http://localhost:{BACKEND_PORT}")

# Asset Paths
IMAGE_DIR = os.path.join(BASE_DIR, "image")
LOGO_PATH = os.path.join(IMAGE_DIR, "Logo.png")
INVERSE_LOGO_PATH = os.path.join(IMAGE_DIR, "inverseLogo.png")
