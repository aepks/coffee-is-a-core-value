from database import invoice_users, rfid_return_user, fingerprint_return_user
from gpio_interface import display, button_press, activate_led, deactivate_led
from gpio_interface import b1, b2, b3, flash_led
import time
import datetime

while True:
    c_time = datetime.now()
    if c_time.hours == 23:
        invoice_users()
        last_invoice = datetime.now()

    display(f"Press Any Button\nTo Begin   {c_time.hours}:{c_time.minutes}")
    if button_press():
        display("Scan your card\n or fingerprint")
        # somehow both scan for fingerprint and rfid card
        fingerprint_return_user(3)
        user = rfid_return_user(113815)  # jschmitz2 for purpose of testing

    display("Welcome. \nCoffee|Cup|Done")
    activate_led()
    starttime = time.time()
    while user:
        button = button_press()
        if button:
            if button == 0:
                user.purchase("coffee")
                activate_led(b1)
                display(f"Coffee purchased\nBalance: {user.balance()}")
                time.sleep(2)
                deactivate_led(b1)
            elif button == 1:
                user.purchase("cup")
                activate_led(b2)
                display(f"Cup purchased\nBalance: {user.balance()}")
                time.sleep(2)
                deactivate_led(b2)
            else:
                user = None
                display("Logging out.")
                activate_led(b3)
                time.sleep(2)
                deactivate_led(b3)

        if time.time() - starttime > 15:
            display("Logging out\nfrom inactivity")
            user = None
            flash_led()
