# Import the DataAPIClient from the astrapy package for interacting with Astra DB
from astrapy import DataAPIClient

# Import constants for authentication and endpoint configuration
from constants import ASTRA_DB_TOKEN, ASTRA_DB_ENDPOINT

# Import Streamlit for caching resources and displaying UI
import streamlit as st
import os

# Cache the Astra DB client resource to avoid re-initializing on every rerun
@st.cache_resource
def get_astra_client():
    """
    Initializes and returns the Astra DB database client using the provided
    token and endpoint from the constants module. The result is cached by Streamlit.
    """
    client = DataAPIClient(ASTRA_DB_TOKEN)  # Create a DataAPIClient instance with the token
    db = client.get_database_by_api_endpoint(ASTRA_DB_ENDPOINT)  # Connect to the database using the endpoint
    return db

# Initialize the Astra DB client (cached)
db = get_astra_client()

# List of required collection names in the database
db_collections = ['personal_data', 'notes']

# Ensure that each required collection exists in the database
for collection in db_collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)  # Create the collection if it does not exist

# Get references to the specific collections for later use
personal_data_collection = db.get_collection('personal_data')
notes_collection = db.get_collection('notes')
