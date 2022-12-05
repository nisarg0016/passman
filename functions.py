if __name__ == "__main__":
    print('This is not an executable file. To access the password manager, execute \'passman.py\'.')
    quit()

import tkinter as tk, sqlite3, os, platform, platformdirs, pyglet, secrets, string, pyperclip3 as pc
from tkinter import ttk
from passman import main, bindToEntry
from time import sleep

pyglet.font.add_file(f'{os.path.dirname(os.path.realpath(__file__))}/assets/FiraCode.ttf')


def erase(entry, placeholder, event=None):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
    if 'password' in placeholder:
        entry["show"] = "*"

def add(entry, placeholder, event=None):
    if 'password' in placeholder and entry.get() == '':
        entry["show"] = ""
    if entry.get() == '':
        entry.insert(0, placeholder)

def bindToEntry(entry, placeholder):
    entry.bind('<FocusOut>', lambda event: add(entry, placeholder))
    entry.insert(0, placeholder)
    tempA = entry.get()
    entry.bind('<FocusIn>', lambda event: erase(entry, placeholder))

def promptWin(root, text, wrap, height, width):
    promptWindow = tk.Toplevel(root)
    promptCanvas = tk.Canvas(promptWindow, height = height, width = width)
    promptWindow.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')
    textFrame = ttk.Frame(promptWindow)
    textFrame.pack(fill="both", expand=True)
    textFrame.place(anchor = "c", relx = .5, rely = .5)
    textLabel = tk.Label(textFrame, text = f'{text}', wraplength = wrap, justify = 'center', font = ('Fira Code SemiBold', 12))
    textLabel.pack()
    promptCanvas.pack()

def createEntryFunc(userWin, crsr2, conn2, masterUsername):
    entryCreate = tk.Toplevel(userWin)
    entryCreate.title('Create a new entry')
    entryCreateCanvas = tk.Canvas(entryCreate, height = 533, width = 800)
    entryCreate.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

    EntryCreateFrame = tk.Frame(entryCreate)
    EntryCreateFrame.pack(fill = 'both', expand = True)
    EntryCreateFrame.place(anchor = 'c', relx = .5, rely = .5)

    def submit(service, serviceUsername, servicePassword, serviceConfirmPassword, crsr2, masterUsername):
        confMatch = 0
        serviceString = service.get()
        serviceUsernameString = serviceUsername.get()
        servicePassString = servicePassword.get()
        servicePassConfString = serviceConfirmPassword.get()
        if serviceString == 'Enter the name of the service' or serviceUsernameString == 'Enter the username of the account' or servicePassString == 'Enter the password of the account' or servicePassConfString == 'Confirm the password':
            promptWin(entryCreate, 'Please fill out all of the fields.', 150, 150, 200)
        else:
            if servicePassString != servicePassConfString:
                confMatch = 1
                promptWin(entryCreate, 'The passwords do not match. Kindly try again.', 200, 150, 300)
            if confMatch == 0:
                crsr2.execute('SELECT * FROM passwords WHERE master_user=:username_alias;', {"username_alias": masterUsername})
                allEntries = crsr2.fetchall()
                matchFound = 0
                for i in allEntries:
                    if i[1] == serviceString and i[2] == serviceUsernameString and matchFound == 0:
                        matchFound = 1
                        promptWin(entryCreate, 'A similar username associated with this service already exists. To edit the password, choose "Edit an entry" instead.', 450, 150, 500)
                if matchFound == 0:
                    crsr2.execute('INSERT INTO passwords VALUES(?, ?, ?, ?)', (masterUsername, serviceString, serviceUsernameString, servicePassString))
                    conn2.commit()
                    promptWin(entryCreate, f'An account with the username {serviceUsernameString} has been added to a service with the name: {serviceString}.', 450, 150, 500)
            elif confMatch == 1:
                return

    service, serviceUsername, servicePassword, serviceConfirmPassword = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
    serviceEntry = ttk.Entry(EntryCreateFrame, textvariable = service, width = 50)
    serviceEntry.pack(pady = 10)
    bindToEntry(serviceEntry, 'Enter the name of the service')
    usernameEntry = ttk.Entry(EntryCreateFrame, textvariable = serviceUsername, width = 50)
    usernameEntry.pack(pady = 10)
    bindToEntry(usernameEntry, 'Enter the username of the account')
    passwordEntry = ttk.Entry(EntryCreateFrame, textvariable = servicePassword, width = 50)
    passwordEntry.pack(pady = 10)
    bindToEntry(passwordEntry, 'Enter the password of the account')
    confirmPasswordEntry = ttk.Entry(EntryCreateFrame, textvariable = serviceConfirmPassword, width = 50)
    confirmPasswordEntry.pack(pady = 10)
    bindToEntry(confirmPasswordEntry, 'Confirm the password')
    submitButton = ttk.Button(EntryCreateFrame, text = 'Create the entry', style = 'Accent.TButton', command = lambda: submit(service, serviceUsername, servicePassword, serviceConfirmPassword, crsr2, masterUsername))
    submitButton.pack(pady = 25)

    entryCreateCanvas.pack()


