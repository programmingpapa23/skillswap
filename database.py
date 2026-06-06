import sqlite3

def get_db_connection():
    """Establishes connection to SkillExchangeDB using sqlite3.Row [cite: 433, 434]"""
    conn = sqlite3.connect('SkillExchangeDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the relational database schema based on OOSE design [cite: 421]"""
    conn = get_db_connection()
    
    # Create User Table (Static Structural Design) [cite: 133]
    conn.execute('''
        CREATE TABLE IF NOT EXISTS User (
            userId INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            passwordHash VARCHAR(255) NOT NULL,
            bio TEXT,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Skill Table 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Skill (
            skillId INTEGER PRIMARY KEY AUTOINCREMENT,
            skillName VARCHAR(100) NOT NULL,
            category VARCHAR(100)
        )
    ''')

    # Create UserOffer (Teach) association table 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS UserOffer (
            offerId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER,
            skillId INTEGER,
            level VARCHAR(50),
            available INTEGER DEFAULT 1,
            FOREIGN KEY(userId) REFERENCES User(userId),
            FOREIGN KEY(skillId) REFERENCES Skill(skillId)
        )
    ''')

    # Create RequestPreference (Learn) association table 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS UserRequestPreference (
            requestPrefId INTEGER PRIMARY KEY AUTOINCREMENT,
            userId INTEGER,
            skillId INTEGER,
            levelNeeded VARCHAR(50),
            FOREIGN KEY(userId) REFERENCES User(userId),
            FOREIGN KEY(skillId) REFERENCES Skill(skillId)
        )
    ''')
    skills = [
        ('Python Programming', 'Programming'),
        ('Machine Learning', 'Data Science'),
        ('Web Development', 'Software Engineering'),
        ('UI/UX Design', 'Design'),
        ('Public Speaking', 'Communication'),
        ('Database Management', 'Systems')
    ]
    
    # Check if Skill table is empty before inserting to avoid duplicates
    existing = conn.execute('SELECT COUNT(*) FROM Skill').fetchone()[0]
    if existing == 0:
        conn.executemany('''
            INSERT INTO Skill (skillName, category) VALUES (?, ?)
        ''', skills)
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ExchangeRequest (
            exchangeId INTEGER PRIMARY KEY AUTOINCREMENT,
            senderId INTEGER NOT NULL,
            receiverId INTEGER NOT NULL,
            skillId INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (senderId) REFERENCES User (userId),
            FOREIGN KEY (receiverId) REFERENCES User (userId),
            FOREIGN KEY (skillId) REFERENCES Skill (skillId)
        )
    ''')
    
    conn.commit()
    conn.close()