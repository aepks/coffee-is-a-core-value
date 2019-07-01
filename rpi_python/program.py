from database import *
from gpio_interface import *
import time
import datetime

while True:
    current_datetime = datetime.now()
    if current_datetime.hours == 23:
        invoice_users()
        last_invoice = datetime.now()

    display(f"Press Any Button\nTo Begin   {current_datetime.hours}:{current_datetime.minutes}")
    if button_press():
        display("Scan your card\n or fingerprint")
        # somehow both scan for fingerprint and rfid card
        user = rfid_return_user(113815) # jschmitz2 for purpose of testing

    display("Welcome. \nCoffee|Cup|Done")
    activate_led()
    startime = time.time()
    while user:
        button = button_press()
        if button:
            if button = 0:
                user.purchase("coffee")
                activate_led(b1)
                display(f"Coffee purchased\nBalance: {user.balance()}")
            elif button 1:
                user.purchase("cup")
                activate_led(b2)
                display(f"Cup purchased\nBalance: {user.balance()}")
            else:
                user = None
                display("Logging out.")
                activate_led(b3)

        if time.time() - starttime > 15:
            display("Logging out\nfrom inactivity")
            user = None
            flash_led()
