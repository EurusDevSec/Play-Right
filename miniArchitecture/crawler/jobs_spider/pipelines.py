import sqlite3
import os

class SQLitePipeline:
    def open_spider(self, spider):
       
        db_path = os.path.join('data', 'jobs.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                url TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                description TEXT,
                scraped_at TEXT
            )
        ''')

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute('''
            INSERT OR REPLACE INTO jobs (url, title, company, location, salary, description, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('url'),
            item.get('title'),
            item.get('company'),
            item.get('location'),
            item.get('salary'),
            item.get('description'),
            item.get('scraped_at')
        ))
        self.conn.commit()
        return item