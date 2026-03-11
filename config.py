from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SESSION = os.getenv("POESESSID")
    LEAGUE = "Mirage"
    # SEARCH_IDS = ["yYRVXKnqCR", "7ngvw0v2S5", "KlD8yZPgU5"]
    SEARCH_IDS = ["glW8vEvaiQ", 'wvPbmnvBFb', "LgdLY0w2In"]
    # SEARCH_IDS = ["9z2nRpbKfK"]

config = Config()