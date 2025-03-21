import sqlite3


def create_table():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    # Connect to SQLite database (creates file if not exists)
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS short_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        short_code TEXT UNIQUE NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        access_count INTEGER DEFAULT 0
    );
    ''')

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_table()