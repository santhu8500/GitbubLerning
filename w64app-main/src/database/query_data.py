import pandas as pd
from database.db_client import db_client

def load_data_to_dataframe(query):
  with db_client as client:
    # Execute the query
    results = client.execute_query(query)

    # Extract column names from the cursor description
    column_names = [desc[0] for desc in client.cursor.description]

    # Load results into a Pandas DataFrame
    df = pd.DataFrame(results, columns=column_names)

  return df
