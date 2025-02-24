import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.conn_params = {
            'dbname': os.getenv('PGDATABASE'),
            'user': os.getenv('PGUSER'),
            'password': os.getenv('PGPASSWORD'),
            'host': os.getenv('PGHOST'),
            'port': os.getenv('PGPORT')
        }

    @contextmanager
    def get_cursor(self):
        conn = psycopg2.connect(**self.conn_params)
        try:
            yield conn.cursor(cursor_factory=RealDictCursor)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def initialize_schema(self):
        with open('schema.sql', 'r') as f:
            schema = f.read()
        with self.get_cursor() as cur:
            cur.execute(schema)

    def get_or_create_user(self, username):
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username)
                VALUES (%s)
                ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
                RETURNING id;
                """,
                (username,)
            )
            result = cur.fetchone()
            return result['id']

    def record_attempt(self, user_id, question_id, correct, time_taken):
        with self.get_cursor() as cur:
            cur.execute(
                """
                INSERT INTO quiz_progress (user_id, question_id, correct, time_taken)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, question_id, correct, time_taken)
            )
            # Update user statistics
            cur.execute(
                """
                INSERT INTO user_statistics (user_id, total_attempts, correct_answers, total_time, last_quiz_date)
                VALUES (%s, 1, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) DO UPDATE SET
                    total_attempts = user_statistics.total_attempts + 1,
                    correct_answers = user_statistics.correct_answers + %s,
                    total_time = user_statistics.total_time + %s,
                    last_quiz_date = CURRENT_TIMESTAMP;
                """,
                (user_id, 1 if correct else 0, time_taken, 1 if correct else 0, time_taken)
            )

    def get_user_statistics(self, user_id):
        with self.get_cursor() as cur:
            cur.execute(
                """
                SELECT * FROM user_statistics WHERE user_id = %s
                """,
                (user_id,)
            )
            return cur.fetchone()
