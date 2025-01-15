import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class DBClient:
  def __init__(self):
    self.connection = None
    self.cursor = None

  def connect(self):
    """Establish the connection to the database"""
    if self.connection is None or self.connection.closed:
      try:
        self.connection = psycopg2.connect(
          host=DB_HOST,
          port=DB_PORT,
          dbname=DB_NAME,
          user=DB_USER,
          password=DB_PASSWORD
        )
        self.cursor = self.connection.cursor()
        print("Connected to the database")
      except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

  def execute_query(self, query, params=None):
    """Execute a SQL query and return the results"""
    try:
      self.connect()  # Ensure we are connected
      if params:
        self.cursor.execute(query, params)
      else:
        self.cursor.execute(query)

      # Commit the transaction if it's a data-modifying query (INSERT, UPDATE, DELETE)
      if query.strip().lower().startswith(('insert', 'update', 'delete')):
        self.connection.commit()

      # Fetch all rows from the result if it's a SELECT query
      if query.strip().lower().startswith('select'):
        return self.cursor.fetchall()

    except Exception as e:
      print(f"Error executing query: {e}")
      raise

  def close(self):
    """Close the connection and cursor"""
    if self.cursor:
      self.cursor.close()
    if self.connection:
      self.connection.close()
    print("Connection closed")
  
  def __enter__(self):
    """Called when entering the context (with block)"""
    self.connect()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    """Called when exiting the context (with block)"""
    self.close()

# Export the DBClient instance to be used elsewhere
db_client = DBClient()
