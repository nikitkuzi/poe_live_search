from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SESSION = os.getenv("POESESSID")
    LEAGUE = "Mirage"
    # SEARCH_IDS = ["yYRVXKnqCR", "7ngvw0v2S5", "KlD8yZPgU5"]
    SEARCH_IDS = ["glW8vEvaiQ", 'rPjwmZKMHQ', "LgdLY0w2In", "nrj4lRLyf0", "G6dbmqmZcb", "Lg9j3X5Xfn", "EB6bdkMLC5"]
    # SEARCH_IDS = ["9z2nRpbKfK"]

config = Config()