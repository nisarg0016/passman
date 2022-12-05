import tkinter as tk, functions as loginMethod, sqlite3, os, platformdirs, platform
from tkinter import ttk


def erase(entry, placeholder, root, loginUsername, loginPassword, event=None):
    if entry.get() == placeholder:
        entry.delete(0, 'end')
    if placeholder == "Enter your password":
        entry["show"] = "*"
    root.bind("<Return>", lambda event: loginMethod.loginToMain(root, crsr, loginUsername, loginPassword))

def add(entry, placeholder, root, event=None):
    if placeholder == "Enter your password" and entry.get() == '':
        entry["show"] = ""
    if entry.get() == '':
        entry.insert(0, placeholder)
        root.bind("<Return>")

def bindToEntry(entry, placeholder, root, loginUsername, loginPassword):
    add(entry, placeholder, root)
    entry.bind('<FocusIn>', lambda event: erase(entry, placeholder, root, loginUsername, loginPassword))
    entry.bind('<FocusOut>', lambda event: add(entry, placeholder, root))


path = ''
if platform.system() == 'Linux':
    path = f"{platformdirs.user_data_dir()}/passman"
elif platform.system() == 'Windows':
    path = f"{platformdirs.user_data_dir()}\\passman"
if not os.path.exists(path):
    os.makedirs(path)
conn = ''
if platform.system() == 'Linux':
    conn = sqlite3.connect(f"{path}/master.db")
elif platform.system() == 'Windows':
    conn = sqlite3.connect(f"{path}\\master.db")
crsr = conn.cursor()
crsr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='master';")
if crsr.fetchone()[0] != 1:
    crsr.execute("CREATE TABLE master (username VARCHAR(100), password VARCHAR(100));")


def main():
    root = tk.Tk()
    root.title('PassMan')

    rootCanvas = tk.Canvas(root, height=533, width=800)

    mainFrame = ttk.Frame(root)
    mainFrame.pack(fill = "both", expand = True)
    mainFrame.place(anchor = "c", relx = .5, rely = .5)

    root.tk.call("source", f"{os.path.dirname(os.path.realpath(__file__))}/themes/azure.tcl")
    root.tk.call("set_theme", "dark")
    root.iconbitmap(f'{os.path.dirname(os.path.realpath(__file__))}/assets/icon.ico')

    loginUsername, loginPassword = tk.StringVar(), tk.StringVar()

    usernameEntry = ttk.Entry(mainFrame, textvariable = loginUsername)
    usernameEntry.pack(pady = 5)
    bindToEntry(usernameEntry, 'Enter your username', root, loginUsername, loginPassword)
    passwordEntry = ttk.Entry(mainFrame, textvariable = loginPassword)
    passwordEntry.pack(pady = 5)
    bindToEntry(passwordEntry, 'Enter your password', root, loginUsername, loginPassword)
    ButtonFrame = ttk.Frame(mainFrame)
    loginButton = ttk.Button(ButtonFrame, text = "Login", style = "Accent.TButton", command = lambda: loginMethod.loginToMain(root, crsr, loginUsername, loginPassword))
    loginButton.grid(row = 0, column = 0, padx = 10, pady = 10)
    createUser = ttk.Button(ButtonFrame, text = "Create a new user", command = lambda: loginMethod.createNewUser(root, crsr, conn, loginUsername, loginPassword))
    createUser.grid(row = 0, column = 1, padx = 10, pady = 10)
    ButtonFrame.pack()

    rootCanvas.pack()

    root.mainloop()

if __name__ == "__main__":
    main()