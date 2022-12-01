import string, secrets, getpass, os, sqlite3, platformdirs, platform
from time import sleep
import pyperclip3 as pc

def cls():
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')

def post_login(mast_username, mast_pass):
    path = ''
    if platform.system() == 'Linux':
        path = f"{platformdirs.user_data_dir()}/passman"
    elif platform.system() == 'Windows':
        path = f"{platformdirs.user_data_dir()}\\passman"
    if not os.path.exists(path):
        os.makedirs(path)
    conn2 = ''
    if platform.system() == 'Linux':
        conn2 = sqlite3.connect(f"{path}/pass.db")
    elif platform.system() == 'Windows':
        conn2 = sqlite3.connect(f"{path}\\pass.db")
    crsr2 = conn2.cursor()
    sqldb = "CREATE TABLE passwords (master_user VARCHAR(100), alias VARCHAR(100), username VARCHAR(100), password VARCHAR(100));"
    crsr2.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='passwords';")
    if crsr2.fetchone()[0] != 1:
        crsr2.execute(sqldb)
    a = input('1. Create a new entry for an account\n2. Generate a new 16-digit alphanumeric password\n3. Access previously saved passwords\n4. Edit the password or username for an account\n5. Delete an account already present\n6. Logout\n7. Exit\nEnter your choice: ')
    if a == '1':
        cls()
        def new_acc():
            acc_alias = input('Please enter the service name for which this account is being added: ')
            acc_username = input('Please enter the user name: ')
            acc_pass = getpass.getpass('Please enter the password: ')
            conf_acc_pass = getpass.getpass('Please enter the password again for confirmation: ')
            if (conf_acc_pass != acc_pass):
                print('The confirmed password and the provided password do not match.\nKindly try again.')
                new_acc()
            elif (conf_acc_pass == acc_pass):
                crsr2.execute("INSERT INTO passwords (master_user, alias, username, password)values(?,?,?,?)", (mast_username, acc_alias, acc_username, acc_pass))
                conn2.commit()
                print('A new account has been added successfully.')
        new_acc()
        post_login(mast_username, mast_pass)
    elif a == '2':
        cls()
        secure_pass = ''
        while(secure_pass.isalpha() or secure_pass.isnumeric() or secure_pass == ''):
            secure_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        b = input('Would you like to display the password or copy it to your clipboard?\n1. Display\n2. Copy it to my clipboard\n3. Do both\n4. Return to the menu\nEnter your choice: ')
        if b == '1':
            cls()
            print(f"The password generated is: {secure_pass} \nThis message will disappear in the next 10 seconds.")
            sleep(10)
            cls()
            post_login(mast_username, mast_pass)
        elif b == '2':
            cls()
            pc.copy(secure_pass)
            print(f'The password has been copied to your clipboard.')
            post_login(mast_username, mast_pass)
        elif b == '3':
            cls()
            pc.copy(secure_pass)
            print(f'The password generated is: {secure_pass}\nAnd it has been copied to your clipboard.\nThis message will disappear in the next 5 seconds.')
            sleep(5)
            cls()
            post_login(mast_username, mast_pass)
        elif b == '4':
            post_login(mast_username, mast_pass)
        else:
            print('Please enter a valid input.')
            post_login(mast_username, mast_pass)
    elif a == '3': 
            crsr2.execute("SELECT * FROM passwords WHERE master_user=:mast_username;", {"mast_username": mast_username})
            all_pass = crsr2.fetchall()
            if len(all_pass) == 0: 
                cls()
                print('There are no account services registered in your user.\nTo use this function kindly add more users.')
                post_login(mast_username, mast_pass)
            cls()
            def disp_acc(mast_pass):
                b = input('Would you like to: \n1. Display all the account services entered\n2. Search for the certain account service and get its password\n3. Return to the menu\nEnter your choice: ')
                if b == '1':
                    cls()
                    end_print = ''
                    for i in all_pass:
                        end_print = end_print + f'\nAccount Service: {i[1]}\nUsername: {i[2]}'
                    print(f'{end_print}\n')
                    sleep(2)
                    disp_acc(mast_pass)
                elif b == '2':
                    c = getpass.getpass('Verify your identity first. Enter your master password: ')
                    if c != mast_pass:
                        print('The password was incorrect please try again.')
                        disp_acc(mast_pass)
                    c = input('Which account service would you like to find the password of: ')
                    loop_car = ''
                    loop_list = []
                    j = 0
                    for i in all_pass:
                        if c.lower() == i[1].lower():
                            j += 1
                            loop_list.append([i[2], i[3]])
                            loop_car = loop_car + f'{j}. Account username: {i[2]}\nAccount password: {i[3]}\n'
                    if len(loop_car) > 1:                        
                        d = input('Copy an entry to your clipboard? y/n: ')
                        if d.lower().startswith('n'):
                            disp_acc(mast_pass)
                        elif d.lower().startswith('y'):
                            def copy_pass(loop_list, mast_pass):
                                try:
                                    d = int(input('Choose the serial number of the entry to copy to your clipboard: '))
                                    if d > len(loop_list):
                                        print('Choose a valid entry.')
                                        copy_pass(loop_list, mast_pass)
                                    elif d <= len(loop_list): 
                                        pc.copy(loop_list[d-1][1])
                                        print(f'The password "{loop_list[d-1][1]}" has been copied to your clipboard!')
                                        sleep(1)
                                        cls()
                                        disp_acc(mast_pass)
                                except:
                                    print('Please enter a valid number.')
                                    disp_acc(mast_pass)
                            copy_pass(loop_list, mast_pass)
                    else:
                        print(loop_car)
                        print('I could not find any accounts matching that account service, make sure you entered it correctly.\nTry finding an account service by displaying all of them.')
                        disp_acc(mast_pass)
                elif b == '3':
                    post_login(mast_username, mast_pass)
            disp_acc(mast_pass)
        
    elif a == '4':
        cls()
        c = getpass.getpass('Verify your identity first. Enter your master password: ')
        if c != mast_pass:
            cls()
            print('The password was incorrect please try again.')
            post_login(mast_username, mast_pass)
        acc_alias = input('Please enter the service name for this account: ')
        acc_username = input('Please enter the user name: ')
        crsr2.execute("SELECT * FROM passwords WHERE master_user=:mast_username AND alias =:acc_alias AND username=:acc_username;", {"mast_username": mast_username, "acc_alias": acc_alias, "acc_username": acc_username})
        all_acc = crsr2.fetchall()
        if len(all_acc) < 1:
            print('No entries with the specified parameters could be found.')
            post_login(mast_username, mast_pass)
        acc_pass = getpass.getpass('Please enter the new password: ')
        for i in all_acc:
            crsr2.execute("UPDATE passwords SET password=:acc_pass WHERE master_user=:mast_username AND alias =:acc_alias AND username=:acc_username;", {"acc_pass":acc_pass, "mast_username": mast_username, "acc_alias": acc_alias, "acc_username": acc_username})
            conn2.commit()
        print(f'Successfully changed the password of {acc_alias} for the account name {acc_username}.')
        post_login(mast_username, mast_pass)

    elif a == '5':
        cls()
        c = getpass.getpass('Verify your identity first. Enter your master password: ')
        if c != mast_pass:
            cls()
            print('The password was incorrect please try again.')
            post_login(mast_username, mast_pass)
        acc_alias = input('Please enter the service name for the account to be deleted: ')
        acc_username = input('Please enter the user name: ')
        crsr2.execute("SELECT * FROM passwords WHERE master_user=:mast_username AND alias =:acc_alias AND username=:acc_username;", {"mast_username": mast_username, "acc_alias": acc_alias, "acc_username": acc_username})
        all_acc = crsr2.fetchall()
        print(len(all_acc))
        if len(all_acc) < 1:
            print('No entries with the specified parameters could be found.')
            post_login(mast_username, mast_pass)
        elif len(all_acc) >= 1:
            crsr2.execute("DELETE FROM passwords WHERE master_user=:mast_username AND alias =:acc_alias AND username=:acc_username;", {"mast_username": mast_username, "acc_alias": acc_alias, "acc_username": acc_username})
            conn2.commit()
            print(f'Successfully deleted the entry of {acc_alias} for the account name {acc_username}.')
            sleep(2)
            cls()
            post_login(mast_username, mast_pass)

    elif a == '6':
        cls()
        return
    elif a == '7':
        cls()
        print("Thank you for using our password manager!")
        quit()
    else: 
        cls()
        print('This function does not exist ')
        sleep(2)
        cls()
        post_login(mast_username, mast_pass)