def generatePassword(userWin):
    securePassword = ''
    while(securePassword.isalpha() or securePassword.isnumeric() or securePassword == ''):
        securePassword = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
    def displayWin(securePassword, userWin):
        passDisplay = tk.Toplevel(userWin)
        passDisplay.title('Generated password!')
        passDisplayCanvas = tk.Canvas(passDisplay, height = 533, width = 800)
        passDisplay.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

        PassDisplayFrame = tk.Frame(passDisplay)
        PassDisplayFrame.pack(fill="both", expand=True)
        PassDisplayFrame.place(anchor="c", relx=.5, rely=.5)

        def displayClip(passDisplay, userWin, securePassword):
            passDisplay.destroy()
            displayClipboard = tk.Toplevel(userWin)
            displayClipboard.title('Here\'s the generated password!')
            displayClipboardCanvas = tk.Canvas(displayClipboard, height = 150, width = 700)
            displayClipboard.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

            DisplayClipboardFrame = tk.Frame(displayClipboard)
            DisplayClipboardFrame.pack(fill="both", expand=True)
            DisplayClipboardFrame.place(anchor="c", relx=.5, rely=.5)

            passwordLabel = tk.Label(DisplayClipboardFrame, text = f"The password is: {securePassword}", font = ('Fira Code SemiBold', 20))
            passwordLabel.pack(pady = 20)
            disappearLabel = tk.Label(DisplayClipboardFrame, text = "This window will disappear in 10 seconds.", font = ('Fira Code SemiBold', 10))
            disappearLabel.pack(pady = 10)

            displayClipboardCanvas.pack()
            displayClipboard.after(10000, lambda: displayClipboard.destroy())
            def closeWin():
                displayClipboard.destroy()
                displayWin(securePassword, userWin)
            displayClipboard.protocol("WM_DELETE_WINDOW", lambda: closeWin())

        copyPass = ttk.Button(PassDisplayFrame, text = 'Copy the newly generated password', style = 'Accent.TButton', command = lambda: pc.copy(securePassword))
        copyPass.pack(pady = 10)
        displayPass = ttk.Button(PassDisplayFrame, text = 'Display the newly generated password', style = 'Accent.TButton', command = lambda: displayClip(passDisplay, userWin, securePassword))
        displayPass.pack(pady = 10)
        cAndDPass = ttk.Button(PassDisplayFrame, text='Copy and display', style='Accent.TButton', command=lambda: (pc.copy(securePassword), displayClip(passDisplay, userWin, securePassword)))
        cAndDPass.pack(pady = 10)

        passDisplayCanvas.pack()
    displayWin(securePassword, userWin)


def displayEntries():
    pass


def loginToMain(root, crsr, loginUsername, loginPassword):
    username = loginUsername.get()
    password = loginPassword.get()
    if (username == 'Enter your username' or password == 'Enter your password') or (len(username) == 0 or len(password) == 0):
        return
    crsr.execute('SELECT * FROM master;')
    masterDB = crsr.fetchall()
    loginCheck = 0
    for i in masterDB:
        if username == i[0] and password == i[1]:
            loginCheck = 1

    if loginCheck == 0:
        promptWin(root, 'Error logging in, the username or password is incorrect.', 200, 150, 300)

    elif loginCheck == 1:
        userWindow(root, username, password)
        main()


