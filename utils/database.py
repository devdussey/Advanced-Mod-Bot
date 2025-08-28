import aiosqlite
import json

DB_NAME = "database.sqlite3"


# Initialize tables
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Warnings table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            moderator_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Jail table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS jail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            roles_json TEXT NOT NULL,
            moderator_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Settings table (for storing jail role etc.)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        await db.commit()


# -----------------------------
# Warning system helpers
# -----------------------------
async def add_warning(user_id: int, moderator_id: int, reason: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO warnings (user_id, moderator_id, reason) VALUES (?, ?, ?)",
            (user_id, moderator_id, reason))
        await db.commit()


async def get_warnings(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM warnings WHERE user_id = ?",
                                  (user_id, ))
        rows = await cursor.fetchall()
        return rows


# -----------------------------
# Jail system helpers
# -----------------------------
async def jail_user(user_id: int, roles: list[int], moderator_id: int,
                    reason: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO jail (user_id, roles_json, moderator_id, reason) VALUES (?, ?, ?, ?)",
            (user_id, json.dumps(roles), moderator_id))
