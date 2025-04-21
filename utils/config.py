import os
from dotenv import load_dotenv
import joblib

# Load .env file
load_dotenv(override=True)

# .env variables
APP_NAME = os.getenv('APP_NAME')
VERSION = os.getenv('VERSION')
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')

# PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_FOLDER_PATH = os.path.join(BASE_DIR, "assets")

# Load Models
preprocessor = joblib.load(os.path.join(ASSETS_FOLDER_PATH, 'preprocessor.pkl'))
forest_model = joblib.load(os.path.join(ASSETS_FOLDER_PATH, 'forest_tuned.pkl'))
xgboost_model = joblib.load(os.path.join(ASSETS_FOLDER_PATH, 'xgb_tuned.pkl'))