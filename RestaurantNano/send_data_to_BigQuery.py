import os
from google.cloud import bigquery
import pandas as pd

# Set the environment variable for Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/kdedge/Downloads/edgecomputingproject-4f22be1ed057.json'

# Create a BigQuery client
client = bigquery.Client()

def get_profile_name(user_id):

    print("Hi from inside get_profile_name")
    """
    Retrieves the ProfileName for a given UserId from BigQuery.
   
    Parameters:
    user_id (str): The UserId to search for.
   
    Returns:
    str: The ProfileName associated with the UserId.
    """
    # Define the dataset and table
    dataset_id = 'reviewsdataset'
    table_id = 'reviews'

    # Construct the SQL query
    query = f"""
    SELECT ProfileName
    FROM `{dataset_id}.{table_id}`
    WHERE UserId = '{user_id}'
    LIMIT 1
    """
   
    # Execute the query
    query_job = client.query(query)
   
    # Retrieve the results
    results = query_job.result()
   
    # Extract the ProfileName from the results
    for row in results:
        return row.ProfileName
   
    # Return a default value if no ProfileName is found
    return "Unknown"


def send_data_to_bigquery(data):

    print("Hi from inside send_data_to_bigquery")
    """
    Sends data to a predefined BigQuery table.
   
    Parameters:
    data (dict): The data to be sent to BigQuery, structured as a dictionary.
    """
    # Define the dataset and table
    project_id = 'edgecomputingproject'
    dataset_id = 'reviewsdataset'
    table_id = 'reviews'
    table_ref = client.dataset(dataset_id).table(table_id)

    # Extract UserId and ProductId from input data
    user_id = data.get("UserId")
    product_id = data.get("ProductId")  


    # Retrieve the ProfileName for the given UserId
    profile_name = get_profile_name(user_id)

    print("Username",profile_name)


    # Merge provided data with static data
    static_data = {
        "Id": 1234,
        "ProfileName": profile_name,
        "HelpfulnessNumerator": 1,
        "HelpfulnessDenominator": 1,
        "Score": 999,
        "Time": 1303862400,
        "Summary": "baaad",
        "Text": "I have bought several of the Vitality canned dog food products and have found them all to be of good quality."
    }

   
    # Merge provided data with static data
    complete_data = {**static_data, **data}
   
    # Convert the data to a DataFrame
    df = pd.DataFrame([complete_data])
   
    # Load data to BigQuery
    job = client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for the job to complete

    print("Data loaded successfully")



example_data = {
"UserId": "A3SGXH7AUHU8GW",
"ProductId": "B001E4KFG0"
}

# Call the function with example datails
send_data_to_bigquery(example_data)
