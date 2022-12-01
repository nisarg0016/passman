import sqlite3, os, platformdirs
from functions import *

if __name__ == "__main__":
    cls()
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
    crsr.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='master';")
    if crsr.fetchone()[0] != 1:
        crsr.execute("CREATE TABLE master (username VARCHAR(100), password VARCHAR(100));")
        print('''--------------WELCOME TO THE PASSWORD MANAGER-----------------''')
        master_select(crsr, conn)
    else:
        print('''--------------WELCOME TO THE PASSWORD MANAGER-----------------''')
        master_select(crsr, conn)
