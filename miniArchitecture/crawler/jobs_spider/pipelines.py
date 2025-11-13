import json
import os
import sqlite3


class SQLitePipeline:
    def open_spider(self, spider):
        db_path = os.path.join("data", "jobs.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS jobs (
                url TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                experience TEXT,
                tags TEXT,
                skills TEXT,
                description TEXT,
                scraped_at TEXT
            )
            '''
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        def _serialize(value):
            if value is None:
                return None
            if isinstance(value, (list, dict)):
                return json.dumps(value, ensure_ascii=False)
            return value

        self.cur.execute(
            '''
            INSERT OR REPLACE INTO jobs (
                url,
                title,
                company,
                location,
                salary,
                experience,
                tags,
                skills,
                description,
                scraped_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                item.get("url"),
                item.get("title"),
                item.get("company"),
                item.get("location"),
                item.get("salary"),
                _serialize(item.get("experience")),
                _serialize(item.get("tags")),
                _serialize(item.get("skills")),
                item.get("description"),
                item.get("scraped_at"),
            ),
        )
        self.conn.commit()
        return item