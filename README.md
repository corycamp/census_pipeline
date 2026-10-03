# Census Data Pipeline

Reading census data provided by the U.S. Census Bureau's Small Area Health Insurance Estimates (SAHIE) program API, that shows single year estimates of health insurance coverage status for all counties in the U.S. For the purpose of this project, data cleaning and standardization will be done for the year 2020, however, the data format and code functionality is appliable earlier years.

## Tools used

- PostgreSQL
- Pandas
- Python

## Data flow

When the pipeline runs, the full dataset will be gathered from the API. Seeing as this is existing data, if the orginal raw data exists from a previous initial load, no new instances need to be gathered.

- Pull data from cenus.gov API
- Read data into Original Table on initial load
- Clean and Standardized data pulled from Original into Formatted Table

## Data Cleaning

Converted the 2D array coming from the API into a panda dataframe for easier manipulation. After converting, the following changes were done:

- Reformatted the data to have the first array from the API be the column names

- Added a original_serial_id column to match the serial number of the transformed data with the raw data in the Postgres table for tracking

- Removed duplicate state columns and renamed the county column to county_fips_code (Five digit unique numerical identifier used to identify U.S. counties)

- Kept the abbreviations for the states, renamed that column to 'states'.

- Removed the time and country column
