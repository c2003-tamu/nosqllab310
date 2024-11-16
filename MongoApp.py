import pymongo
from dotenv import load_dotenv
import os


class MongoApp:
    def __init__(self):
        load_dotenv()
        db_password = os.getenv("DB_PASSWORD")
        db_username = os.getenv("DB_USERNAME")
        connection_string = os.getenv("CONNECTION_STRING")

        print(f"db_password = {db_password}")
        print(f"db_username = {db_username}")
        print(f"connection_string = {connection_string}")

        if not db_password or not db_username or not connection_string:
            raise ValueError("One or multiple .env variables not found!")

        mongodb_connection_string = f"mongodb+srv://{
            db_username}:{db_password}@{connection_string}"

        print(f"mongodb_connection_string = {mongodb_connection_string}")

        self.client = pymongo.MongoClient(mongodb_connection_string)
        self.db = self.client['Votes']

    def get_all_candidates(self):
        try:
            candidates = list(self.db.candidates.find(
                {}, {"_id": 0, "candidateName": 1}))
            return [candidate['candidateName'] for candidate in candidates]
        except Exception as e:
            print(f"Error fetching candidates: {e}")
        return

    def has_id_voted(self, id):
        try:
            voters = list(self.db.ballots.find({}, {"_id": 0, "voterID": 1}))
            voter_ids = [voter['voterID'] for voter in voters]
            return (id in voter_ids)
        except Exception as e:
            print(f"Error fetching votes: {e}")
        return

    def post_ballot(self, voterID, regPIN, firstChoice, secondChoice, thirdChoice):
        try:
            ballot = {
                "voterID": voterID,
                "regPIN": regPIN,
                "firstChoice": firstChoice,
                "secondChoice": secondChoice,
                "thirdChoice": thirdChoice
            }
            self.db.ballots.insert_one(ballot)
        except Exception as e:
            print(f"Error posting ballot: {e}")
        return
