from api.census_client import CensusClient
from services.db_service import DBService
from utils.data_transformer import transform_census_data

import asyncio

def setup_data_connection():
    print('Setting up database and client connection...')
    db_service = DBService()
    census_client = CensusClient()

    return [db_service, census_client]

async def save_raw_data(db_service, census_client):
    census_data = await asyncio.to_thread(census_client.get_census_data)
    print('Census data fetched successfully.')
    
    print('Inserting data into the database...')
    await db_service.create_table('create_original_table', census_data)
    db_service.close_db_connection()
    

async def main():
   try:
       print('########## Initializing ##########\n')
       db_service, census_client = setup_data_connection()
    #    await save_raw_data(db_service, census_client)

       print('\n########## Initialization complete ##########\n')

       print('\n########## Cleaning Data ##########\n')
       raw_data = await db_service.fetch_raw_census_data()
       
       if not raw_data:
           raise ValueError("No raw data found in the database.")

       # Perform data cleaning here
       cleaned_data = transform_census_data(raw_data)
       print(f'Cleaned data: {cleaned_data.head(2)}')

       if cleaned_data.empty:
           raise ValueError("No cleaned data available after transformation.")
       
       print('\n########## Inserting Cleaned Data ##########\n')
    #    await db_service.create_table('create_cleaned_table', cleaned_data)
    #    print('Cleaned data inserted successfully.')

       db_service.close_db_connection()
       print('\n########## Connection closed successfully ##########\n')


   except Exception as e:
       print(f"An error occurred: {e}")


if __name__ == '__main__':
    asyncio.run(main())