import psycopg2
import os
import json
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class table_names(Enum):
    ORIGINAL_TABLE = "original_table"


class DBService:
    sql_mapping = {
        "create_original_table": f"CREATE TABLE IF NOT EXISTS {table_names.ORIGINAL_TABLE.value} (id SERIAL PRIMARY KEY, data JSONB NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "create_cleaned_table": "CREATE TABLE IF NOT EXISTS cleaned_census_data (id SERIAL PRIMARY KEY, data JSONB NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
    }

    def __init__(self):
        self.conn_string = f"dbname='{os.getenv('POSTGRES_DB')}' user='{os.getenv('POSTGRES_USER')}' password='{os.getenv('POSTGRES_PASSWORD')}' host='{os.getenv('POSTGRES_HOST')}' port='{os.getenv('POSTGRES_PORT')}'"
        self.get_db_connection()

    def get_db_connection(self):
        try:
            self.conn = psycopg2.connect(self.conn_string)
            print("Database service initialized successfully.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise e

    def close_db_connection(self):
        if self.conn:
            self.conn.close()

    async def create_table(self, sql_key, data):
        try:
            conn = self.conn
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute(self.sql_mapping[sql_key], data)
                    print("Table created successfully")
                    await self.insert_data(
                        f"INSERT INTO {table_names.ORIGINAL_TABLE.value} (data) VALUES (%s);",
                        data,
                    )
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")

    async def insert_data(self, sql_function, data):
        try:
            conn = self.conn
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_function, (json.dumps(data),))
                    print("Data inserted successfully")
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")

    async def fetch_raw_census_data(self):
        try:
            conn = self.conn
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"SELECT * FROM {table_names.ORIGINAL_TABLE.value} WHERE created_at = (SELECT MAX(created_at) FROM {table_names.ORIGINAL_TABLE.value});"
                    )
                    rows = cursor.fetchall()
                    return {"id": rows[0][0], "data": rows[0][1]} if rows else {}
        except psycopg2.Error as e:
            print(f"Error fetching raw census data: {e}")
            return []

    async def load_clean_data_into_db(self, cleaned_data):
        try:
            conn = self.conn
            if conn:
                with conn.cursor() as cursor:
                    query = """
                        INSERT INTO cleaned_census_data (
                            target_poverty_count,
                            feature_pct_uninsured,
                            feature_pct_insured,
                            dim_age_category,
                            dim_sex_category,
                            dim_race_category,
                            dim_poverty_ratio_category,
                            dim_year,
                            dim_state_fips,
                            dim_county_fips,
                            time,
                            original_serial_id
                        ) VALUES %s;
                    """
                    columns = list(cleaned_data.columns)
                    data_tuples = [tuple(x) for x in cleaned_data.values]
                    cursor.execute(self.sql_mapping["create_cleaned_table"])
                    cursor.execute(
                        query,
                        data_tuples,
                    )
                    print("Cleaned data inserted successfully")
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error loading cleaned data into the database: {e}")


# Example usage:
# db_service = DBService()
# conn = db_service.get_db_connection()
# if conn:
#     with conn.cursor() as cursor:
#         print("Database connection successful")
#     conn.close()
