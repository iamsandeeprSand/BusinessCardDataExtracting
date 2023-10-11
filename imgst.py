import streamlit as st
from ocrimg import upload_database, extracted_data, show_database

# ------------------------------------------setting page configuration in streamlit---------------------------------------------------------
st.set_page_config(page_title='Bizcardx Extraction', layout="wide")



data_extraction, database_side = st.tabs(
    ['Uploading and Viewing', 'Stored Data'])
file_name = 'ocrfile'
with data_extraction:
    
    st.subheader(':violet[Upoload an image file to extract data]')
    # ---------------------------------------------- Uploading file to streamlit app ------------------------------------------------------
    uploaded = st.file_uploader('Choose an Image file')
    # --------------------------------------- Convert binary values of image to IMAGE ---------------------------------------------------
    if uploaded is not None:
        with open(f'{file_name}.png', 'wb') as f:
            f.write(uploaded.getvalue())
        # ----------------------------------------Extracting data from image (Image view)-------------------------------------------------
        st.subheader(':green[Image view of Data]')
        if st.button('Extract Data from Image'):
            extracted = extracted_data(f'{file_name}.png')
            st.image(extracted)

        # ----------------------------------------upload data to database----------------------------------------------------------------
        st.subheader(':violet[Upload extracted to Database]')
        if st.button('Upload data'):
            upload_database(f'{file_name}.png')
            st.success('Data uploaded to Database successfully!', icon="✅")
# --------------------------------------------getting data from database and storing in df variable---------------------------------------
df = show_database()
with database_side:
    
    # ----------------------------------------Showing all datas in database---------------------------------------------------------------
    st.title(':violet[All Data in Database]')
    if st.button('Show All'):
        st.dataframe(df)
    