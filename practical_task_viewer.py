import streamlit as st
from supabase import create_client, Client
import os

# Initialize Supabase client
try:
    SUPABASE_URL = os.environ["SUPABASE_URL"]
    SUPABASE_KEY = os.environ["SUPABASE_KEY"]
except KeyError:
    st.error("Environment variables SUPABASE_URL or SUPABASE_KEY are not set.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit App Title
st.title("Batch Number PDF Viewer")

# Sidebar or main input field for batch number
batch_number = st.text_input("Enter Batch Number:", "")

# Search button
if st.button("Search"):
    if batch_number:
        # Construct the file name
        file_name = f"{batch_number}.pdf"
        
        try:
            # Get the public URL for the file
            response = supabase.storage.from_("test_prac_scans").get_public_url(file_name)

            if isinstance(response, dict) and "publicUrl" in response:
                file_url = response["publicUrl"]
                st.success("File found!")
                st.write(f"Public URL: [View PDF]({file_url})")
            elif isinstance(response, str):  # If the response is already a URL
                st.success("File found!")
                st.write(f"Public URL: [View PDF]({response})")
            else:
                st.error("File not found in the bucket.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a batch number.")
