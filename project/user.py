import time
import datetime
from mysql_connection import *



class user:

    def _timestamp(self):
        return time.time()

    def __init__(self, rfid_key):

        self.rfid_key = rfid_key
        self.username = self.gen_user_name()
        self.email_address = self.username + "@hawk.iit.edu"
        self.balance = 0.00
        self.account_type = "user"
        self.soda_price = None
        self.coffee_price = None

    def gen_user_name(self):

        return f"Test User {self.rfid_key}"

    def purchase(self, item):

        price = 0.5 # Temp function: Call to 'parameters' table to check out what the price should be.
        minbal = 0.00 # Call to 'parameters' table to see what 'minbal' should be.
        if (self.balance - price) < minbal:
            return False
        else:
            prev_bal = self.balance
            self.balance -= price

            # Call to 'users' table to update their balance.

            receipt = (self._timestamp(), 'purchase', item, price, prev_bal, self.balance)

            # Call to 'user' table that logs this data.

    def refund(self):

        machine_bills = [] # sql statement
