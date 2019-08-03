# Project Design
#### Local account and balance system for the coffee and soda machines at AEPKS

### Authors:

###### Justin Schmitz:
* Market Research
* Policy Decisions
* Physical Enclosure
* Database Configuration and Use
* Payment API Configuration
* Program Runtime

###### Gabriel Krell:
* R305 Package Development
* General advising and assistance with development

### Usage:

##### Consumer Use:

1. User wakes machine.
  1. Machine is woken with a button press or RFID input.
1. User logs in.
  1. Machine scans for either fingerprint or RFID card input.
  2. Once input is read, attempt to authenticate.
    1. If authentication is successful, continue.
    2. Else, proceed appropriately.
      1. If input failed to read, try again.
      2. If RFID card number not recognized, proceed to 'User Registration'.
2. User Registration:
  1. Given user's RFID key as an input, create a new user.
  1. If there's an open fingerprint slot, use this slot. Otherwise, find the user that logged in last, and clear that fingerprint slot, and assign it to the new user.
3. User Interaction:
  1. To purchase an item, user presses the relevant button [to be finalized later].
  2. User then presses a button to be logged out, or is logged out after 30 seconds.

##### Manager Use:
Process is in progress.
