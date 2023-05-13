import json
import argparse
import os
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(filename='banking_system.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the JSON database file exists, and create it if it doesn't
if not os.path.exists('bank_db.json'):
    with open('bank_db.json', 'w') as f:
        json.dump({}, f)

# Load the JSON database file into memory
with open('bank_db.json', 'r') as f:
    bank_db = json.load(f)

# Define the operations that can be performed
OPERATIONS = ['Delete', 'Deposit', 'Withdraw', 'Fund Transfer', 'List', 'Exit']

# Define the argparse arguments
parser = argparse.ArgumentParser(description='Basic Banking System')
parser.add_argument('-u', '--username', type=str, required=True, help='The username for the account')
parser.add_argument('-db', '--database', type=str, required=True, help='The location of the JSON database file')
args = parser.parse_args()

# Check if the user exists in the database, and create a new account if they don't
if args.username not in bank_db:
    bank_db[args.username] = {'id': len(bank_db) + 1, 'balance': 0, 'last_transaction': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    with open(args.database, 'w') as f:
        json.dump(bank_db, f)

# Define the functions for the operations

def delete_account():
    logging.info('Deleting account for user %s', args.username)
    del bank_db[args.username]
    with open(args.database, 'w') as f:
        json.dump(bank_db, f)
    print('Account deleted successfully')

def deposit(amount):
    logging.info('Depositing %d rupees to account of user %s', amount, args.username)
    bank_db[args.username]['balance'] += amount
    bank_db[args.username]['last_transaction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(args.database, 'w') as f:
        json.dump(bank_db, f)
    print('Deposit of {} rupees successful'.format(amount))

def withdraw(amount):
    logging.info('Withdrawing %d rupees from account of user %s', amount, args.username)
    if bank_db[args.username]['balance'] >= amount:
        bank_db[args.username]['balance'] -= amount
        bank_db[args.username]['last_transaction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(args.database, 'w') as f:
            json.dump(bank_db, f)
        print('Withdrawal of {} rupees successful'.format(amount))
    else:
        print('Insufficient balance')

def fund_transfer(amount, recipient):
    logging.info('Transferring %d rupees from account of user %s to account of user %s', amount, args.username, recipient)
    if bank_db[args.username]['balance'] >= amount:
        bank_db[args.username]['balance'] -= amount
        bank_db[args.username]['last_transaction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bank_db[recipient]['balance'] += amount
        bank_db[recipient]['last_transaction'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(args.database, 'w') as f:
            json.dump(bank_db, f)
        print('Transfer of {} rupees successful to {}'.format(amount, recipient))
    else:
        print('Insufficient balance')

# Get user input for the operation to perform
while True:
    print('Operations:', ', '.join(OPERATIONS))
    operation = input('Enter the operation to perform: ')
    if operation not in OPERATIONS:
        print('Invalid operation')
        continue
    if operation == 'Delete':
        confirm = input('Are you sure you want to delete your account? This action is irreversible. (y/n): ')
        if confirm.lower() == 'y':
            delete_account()
            break
        else:
            continue
    elif operation == 'Deposit':
        amount = input('Enter the amount to deposit: ')
        try:
            amount = int(amount)
            if amount < 0:
                raise ValueError
        except ValueError:
            print('Invalid amount')
            continue
        deposit(amount)
    elif operation == 'Withdraw':
        amount = input('Enter the amount to withdraw: ')
        try:
            amount = int(amount)
            if amount < 0:
                raise ValueError
        except ValueError:
            print('Invalid amount')
            continue
        withdraw(amount)
    elif operation == 'Fund Transfer':
        amount = input('Enter the amount to transfer: ')
        try:
            amount = int(amount)
            if amount < 0:
                raise ValueError
        except ValueError:
            print('Invalid amount')
            continue
        recipient = input('Enter the recipient\'s username: ')
        if recipient not in bank_db:
            print('Recipient not found')
            continue
        fund_transfer(amount, recipient)
    elif operation == 'List':
        print('Account details:')
        print(json.dumps(bank_db[args.username], indent=4))
    elif operation == 'Exit':
        break

print('Thank you for using the banking system')
logging.shutdown()