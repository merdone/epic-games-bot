import sqlite3


class Database:
    def __init__(self, db_file="games.db"):
        self.connection = sqlite3.connect(db_file)
        self.db_name = db_file
        self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self) -> None:
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    is_active BOOLEAN DEFAULT 1
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    image_url TEXT,
                    link TEXT,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    was_sent BOOLEAN DEFAULT 0
                )
            """)

    def add_user(self, user_id: int) -> None:
        """add user to database"""
        with self.connection:
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
            )
            self.cursor.execute(
                "UPDATE users SET is_active = 1 WHERE user_id = ?", (user_id,)
            )

    def set_active(self, user_id: int, is_active: bool) -> None:
        """change user status"""
        with self.connection:
            self.cursor.execute(
                "UPDATE users SET is_active = ? WHERE user_id = ?", (is_active, user_id)
            )

    def get_users(self) -> list:
        """get all active users for subscription"""
        with self.connection:
            return self.cursor.execute(
                "SELECT user_id FROM users WHERE is_active = 1"
            ).fetchall()

    def game_exists(self, game_id: str) -> bool:
        """check is game in database"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT game_id from games WHERE game_id = ?", (game_id,)
            ).fetchall()
        return bool(result)

    def user_exists(self, user_id) -> bool:
        """check is user in database"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT user_id from users WHERE user_id = ?", (user_id,)
            ).fetchall()
        return bool(result)

    def add_game(self, game_info: dict) -> None:
        """add game to database"""
        with self.connection:
            self.cursor.execute("""
                INSERT OR IGNORE INTO games 
                (game_id, title, description, image_url, link, start_date, end_date, was_sent)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, (
                game_info['game_id'],
                game_info['name'],
                game_info['description'],
                game_info['image_url'],
                game_info['link'],
                game_info['start_date'],
                game_info['end_date']
            ))

    def get_active_games(self) -> list:
        """return list of active games"""
        with self.connection:
            return self.cursor.execute("""
                SELECT title, description, link, image_url, start_date, end_date
                FROM games 
                WHERE end_date > CURRENT_TIMESTAMP
            """).fetchall()

    def get_active_users(self) -> list:
        """return list of all active users"""
        with self.connection:
            return self.cursor.execute("""
            SELECT user_id from users WHERE is_active = 1
            """).fetchall()
