#Database Management
import sqlite3
import datetime
import os
from pathlib import Path
from config import DATABASE, DB_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DB_PATH
        self.connection = None
        self.create_database()
    
    def create_records_folder(self):
        try:
            Path(DATABASE['FOLDER']).mkdir(parents=True, exist_ok=True)
            print(f"Records folder ready: '{DATABASE['FOLDER']}'")
            return True
        except Exception as e:
            print(f"Error creating records folder: {e}")
            return False
    
    def create_database(self):
        try:
            if not self.create_records_folder():
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check for existing table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='measurements'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                self._update_table_structure(cursor, conn)
            else:
                self._create_new_tables(cursor)
            
            conn.commit()
            conn.close()
            print(f"Database '{self.db_path}' ready")
            return True
            
        except Exception as e:
            print(f"Database creation error: {e}")
            return False
    
    def _update_table_structure(self, cursor, conn):
        cursor.execute("PRAGMA table_info(measurements)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        # Add missing columns
        updates = [
            ("angle", "INTEGER DEFAULT 90"),
            ("direction", "TEXT DEFAULT 'FRONT'"),
            ("direction_code", "INTEGER DEFAULT 3"),
            ("scan_mode", "TEXT DEFAULT 'AUTO'")
        ]
        
        for column_name, column_def in updates:
            if column_name not in column_names:
                print(f"Adding '{column_name}' column...")
                cursor.execute(f"ALTER TABLE measurements ADD COLUMN {column_name} {column_def}")
                conn.commit()
        
        print("Table structure updated")
    
    def _create_new_tables(self, cursor):
        # Measurements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            distance REAL NOT NULL,
            angle INTEGER NOT NULL,
            direction TEXT NOT NULL,
            direction_code INTEGER NOT NULL,
            alert_status INTEGER NOT NULL,
            scan_mode TEXT DEFAULT 'AUTO'
        )
        ''')
        
        # System logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            event_type TEXT NOT NULL,
            description TEXT,
            system_mode TEXT
        )
        ''')
        
        print("New tables created")
    
    def get_connection(self):
        max_retries = DATABASE['MAX_RETRIES']
        
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(self.db_path, timeout=DATABASE['CONNECTION_TIMEOUT'])
                return conn
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(1)
        
        print("Failed to establish database connection")
        return None
    
    def save_measurement(self, distance, angle, direction, direction_code, alert_status, scan_mode):
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            now = datetime.datetime.now()
            
            cursor.execute(
                "INSERT INTO measurements (date_time, distance, angle, direction, direction_code, alert_status, scan_mode) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (now.strftime('%Y-%m-%d %H:%M:%S'), distance, angle, direction, direction_code, alert_status, scan_mode)
            )
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Data saving error: {e}")
            return False
        finally:
            conn.close()
    
    def log_system_event(self, event_type, description, system_mode):
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            now = datetime.datetime.now()
            
            cursor.execute(
                "INSERT INTO system_logs (date_time, event_type, description, system_mode) VALUES (?, ?, ?, ?)",
                (now.strftime('%Y-%m-%d %H:%M:%S'), event_type, description, system_mode)
            )
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Event logging error: {e}")
            return False
        finally:
            conn.close()
    
    def get_recent_measurements(self, limit=8):
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT date_time, distance, angle, direction, alert_status, scan_mode
            FROM measurements
            ORDER BY id DESC
            LIMIT ?
            """, (limit,))
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error fetching measurements: {e}")
            return []
        finally:
            conn.close()
    
    def get_statistics(self):
        conn = self.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            stats = {}
            
            # Total record count
            cursor.execute("SELECT COUNT(*) FROM measurements")
            stats['total_records'] = cursor.fetchone()[0]
            
            # Alert count
            cursor.execute("SELECT COUNT(*) FROM measurements WHERE alert_status = 1")
            stats['alert_count'] = cursor.fetchone()[0]
            
            # Average distance
            cursor.execute("SELECT AVG(distance) FROM measurements")
            avg_distance = cursor.fetchone()[0]
            stats['avg_distance'] = round(avg_distance, 2) if avg_distance else 0
            
            # Danger zones
            cursor.execute("""
            SELECT direction, COUNT(*) 
            FROM measurements 
            WHERE alert_status = 1 
            GROUP BY direction 
            ORDER BY COUNT(*) DESC
            """)
            stats['danger_zones'] = cursor.fetchall()
            
            return stats
            
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {}
        finally:
            conn.close()
    
    def cleanup_old_records(self, days=30):
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
            
            cursor.execute(
                "DELETE FROM measurements WHERE date_time < ?",
                (cutoff_date.strftime('%Y-%m-%d %H:%M:%S'),)
            )
            
            cursor.execute(
                "DELETE FROM system_logs WHERE date_time < ?",
                (cutoff_date.strftime('%Y-%m-%d %H:%M:%S'),)
            )
            
            conn.commit()
            print(f"Cleaned records older than {days} days")
            return True
            
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
        finally:
            conn.close()