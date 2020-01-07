from pathlib import Path  # python3 only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

API_TOKEN = os.getenv("BITLY_TOKEN")
