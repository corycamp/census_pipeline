import pandas as pd


def transform_census_data(raw_data_object):
    """Transforms raw census data into a cleaned format.

    Args:
        raw_data_object (dict): The raw census data fetched from the database.

    Returns:
        pd.DataFrame: The cleaned and transformed census data.
    """
    if not raw_data_object or "data" not in raw_data_object:
        return None

    raw_data = raw_data_object["data"]
    raw_serial_id = raw_data_object["id"]

    # Convert the cleaned data to a pandas DataFrame for easier manipulation
    raw_data_df = pd.DataFrame(raw_data)

    # Drop the first row which contains the original column headers
    cleaned_data_df = raw_data_df.copy()
    cleaned_data_df.columns = cleaned_data_df.iloc[0]
    cleaned_data_df = cleaned_data_df[1:]

    columns_to_drop = [
        # Statistical Bounds and Margins of Error
        "NIC_LB90",
        "NIC_UB90",
        "NIC_MOE",
        "NUI_LB90",
        "NUI_UB90",
        "NUI_MOE",
        "PCTIC_LB90",
        "PCTIC_UB90",
        "PCTIC_MOE",
        "PCTUI_LB90",
        "PCTUI_UB90",
        "PCTUI_MOE",
        "NIPR_LB90",
        "NIPR_UB90",
        "NIPR_MOE",
        # Raw Counts (Use percentages instead to avoid population bias)
        "NIC_PT",
        "NUI_PT",
        # Redundant Text Descriptions
        "AGE_DESC",
        "SEX_DESC",
        "RACE_DESC",
        "IPR_DESC",
        "NAME",
        "STABREV",
        # API Metadata and Query Parameters
        "GEOID",
        "GEOCAT",
    ]

    column_mapping = {
        "NIPR_PT": "target_poverty_count",
        "PCTUI_PT": "feature_pct_uninsured",
        "PCTIC_PT": "feature_pct_insured",
        "AGECAT": "dim_age_category",
        "SEXCAT": "dim_sex_category",
        "RACECAT": "dim_race_category",
        "IPRCAT": "dim_poverty_ratio_category",
        "YEAR": "dim_year",
        "STATE": "dim_state_fips",
        "COUNTY": "dim_county_fips",
    }

    # Fix column names and drop unnecessary columns
    cleaned_data_df.columns.name = None
    cleaned_data_df.drop(columns=["state"], inplace=True)
    cleaned_data_df.drop(columns=columns_to_drop, inplace=True)

    # Map the column names to the desired names
    cleaned_data_df.rename(columns=column_mapping, inplace=True)

    cleaned_data_df["original_serial_id"] = raw_serial_id

    return cleaned_data_df