def createNewUser(root, crsr, conn, loginUsername, loginPassword):
    username = loginUsername.get()
    password = loginPassword.get()
    if (username == 'Enter your username' or password == 'Enter your password') or (len(username) == 0 or len(password) == 0):
        return
    crsr.execute('SELECT * FROM master;')
    masterDB = crsr.fetchall()
    noUserExists = 0
    for i in masterDB:
        if i [0] == username:
            promptWin(root, 'A user with this username already exists, please select a new username.', 250, 150, 300)
            noUserExists = 1
    if noUserExists == 1:
        return
    elif noUserExists == 0:
        def submitConf():
            confirmPassString = confirmPass.get()
            if confirmPassString == password:
                crsr.execute('INSERT INTO master (username, password) VALUES(?, ?)', (username, password))
                conn.commit()
                confirmPassWin.destroy()
                promptWin(root, f'Successfully created a user with the username: {username}', 250, 150, 300)
            else:
                promptWin(confirmPassWin, 'The two passwords do not match. Kindly try again.', 300, 150, 350)

        confirmPassWin = tk.Toplevel(root)
        confirmPassWin.title('Confirm the password for your new account.')
        confirmPassWin.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

        confirmPassWinCanvas = tk.Canvas(confirmPassWin, height = 233, width = 450)
        ConfirmPassWinFrame = tk.Frame(confirmPassWin)
        ConfirmPassWinFrame.pack(fill="both", expand=True)
        ConfirmPassWinFrame.place(anchor="c", relx=.5, rely=.5)

        confirmPass = tk.StringVar()
        confirmPassEntry = ttk.Entry(ConfirmPassWinFrame, textvariable = confirmPass)
        confirmPassEntry.pack(pady = 15)
        bindToEntry(confirmPassEntry, 'Confirm the password')
        confirmButton = ttk.Button(ConfirmPassWinFrame, text = 'Confirm', style = 'Accent.TButton', command = lambda: submitConf())
        confirmButton.pack(pady = 10)

        confirmPassWinCanvas.pack()


