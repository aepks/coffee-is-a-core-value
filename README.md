## Project Design
#### Local account and balance system for the coffee and soda machines at AEPKS


Justin Schmitz, Daniel Keats (Jimmy)

### Main Objectives:

1. Provide an easy and efficient method for regulating account balances using student's Hawkcards, or any other 125 kHZ RFID card if they are not a student. This includes:

  1. Adding money to accounts.
  2. Purchasing items from the machines.
  3. Refunding account balance.


3. Allow for account management - such that if somebody claims they put money in and didn't get it, or some other strange thing happened, this needs to be fixable by an administrator. This should be easy to do, such that it doesn't need to be done by the guy who wrote the thing, so that it is sustainable into the future.

4. Allow for guests to purchase items - guests need a way to put money into the soda machine and purchase both soda and coffee products.

5. Automatic account registration - such that without having to sign up online or in advance, IIT students will be able to scan their ID for the first time and have an account generate, including pulling their hawk email address.

6. Enforcement of payment - ensure that the system cannot easily be 'broken' so as to allow a person who did not pay to receive product.

7. Encryption - The service should be at least a little secure, with encryption on the administrator passwords.

8. A web portal - a simple website for an administrator where they can access and modify accounts, change prices, and obtain full data exports.

9. A receipt system - a button that, when pressed, sends an email to the user containing their full purchase history, their current balance, and a graph showing their purchases over time.

10. Have an automated email system in place to let users know when their balance is starting to run low (5$, <1$).

### Implementation Details:

###### Hardware:

Raspberry Pi models will be used for the parts of the machine. The responsibilities of each 'half' of the device:

1. Soda Machine (Master):
   * Host the mySQL server and the web portal.
   * Have an RFID reader for a user to scan into their account.
   * Allow for the input of money into a user account.
   * Allow for the return of money from a user account. (Refunds)
   * Have a 'receipt' button to send the user their receipt.
   * Have a 'logoff' button, for when the user is done with their session.
   * Have a button for the user to purchase a soda, and regulate this with the account system.


2. Coffee Machine (Slave):
  * Connect to the mySQL server hosted by the Soda Machine Pi.
  * Have an RFID reader for a user to scan into their account.
  * Have a button for the user to purchase a coffee.
  * Have a guard mechanism to uncover and recover the touchscreen of the coffee machine, to prevent unauthorized purchases
  * Have a 'logoff' button, for when the user is done with their session.

###### Software:

The program will be mostly written in Python 3. This makes it easy to use mySQL, as well as connecting to physical buttons using GPIO.

**mySQL Table Design:**

There will be n+1 tables, where n refers to the number of users of the program.

The tables will be laid out as follows:

'main' table:

| rfid_key | user_name | balance |
| -------- | --------- | ------- |
| 113815   | jschmitz2 | 35.25   |
| 116381   | jschmoe38 | 2.31    |

'user' table (for each individual user):
*note: this table will be named after their user ID*

| timestamp | action   | item | amount | prev_bal | cur_bal |
| --------- | -------- | ---- | ------ | -------- | ------- |
| *format*  | purchase | soda | 0.50   | 35.75    | 35.25   |

###### Money Input Design

**whatever jimmy says is true**
