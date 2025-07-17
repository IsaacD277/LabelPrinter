import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Initialize API base URL and headers
    CONNECTWISE_BASE_URL = os.environ.get('CONNECTWISE_BASE_URL', 'http://na.myconnectwise.net/v4_6_release/apis/3.0')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    LOGIN_COMPANY = os.environ.get('LOGIN_COMPANY')
    PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

    # Initialize base directory for templates
    BASE_DIR = os.environ.get('BASE_DIR', os.path.dirname(os.path.abspath(__file__)))

    @classmethod
    def validate_config(cls):
        required_vars = ['CLIENT_ID', 'LOGIN_COMPANY', 'PUBLIC_KEY', 'PRIVATE_KEY']
        missing = [var for var in required_vars if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
