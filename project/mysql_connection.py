import mysql.connector
import time

db = mysql.connector.connect(host='localhost', user='aepks', passwd = 'aepks', auth_plugin='mysql_native_password')
c = db.cursor()

c.execute("DROP DATABASE aepks_accounts")
try:
    c.execute("USE aepks_accounts")
except:
    c.execute("CREATE DATABASE aepks_accounts")
    c.execute("USE aepks_accounts")

# Parameters Table:

def gen_parameters_table(coffee_price, soda_price): # tested and working

    c.execute("CREATE TABLE parameters (item VARCHAR(20), price FLOAT)")

    a = [("coffee", coffee_price), ("soda", soda_price)]

    for x in a:
        c.execute("INSERT INTO parameters (item, price) VALUES (%s, %s)", x)

def update_parameters_table(item, newval): # tested working

    c.execute("UPDATE parameters SET price = %s WHERE item = %s", (newval, item))

def get_price(item):

    c.execute("SELECT * FROM parameters WHERE item = %s", (item,))
    for row in c:
        return row[1] # tested working

# Machine Information Table:

def gen_machine_information(): # tested working

    c.execute("CREATE TABLE machine_information (timestamp DOUBLE, balance FLOAT, soda_sold INT, coffee_sold INT)")
    c.execute("INSERT INTO machine_information (timestamp, balance, soda_sold, coffee_sold) VALUES (%s, %s, %s, %s)", (time.time(), 0.00, 0, 0))

def get_total_sales(): # tested maybe working? as long as it returns the most recent one

    c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC")
    for row in c:
        return row[1]
        break

def gen_sales(): # tested working
    c.execute("CREATE TABLE sales (timestamp DOUBLE, rfid_key INT, item VARCHAR(20), price FLOAT)")

def get_sales_in_daterange(start_seconds, end_seconds): # tested working (probably)
    c.execute("SELECT * FROM sales WHERE timestamp BETWEEN %s AND %s ", (start_seconds, end_seconds))
    sales = []
    for row in c:
        sales.append(row)
    return sales

def update_machine_balance(bal_change, soda_sold=0, coffee_sold=0):
    c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC")
    for row in c:
        prev_bal = row[1]
        prev_soda = row[2]
        prev_coffee = row[3]
        break
    new_bal = prev_bal + bal_change

    c.execute("""INSERT INTO machine_information (timestamp, balance, soda_sold, coffee_sold) VALUES
    (%s, %s, %s, %s)""", (time.time(), new_bal, (prev_soda + soda_sold), (prev_coffee + coffee_sold)))

def gen_users():

    c.execute("""CREATE TABLE users (rfid_key INTEGER, user_name VARCHAR(30), email_address VARCHAR(30), balance FLOAT,
    account_type VARCHAR(10), soda_price FLOAT, coffee_price FLOAT, active TINYINT(1))""")

def pp():
    c.execute("SELECT * FROM sales")
    for row in c: print(row)

# Important functions!!!

def gen_user_account(time, rfid_key): # tested working

    user_name = None # Placeholder
    email_address = None # Placeholder
    balance = 0.00
    account_type = 'user'
    soda_price = None
    coffee_price = None
    active = 1

    c.execute("""INSERT INTO users (rfid_key, user_name, email_address, balance, account_type, soda_price, coffee_price, active) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)""", (rfid_key, user_name, email_address, balance, account_type, soda_price, coffee_price, active,))

    c.execute(f"CREATE TABLE rfid_id_{rfid_key} (timestamp DOUBLE, action VARCHAR(20), item VARCHAR(20), amount FLOAT, cur_bal FLOAT)")

def log_sale(time, rfid_key, item, price):

    c.execute("INSERT INTO sales (timestamp, rfid_key, item, price) VALUES (%s, %s, %s, %s)", (time, rfid_key, item, price))

    c.execute(f"SELECT cur_bal FROM rfid_id_{rfid_key} ORDER BY timestamp DESC")
    prev_bal = 0
    for row in c:
        prev_bal = row[0]
        break

    cur_bal = prev_bal - price
    c.execute(f"""INSERT INTO rfid_id_{rfid_key} (timestamp, action, item,
    amount, cur_bal) VALUES (%s, %s, %s, %s, %s)""", (time, "purchase", item,  price, cur_bal))

    c.execute("UPDATE users SET balance = %s WHERE rfid_key = %s", (cur_bal, rfid_key))

    if item == "coffee":
        update_machine_balance(price, 0, 1)
    elif item == "soda":
        update_machine_balance(price, 1, 0)

def logon(rfid_key):

    c.execute("SELECT * FROM users WHERE rfid_key = %s", (rfid_key,))
    a = []
    for x in c:
        if x:
            return [val for val in x]
    else:
        gen_user_account(time.time(), rfid_key)
        c.execute("SELECT * FROM users WHERE rfid_key = %s", (rfid_key,))
        for x in c:
            return [val for val in x]
