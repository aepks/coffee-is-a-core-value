import mysql.connector
import time

db = mysql.connector.connect(host='localhost', user='aepks', passwd = 'aepks', auth_plugin='mysql_native_password')
c = db.cursor(buffered=True)

def fire(): # Destorys and rebuilds database.

    c.execute("DROP DATABASE aepks_accounts")
def init():
    try:
        c.execute("USE aepks_accounts")
    except:
        c.execute("CREATE DATABASE aepks_accounts")
        c.execute("USE aepks_accounts")
        gen_users()
        gen_sales()
        gen_parameters_table(0.5, 0.5)
        gen_machine_information()


# Parameters Table:

def gen_parameters_table(coffee_price, soda_price): # tested and working

    c.execute("CREATE TABLE parameters (item VARCHAR(20), price FLOAT)")

    a = [("coffee", coffee_price), ("soda", soda_price)]

    for x in a:
        c.execute("INSERT INTO parameters (item, price) VALUES (%s, %s)", x)

    db.commit()

def update_parameters_table(item, newval): # tested working

    c.execute("UPDATE parameters SET price = %s WHERE item = %s", (newval, item))

    db.commit()

def get_price(item):

    c.execute("SELECT * FROM parameters WHERE item = %s", (item,))
    for row in c:
        return row[1] # tested working

    db.commit()

# Machine Information Table:

def gen_machine_information(): # tested working

    c.execute("CREATE TABLE machine_information (timestamp DOUBLE, balance FLOAT, soda_sold INT, coffee_sold INT)")
    c.execute("INSERT INTO machine_information (timestamp, balance, soda_sold, coffee_sold) VALUES (%s, %s, %s, %s)", (round(time.time()), 0.00, 0, 0))

    db.commit()

def get_total_sales(): # tested maybe working? as long as it returns the most recent one

    c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC")
    for row in c:
        return row[1]
        break

    db.commit()

def gen_sales(): # tested working
    c.execute("CREATE TABLE sales (timestamp DOUBLE, rfid_key INT, item VARCHAR(20), price FLOAT)")

    db.commit()

def get_sales_in_daterange(start_seconds, end_seconds): # tested working (probably)
    c.execute("SELECT * FROM sales WHERE timestamp BETWEEN %s AND %s ", (start_seconds, end_seconds))
    sales = []
    for row in c:
        sales.append(row)
    return sales

def update_machine_balance(bal_change, soda_sold=0, coffee_sold=0): # tested working
    c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC LIMIT 1")
    for row in c:
        vals = (round(time.time()), row[1] + bal_change, row[2] + soda_sold, row[3] + coffee_sold,)
        # prev_bal = row[1]
        # prev_soda = row[2]
        # prev_coffee = row[3]
        break
    c.execute("""INSERT INTO machine_information (timestamp, balance, soda_sold, coffee_sold) VALUES (%s, %s, %s, %s)""", vals)

    db.commit()

def gen_users(): # tested working

    c.execute("""CREATE TABLE users (rfid_key INTEGER, user_name VARCHAR(30), email_address VARCHAR(30), balance FLOAT,
    account_type VARCHAR(10), soda_price FLOAT, coffee_price FLOAT, active TINYINT(1))""")

    db.commit()

def return_sales_data(): # tested working
    c.execute("SELECT * FROM sales")
    return [row for row in c]

def return_parameters():
    c.execute("SELECT * FROM parameters")
    return [row for row in c]

def return_machine_information():
    c.execute("SELECT * FROM machine_information ORDER BY timestamp DESC")
    return [row for row in c]

def return_users():
    c.execute("SELECT * FROM users")
    return [row for row in c]

def return_user(rfid_key): # This might not work.

    c.execute(f"SELECT * FROM rfid_id_{rfid_key}")
    return [row for row in c]


# Important functions!!!

def gen_user_account(time, rfid_key): # tested working

    user_name = "null" # Placeholder
    email_address = "null" # Placeholder
    balance = 0.00
    account_type = 'user'
    soda_price = None
    coffee_price = None
    active = 1

    c.execute("""INSERT INTO users (rfid_key, user_name, email_address, balance, account_type, soda_price, coffee_price, active) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s)""", (rfid_key, user_name, email_address, balance, account_type, soda_price, coffee_price, active,))

    c.execute(f"CREATE TABLE rfid_id_{rfid_key} (timestamp DOUBLE, action VARCHAR(20), item VARCHAR(20), amount FLOAT, cur_bal FLOAT)")

    db.commit()

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

    db.commit()

def logon(rfid_key):

    c.execute("SELECT * FROM users WHERE rfid_key = %s", (rfid_key,))
    a = []
    for x in c:
        if x:
            return [val for val in x]
    else:
        gen_user_account(round(time.time()), rfid_key)
        c.execute("SELECT * FROM users WHERE rfid_key = %s", (rfid_key,))
        for x in c:
            return [val for val in x]

 # Hawk ID Email Finding, working

def hawkString_output():
    c.execute("SELECT * FROM users WHERE user_name = %s ORDER BY rfid_key DESC", ("null",))
    return [row for row in c]

def hawkString_input(data):
    for row in data:
        c.execute("UPDATE users SET user_name = %s WHERE rfid_key = %s", (row[1], row[0]))
        c.execute("UPDATE users SET email_address = %s WHERE rfid_key = %s",(row[1] + "@hawk.iit.edu", row[0]))

    db.commit()
