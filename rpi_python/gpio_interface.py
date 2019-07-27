from gpiozero import LED, Button
# import adafruit_character_lcd.character_lcd as characterlcd
import board
import time
import digitalio

#
# lcd_columns = 16
# lcd_rows = 2
#
# b1 = Button(18)
# l1 = LED(23)
# b2 = Button(24)
# l2 = LED(25)
# b3 = Button(8)
# l3 = LED(7)
#
# button_led = {b1: l1, b2: l2, b3: l3}
# buttons = [b1, b2, b3]
# leds = [l1, l2, l3]
#
# lcd_rs = digitalio.DigitalInOut(board.D2)  # Pin 4
# lcd_en = digitalio.DigitalInOut(board.D5)  # Pin 6
# lcd_d7 = digitalio.DigitalInOut(board.D22)  # Pin 14
# lcd_d6 = digitalio.DigitalInOut(board.D27)  # Pin 13
# lcd_d5 = digitalio.DigitalInOut(board.D17)  # Pin 12
# lcd_d4 = digitalio.DigitalInOut(board.D4)  # Pin 11
#
# lcd = characterlcd.Character_LCD_Mono(
#     lcd_rs,
#     lcd_en,
#     lcd_d4,
#     lcd_d5,
#     lcd_d6,
#     lcd_d7,
#     lcd_columns,
#     lcd_rows
# )
#
# lcd.backlight = True
#
#
# def display(message):
#     lcd.clear()
#     for line in message.split("\n"):
#         if len(line) > 16:
#             raise KeyError(f"Line too long - {len(line)} characters, 16 max")
#
#     lcd.message = message


def button_press():  # Does a single check if any of the buttons are pressed.
    for button in buttons:
        if button.is_pressed:
            return buttons.index(button)


def activate_led(leds=leds):
    try:
        for led in leds:
            led.on()
    except Exception:
        led.on()


def deactivate_led(leds=leds):
    try:
        for led in leds:
            led.off()
    except Exception:
        led.off()


def flash_led(leds=leds):
    for _ in range(3):
        activate_led(leds)
        time.sleep(.2)
        deactivate_led(leds)


def main():
    while True:
        try:
            button_pressed = button_press()
            if button_pressed:
                flash_led(button_led[button_pressed])
        except KeyboardInterrupt:
            break

    print("Flashing LED 1.")
    flash_led(l1)
    print("Flashing LED 2.")
    flash_led(l2)
    print("Flashing LED 3.")
    flash_led(l3)


if __name__ == "__main__":
    main()

    # Using BOARD numbers.
    # Raspberry Pi 3

    # Pin Configuration:

    # Buttons and LEDs:

    # B1: Pin 12, GPIO 18
    # L1: Pin 16, GPIO 23

    # B2: Pin 18, GPIO 24
    # L2: Pin 22, GPIO 25

    # B3: Pin 24, GPIO 8
    # L3: Pin 26, GPIO 7

    # LCD: https://learn.adafruit.com/character-lcds/python-circuitpython

    # 1:  GND     - PIN 9
    # 2:  5V      - PIN 2
    # 3:  V0      - PIN NONE - POTENTIOMETER - DO WE REALLY NEED THIS
    # 4:  GPIO 2  - PIN 3
    # 5:  GND     - PIN 25
    # 6:  GPIO 3  - PIN 5
    # 7:  SKIP    - PIN
    # 8:  SKIP    - PIN
    # 9:  SKIP    - PIN
    # 10: SKIP    - PIN
    # 11: GPIO 4  - PIN 7
    # 12: GPIO 17 - PIN 11
    # 13: GPIO 27 - PIN 13
    # 14: GPIO 22 - PIN 15
    # 15: 5V      - PIN 4
    # 16: GND     - PIN 39

    # Could merge the ground wires together
