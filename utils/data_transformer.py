import pandas as pd

def transform_census_data(raw_data_object):
    """Transforms raw census data into a cleaned format.

    Args:
        raw_data_object (dict): The raw census data fetched from the database.

    Returns:
        pd.DataFrame: The cleaned and transformed census data.
    """
    if not raw_data_object or 'data' not in raw_data_object:
        return None

    raw_data = raw_data_object['data']
    raw_serial_id = raw_data_object['id']

    # Convert the cleaned data to a pandas DataFrame for easier manipulation
    raw_data_df = pd.DataFrame(raw_data)

    # Drop the first row which contains the original column headers
    cleaned_data_df = raw_data_df.copy()
    cleaned_data_df.columns = cleaned_data_df.iloc[0]
    cleaned_data_df = cleaned_data_df[1:]
    cleaned_data_df.columns.name = None
    cleaned_data_df.drop(columns=['state'], inplace=True)
    cleaned_data_df.columns = cleaned_data_df.columns.str.lower()

    cleaned_data_df['original_serial_id'] = raw_serial_id
    cleaned_data_df['state'] = cleaned_data_df['stabrev'].str.upper()
    cleaned_data_df['county_fips_code'] = cleaned_data_df['county']
    cleaned_data_df.drop(columns=['stabrev','time','county'], inplace=True)

    print(cleaned_data_df.head(2))


    return cleaned_data_df