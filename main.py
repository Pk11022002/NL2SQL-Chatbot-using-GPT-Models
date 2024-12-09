from langchain_community.utilities import SQLDatabase
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os 

load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")

password = quote_plus(db_password)
db = SQLDatabase.from_uri(f"mysql+mysqlconnector://{db_user}:{password}@{db_host}/{db_name}")
print(db.dialect)
# print(db.get_usable_table_names())
# # db.run("SELECT * FROM Artist LIMIT 10;")