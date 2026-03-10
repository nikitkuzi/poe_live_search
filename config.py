from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SESSION = os.getenv("POESESSID")
    LEAGUE = "Mirage"
    SEARCH_IDS = ["G6ldpmvYUb"]

config = Config()