import streamlit as st
import pandas as pd
import psycopg2
from ocrimg import upload_database, extracted_data, show_database

# ------------------------------------------setting page configuration in streamlit---------------------------------------------------------
st.set_page_config(page_title='Bizcardx Extraction', layout="wide")



data_extraction, database_side, Modify = st.tabs(
    ['Uploading and Viewing', 'Stored Data', 'Modify Data'])
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
    
conn = psycopg2.connect(host="localhost",user="postgres",password="sandeep",port=5432,database="data")
cursor = conn.cursor()

#if selected == "Modify":
with Modify:
    st.title(':violet[Modify Data in Database]')
    col1,col2,col3 = st.columns([3,3,2])
    col2.markdown("## Alter or Delete the data here")
    column1,column2 = st.columns(2,gap="large")
    try:
        with column1:
            cursor.execute("SELECT name FROM mytable")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            cursor.execute("select company_name,name,designation,contact_number,mail_id,website_link,address from mytable WHERE name = %s",
                            (selected_card,))
            result = cursor.fetchone()

            # DISPLAYING ALL THE INFORMATIONS
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            address = st.text_input("address", result[6])
           # city = st.text_input("City", result[7])
           # state = st.text_input("State", result[8])
           # pin_code = st.text_input("Pin_Code", result[9])

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                cursor.execute("""UPDATE mytable SET company_name=%s,name=%s,designation=%s,contact_number=%s,mail_id=%s,website_link=%s,address=%s
                                    WHERE name=%s""", (company_name,card_holder,designation,mobile_number,email,website,address,selected_card))
                conn.commit()
                st.success("Information updated in database successfully.")

        with column2:
            cursor.execute("SELECT name FROM mytable")
            result = cursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes Delete Business Card"):
                cursor.execute(f"DELETE FROM mytable WHERE name='{selected_card}'")
                conn.commit()
                st.success("Business card information deleted from database.")
    except:
        st.warning("There is no data available in the database")

    if st.button("View updated data"):
        cursor.execute("select company_name,name,designation,contact_number,mail_id,website_link,address from mytable")
        updated_df = pd.DataFrame(cursor.fetchall(),columns=["Company_Name","name","Designation","Mobile_Number","Email","Website","Address"])
        st.write(updated_df)