def userWindow(root, username, password):
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
    crsr2.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='passwords';")
    if crsr2.fetchone()[0] != 1:
        crsr2.execute("CREATE TABLE passwords (master_user VARCHAR(100), alias VARCHAR(100), username VARCHAR(100), password VARCHAR(100));")


    root.destroy()

    userWin = tk.Tk()
    userWin.title(f'Hello {username}!')
    userWin.tk.call("source", f"{os.path.dirname(os.path.realpath(__file__))}/themes/azure.tcl")
    userWin.tk.call("set_theme", "dark")

    userWinCanvas = tk.Canvas(userWin, height=533, width=1000)
    userWin.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

    MainFrame = ttk.Frame(userWin)
    MainFrame.pack(fill="both", expand=True)
    MainFrame.place(anchor="c", relx=.25, rely=.5)

    generatePass = ttk.Button(MainFrame, text = 'Generate a random 16 character alphanumeric password', style = 'Accent.TButton', command = lambda: generatePassword(userWin))
    generatePass.pack(pady = 10)

    createEntry = ttk.Button(MainFrame, text = 'Create a new entry', style = 'Accent.TButton', command = lambda: createEntryFunc(userWin, crsr2, conn2, username))
    createEntry.pack(pady = 10)

    deleteEntry = ttk.Button(MainFrame, text = 'Delete the selected entry', state = tk.DISABLED, command = lambda: authAndDo('delete'))
    deleteEntry.pack(pady = 10)

    editEntry = ttk.Button(MainFrame, text = 'Edit the selected entry', state = tk.DISABLED, command = lambda: authAndDo('edit'))
    editEntry.pack(pady = 10)

    AliasFrame = ttk.Frame(userWin)
    EntryFrame = ttk.Frame(userWin)
    TreeFrame = ttk.Frame(EntryFrame)

    bigLabel = ttk.Label(AliasFrame, text= f'Welcome to the password manager, {username}!', wraplength = 400, font = ('Fira Code SemiBold', 25))
    bigLabel.pack()

    treeScrollBar = ttk.Scrollbar(TreeFrame)
    treeScrollBar.pack(side = 'right', fill = 'y')

    entryTree = ttk.Treeview(TreeFrame, selectmode = "browse", yscrollcommand=treeScrollBar.set, columns = (1), height = 10)
    entryTree.pack(expand = False, fill = "both")
    treeScrollBar.config(command = entryTree.yview)
    entryTree.column("#0", anchor = "w", width = 200)
    entryTree.column(1, anchor = "w", width = 200)
    entryTree.heading("#0", text = "Service", anchor = "center")
    entryTree.heading(1, text = "Username", anchor = "center")
    
    TreeFrame.pack()

    noteLabel = ttk.Label(EntryFrame, text = 'To select an entry, double click on it.', justify = 'c', wraplength = 400, font = ('Fira Code SemiBold', 12))
    noteLabel.pack(pady = 20)
    note2Label = ttk.Label(EntryFrame, text = 'To refresh the table after a deletion or edit of an entry, double click on the "View all entries" button.', justify = 'c', wraplength = 400, font = ('Fira Code SemiBold', 12))
    note2Label.pack(pady = 10)

    ButtonFrame = tk.Frame(EntryFrame)

    def authAndDo(typeDo = None):
        finalCheck = [0]
        authenticateWin = tk.Toplevel()
        authenticateCanvas = tk.Canvas(authenticateWin, height = 150, width = 600)
        authenticateWin.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')
        authenticateFrame = tk.Frame(authenticateWin)
        authenticateFrame.pack(fill = "both", expand = True)
        authenticateFrame.place(anchor = "c", relx = .5, rely = .5)
        authenticateVar = tk.StringVar()
        authenticateEntry = ttk.Entry(authenticateFrame, textvariable = authenticateVar, width = 50)
        authenticateEntry.pack(pady = 10)
        bindToEntry(authenticateEntry, "Enter your master password")
        def authenticate():
            def temp():
                checkPass = authenticateEntry.get()
                if checkPass == password:
                    authenticateWin.destroy()
                    return True
                else:
                    for i in authenticateFrame.winfo_children():
                        if i.winfo_class() == 'TLabel':
                            i.pack_forget()
                    failureLabel = ttk.Label(authenticateFrame, text = 'This master password is incorrect.', justify = 'c', font = ('Fira Code SemiBold', 12))
                    failureLabel.pack(pady = 10)
            output = temp()
            if output:
                finalCheck[0] = 1
                return bool(finalCheck[0])

        def submit():
            check = authenticate()
            if check:
                focusItem = entryTree.focus()
                dataFocus = entryTree.item(focusItem)
                crsr2.execute('SELECT password FROM passwords WHERE master_user=:m_u_a AND alias=:s_a AND username=:u_a;', {"m_u_a": username, "s_a": dataFocus["text"], "u_a": dataFocus["values"][0]})
                tempStore = crsr2.fetchall()
                if typeDo == 'copy':
                    pc.copy(tempStore[0][0])
                    promptWin(userWin, 'The password has been copied to your clipboard.', 175, 150, 200)
                elif typeDo == 'delete':
                    crsr2.execute('DELETE FROM passwords WHERE master_user=:m_u_a AND alias=:s_a AND username=:u_a;', {"m_u_a": username, "s_a": dataFocus["text"], "u_a": dataFocus["values"][0]})
                    conn2.commit()
                    promptWin(userWin, 'The entry has been deleted.', 175, 150, 200)
                elif typeDo == 'edit':
                    editPassWin = tk.Toplevel(userWin)
                    editPassWin.title('Edit the entry')
                    editPassCanvas = tk.Canvas(editPassWin, height = 333, width = 600)
                    editPassFrame = tk.Frame(editPassWin)
                    editPassFrame.pack(fill = "both", expand = True)
                    editPassFrame.place(anchor = "c", relx = .5, rely = .5)
                    editPassVar = tk.StringVar()
                    editUserVar = tk.StringVar()
                    editUserEntry = ttk.Entry(editPassFrame, textvariable = editUserVar, width = 50)
                    editUserEntry.pack(pady = 5)
                    bindToEntry(editUserEntry, 'Enter your new username')
                    editPassEntry = ttk.Entry(editPassFrame, textvariable = editPassVar, width = 50)
                    editPassEntry.pack(pady = 5)
                    bindToEntry(editPassEntry, 'Enter your new password')
                    editLabel = ttk.Label(editPassFrame, text = 'You need to enter something in at least one of the above fields.', wraplength = 400, font = ('Fira Code SemiBold', 10), justify = 'c')
                    editLabel.pack(pady = 10)
                    def editConfirm():
                        passStr = editPassVar.get()
                        userStr = editUserVar.get()
                        if (passStr == 'Enter your new password' or len(passStr) == 0) and (userStr == 'Enter your new username' or len(userStr) == 0):
                            promptWin(editPassWin, 'Please fill at least one of the fields.', 175, 150, 200)
                        else:
                            crsr2.execute('SELECT username, password FROM passwords WHERE master_user=:m_u_a AND alias=:s_a AND username=:u_a;', {"m_u_a": username, "s_a": dataFocus["text"], "u_a": dataFocus["values"][0]})
                            workWithThis = crsr2.fetchall()
                            if userStr == 'Enter your new username' or len(userStr) == 0:
                                userStr = workWithThis[0][0]
                            elif passStr == 'Enter your new password' or len(passStr) == 0:
                                passStr = workWithThis[0][1]
                            crsr2.execute('UPDATE passwords SET username=:u_a, password=:p_a WHERE master_user=:m_u_a AND alias=:s_a AND username=:u_o_a;', {"u_a": userStr, "p_a": passStr, "m_u_a": username, "s_a": dataFocus["text"], "u_o_a": dataFocus["values"][0]})
                            conn2.commit()
                            editPassWin.destroy()
                            promptWin(userWin, 'Successfully edited the entry.', 175, 150, 200)
                    editButton = ttk.Button(editPassFrame, text = 'Edit', command = editConfirm, style = 'Accent.TButton')
                    editButton.pack(pady = 10)
                    editPassCanvas.pack()
                    editPassWin.mainloop()
                else:
                    showPassWin = tk.Toplevel(userWin)
                    showPassWin.title('Here\'s the password')
                    showPassCanvas = tk.Canvas(showPassWin, height = 150, width = 400)
                    showPassWin.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')
                    showPassFrame = tk.Frame(showPassWin)
                    showPassFrame.pack(fill = "both", expand = True)
                    showPassFrame.place(anchor = "c", relx = .5, rely = .5)
                    showPassLabel = ttk.Label(showPassFrame, text = f"The password to the account is: {tempStore[0][0]}", font = ('Fira Code SemiBold', 10))
                    showPassLabel.pack(pady = 20)
                    willDelete = ttk.Label(showPassFrame, text = 'This window will close automatically in 20 seconds.', wraplength = 350, font = ('Fira Code SemiBold', 10))
                    willDelete.pack(pady = 10)
                    def destroySimple():
                        try:
                            showPassWin.destroy()
                        except:
                            return
                    showPassWin.after(20000, destroySimple)
                    showPassCanvas.pack()

        authenticateButton = ttk.Button(authenticateFrame, text = 'Submit', style = 'Accent.TButton', command = submit)
        authenticateButton.pack()
        authenticateCanvas.pack()
        authenticateWin.wait_window()

    viewPassword = ttk.Button(ButtonFrame, text = 'Show password', command = lambda: authAndDo(), state = tk.DISABLED)
    viewPassword.grid(row = 0, column = 0, padx = 10)
    copyPassToClip = ttk.Button(ButtonFrame, text = 'Copy password to clipboard', state = tk.DISABLED, command = lambda: authAndDo('copy'))
    copyPassToClip.grid(row = 0, column = 1, padx = 10)
    ButtonFrame.pack()

    def focusEnable(event = None):
        currentItem = entryTree.focus()
        itemValues = entryTree.item(currentItem)
        if len(itemValues['text']) == 0:
            return
        else:
            deleteEntry['style'] = 'Accent.TButton'
            deleteEntry['state'] = tk.NORMAL
            editEntry['style'] = 'Accent.TButton'
            editEntry['state'] = tk.NORMAL
            viewPassword['style'] = 'Accent.TButton'
            viewPassword['state'] = tk.NORMAL
            copyPassToClip['style'] = 'Accent.TButton'
            copyPassToClip['state'] = tk.NORMAL
    entryTree.bind('<Button-1>', focusEnable)


    crsr2.execute('SELECT alias, username FROM passwords WHERE master_user=:user_alias;', {"user_alias": username})
    dataList = crsr2.fetchall()
    for item in dataList:
        entryTree.insert("", "end", text = item[0], values = item[1], tags = ('normal'))

    def viewFunc():
        entryTree.delete(*entryTree.get_children())
        crsr2.execute('SELECT alias, username FROM passwords WHERE master_user=:user_alias;', {"user_alias": username})
        dataList = crsr2.fetchall()
        for item in dataList:
            entryTree.insert("", "end", text = item[0], values = item[1], tags = ('normal'))
        if viewEntryInt.get() == 0:
            EntryFrame.pack_forget()
            EntryFrame.place_forget()
            deleteEntry['style'] = ''
            deleteEntry['state'] = tk.DISABLED
            editEntry['style'] = ''
            editEntry['state'] = tk.DISABLED
            viewEntries.config(text = 'View all entries')
            AliasFrame.pack(fill = "both", expand = True)
            AliasFrame.place(anchor = "c", relx = .75, rely = .5)
        if viewEntryInt.get() == 1:
            AliasFrame.pack_forget()
            AliasFrame.place_forget()
            EntryFrame.pack(fill = "both", expand = True)
            EntryFrame.place(anchor = "c", relx = .75, rely = .5)
            viewEntries.config(text = 'Hide all entries')

    AliasFrame.pack(fill = "both", expand = True)
    AliasFrame.place(anchor = "c", relx = .75, rely = .5)

    viewEntryInt = tk.IntVar()
    viewEntries = ttk.Checkbutton(MainFrame, text = 'View all entries', style = 'Toggle.TButton', onvalue = 1, offvalue = 0, variable = viewEntryInt, command = viewFunc)
    viewEntries.pack(pady = 10)

    userWinCanvas.pack()
    userWin.mainloop()
