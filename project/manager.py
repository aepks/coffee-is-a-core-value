import user
import mysql_connection

mysql_connection.init()

def rfid_key_email_pairing():
    needed_users = mysql_connection.hawkString_output()

    hawkStrings = []
    print(needed_users)
    for row in needed_users:
        print(f"RFID key: {row[0]}")
        hawkStrings.append([row[0], input("> ")])

    mysql_connection.hawkString_input(hawkStrings)

def update_price():


    print("If you're not updating an item's price, just hit enter.")

    print("What is the new coffee price?")
    coffee_price = float(input("> "))
    print("What is the new soda price?")
    soda_price = float(input("> "))

    if coffee_price:
        mysql_connection.update_parameters_table("coffee", coffee_price)
    if soda_price:
        mysql_connection.update_parameters_table("soda", soda_price)

rfid_key_email_pairing()
update_price()
