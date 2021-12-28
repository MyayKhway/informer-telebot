import os 
from dotenv.main import load_dotenv 
from pyairtable import Table

load_dotenv()
api_key = os.getenv("ATTOKEN")
base_id = os.getenv("BASEID")
table = os.getenv("TABLENAME")

# Create a new record
table = Table(api_key, base_id, table)

def create_record(user_data):
    table.create(user_data)