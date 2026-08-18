import sqlite3

DATABASE = "database.db"
#fucnction to establish databasea connection
def get_db():
    conn = sqlite3.connect(DATABASE)  
    conn.row_factory = sqlite3.Row
    return conn


#function to initialize the database 
def init_db():
    conn = get_db()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE, 
            password_hash TEXT NOT NULL,
            token TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()
