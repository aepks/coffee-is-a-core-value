import time
import mysql_connection

class user:

    def _timestamp(self):
        return time.time()

    def __init__(self, rfid_key):

        data = mysql_connection.logon(rfid_key)

        self.rfid_key = data[0]
        self.user_name = data[1]
        self.email_address = data[2]
        self.balance = data[3]
        self.account_type = data[4]
        self.active = data[7]

        self.prices = {"coffee": data[5], "soda": data[6]}

        for k in self.prices:
            if not self.prices[k]:
                self.prices[k] = mysql_connection.get_price(k)

    def purchase(self, item):

        if self.active:
            mysql_connection.log_sale(round(time.time()), self.rfid_key, item, self.prices[item])
            data = mysql_connection.logon(self.rfid_key)
            self.balance = data[3]
            return True
        else:
            return False

    def __repr__(self):
        outstring = f"""\nrfid_key: {self.rfid_key}
        \nuser_name: {self.user_name}
        \nemail_address: {self.email_address}
        \nbalance: {self.balance}
        \naccount_type: {self.account_type}
        \nactive: {bool(self.active)}
        \nprices: {self.prices}"""
        return outstring
