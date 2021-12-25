import os 
from dotenv.main import load_dotenv 
from pyairtable import Table

load_dotenv()
api_key = os.getenv("ATTOKEN")
base_id = os.getenv("BASEID")

# Create a new record
table = Table(api_key, base_id, "Tele-bot")

def create_record(user_data):
    table.create(user_data)