import getpass, os
from time import sleep
from postlogin import *
import platform

def cls():
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')

def master_select(crsr, conn):
    print('''1. Create a new user\n2. Login to existing user\n3. Exit the program''')
    a = input('Please select an option from the above options: ')
    if a == '1':
        def masterpass():
            username = input('Enter a username: ')
            password = getpass.getpass('Enter a password: ')
            conf_password = getpass.getpass(
                'Enter the password again for confirmation: ')
            if (conf_password != password):
                print('The two passwords provided do not match. Kindly try again.')
                masterpass()
            elif (len(password) < 10):
                print('Kindly enter a more secure password longer than 10 characters.')
                masterpass()
            if (conf_password == password):                
                crsr.execute(
                    "INSERT INTO master (username, password)values(?,?)", (username, password))
                conn.commit()
                cls()
                print(f'Successfully created a new user with the username: \'{username}\' in the password manager.')
                sleep(3)                
            master_select(crsr, conn)
        masterpass()
    elif a == '2':
        username = input('Enter a username in this server: ')
        password = getpass.getpass('Enter the password for this user: ')
        crsr.execute("SELECT * FROM master")
        ans = crsr.fetchall()
        conf_pass = 0
        while conf_pass == 0:
            for i in ans:
                if password == i[1] and username == i[0]:
                    cls()
                    print(f'Logged in to the user {username}')
                    print(f'Hello and welcome to the password manager {username}!')
                    sleep(2)
                    cls()
                    mast_username = username
                    mast_pass = password
                    post_login(mast_username, mast_pass)
                    conf_pass = 1
                elif password != i[1]:
                    continue
            if conf_pass == 0:
                print('Invalid username or password entered.')
                conf_pass = 1
        master_select(crsr, conn)
    elif a == '3':
        cls()
        print('Thank you for using our password manager!')
        sleep(1)
        cls()
        quit()
    else:
        print('Please enter a valid input.')
        sleep(3)
        cls()
        master_select(crsr, conn)
