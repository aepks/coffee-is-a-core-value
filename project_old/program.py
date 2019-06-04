import user
import mysql_connection

print("""Demo mode
By default, the user logged in is "12345".

Valid commands:
'purchase' - purchases a coffee
'purchase soda' - purchases a soda, but that's pretty second-fiddle.
'refund' - Processes a refund for the user.
'logout' - Logs out of the current account.
'print sales' - Prints full sales data.
'print parameters' - Prints parameters table.
'print machine information' - Prints machine information.
'print users' - Prints the 'users' data.
'print user' - Prints the active user's data.
""")

mysql_connection.init()
active_user = user.user(12345)

while True:
    usr_input = input("> ")

    if usr_input == 'logout':
        print("Please enter your RFID key.")
        active_user = user.user(input("> "))

    elif usr_input == 'purchase':
        active_user.purchase("coffee")

    elif usr_input == 'purchase soda':
        active_user.purchase("soda")

    elif usr_input == 'refund':
        # Do some shit, I don't know
        pass

    elif usr_input == 'print sales':
        for row in mysql_connection.return_sales_data():
            print(row)

    elif usr_input == 'print parameters':
        for row in mysql_connection.return_parameters():
            print(row)

    elif usr_input == 'print machine information':
        for row in mysql_connection.return_machine_information():
            print(row)

    elif usr_input == 'print users':
        for row in mysql_connection.return_users():
            print(row)

    elif usr_input == 'print user':
        for row in mysql_connection.return_user(active_user.rfid_key):
            print(row)
