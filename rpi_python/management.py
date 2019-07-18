import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Config:
server = 'localhost'


def logon():
    username = input("Enter your username: \n> ")
    password = input("Enter your password: \n> ")
    try:
        engine = create_engine(
            f'postgresql+psycopg2://{username}{password}@{server}/aepks'
        )
        return engine
    except Exception:
        print("Sorry, that didn't work. Try again.")
        return logon()


class Session:
    def __init__(self):
        self.engine = logon()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def logout(self):
        self.engine.dispose()
        self.session.close_all()

    def view_history(self, username):
        for line in self.search_user(username).full_history(email=False):
            print(line)

    def email_history(self, username):
        self.search_user(username).full_history()

    def export_statistics(self):
        cur_time = datetime.now()
        file = open(f"aepks-export {cur_time.month} - {cur_time.day}.csv")
        for transaction in self.session.query(database.Transaction):
            file.write(
                "{transaction.id},"
                "{transaction.user_id},"
                "{transaction.timestamp},"
                "{transaction.amount},"
            )
        print(f"Exported 'aepks-export {cur_time.month} - {cur_time.day}.csv'")

    # User Related Functions

    def search_user(self, username):
        users = [user for user in self.session.query(database.User).filter_by(
            name=username
        )]
        i = 0
        if len(users) > 1:
            print("Multiple users found.")
            for user in users:
                print(f"User {i}: {user.username}")
            user = input("Which user? \n> ")
        return users[i]

    def add_balance(self, username, amount):
        self.serach_user(username).add_balance(amount)



def main():
    engine = logon()
    Session = sessionmaker(bind=engine)
    session = Session()
