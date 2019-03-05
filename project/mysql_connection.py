import mysql.connector
import time

db = mysql.connector.connect(host='localhost', user='aepks', passwd = 'aepks')
c = db.cursor()

# Parameters Table:

def gen_parameters_table(coffee_price, soda_price, min_bal):

    c.execute("CREATE TABLE parameters VALUES (coffee_price FLOAT, price FLOAT)")

    a = [("coffee", coffee_price), ("soda", soda_price), ("min_bal", min_bal)]

    for x in a: c.execute("INSERT INTO parameters (?, ?)", x)

def update_parameters_table(item, newval):

    c.execute("UPDATE parameters SET price = ? WHERE item = ?", (item, newval))

def get_price(item):

    return (c.execute("SELECT * FROM parameters WHERE item = ?", (item,)))[1]

# Machine Information Table:


def gen_machine_information():

    c.execute("CREATE TABLE machine_information VALUES (timestamp TEXT, balance FLOAT, soda_sold INT, coffee_sold INT)")
    c.execute("INSERT INTO machine_information (?, 0.00, 0, 0)", (time.time(),))

def get_balance():

    for row in c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC"):
        return row[1]
        break

def get_sales_in_daterange(item, start_date, end_date):
    pass
