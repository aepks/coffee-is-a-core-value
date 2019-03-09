import user
import mysql_connection

active_account = None

# db setup
mysql_connection.gen_users()
mysql_connection.gen_sales()
mysql_connection.gen_parameters_table(0.5, 0.5)
mysql_connection.gen_machine_information()
while True:
    print("Welcome to the program. Please scan your ID.")
    rfid_key = input("> ")
    active_user = user.user(rfid_key)

    print(active_user)

    active_user.purchase("coffee")
    print(active_user)
