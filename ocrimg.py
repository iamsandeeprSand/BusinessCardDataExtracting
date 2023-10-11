import easyocr
import cv2
import pandas as pd
import re
import psycopg2

# -------------------------------------------Establishing connection to database-------------------------------------------------------
conn = psycopg2.connect(host="localhost",user="postgres",password="sandeep",port=5432,database="data")
cursor = conn.cursor()
# -----------------------------------Creating table in sql------------------------------------------------------------------------------
create_table = 'CREATE TABLE IF NOT EXISTS mytable (ID SERIAL PRIMARY KEY, Name TEXT, Designation TEXT,Company_name TEXT,Address TEXT,Contact_number TEXT,Mail_id TEXT,Website_link TEXT,Image BYTEA);'
cursor.execute(create_table)
conn.commit()


def upload_database(image):
    # ----------------------------------------Getting data from image using easyocr------------------------------------------------------
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch') 
    # -----------------------------------------converting got data to single string------------------------------------------------------
    data = []
    j = 0
    for i in result:
        data.append(result[j][1])
        j += 1
    data
    org_reg = " ".join(data)
    reg = " ".join(data)
    # ------------------------------------------Separating EMAIL---------------------------------------------------------------------------
    email_regex = re.compile(r'''(
	[a-zA-z0-9]+
	@
	[a-zA-z0-9]+
	\.[a-zA-Z]{2,10}
	)''', re.VERBOSE)
    email = ''
    for i in email_regex.findall(reg):
        email += i
        reg = reg.replace(i, '')
    # ------------------------------------------Separating phone number---------------------------------------------------------------------------
    phoneNumber_regex = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    phone_no = ''
    for numbers in phoneNumber_regex.findall(reg):
        phone_no = phone_no + ' ' + numbers
        reg = reg.replace(numbers, '')
    # ------------------------------------------Separating Address---------------------------------------------------------------------------
    address_regex = re.compile(r'\d{2,4}.+\d{6}')
    address = ''
    for addr in address_regex.findall(reg):
        address += addr
        reg = reg.replace(addr, '')
    # ------------------------------------------Separating website link---------------------------------------------------------------------------
    link_regex = re.compile(r'www.?[\w.]+', re.IGNORECASE)
    link = ''
    for lin in link_regex.findall(reg):
        link += lin
        reg = reg.replace(lin, '')
    # ------------------------------------------Separating Designation (only suitable for this dataset)----------------------------------------
    desig_list = ['DATA MANAGER', 'CEO & FOUNDER',
                  'General Manager', 'Marketing Executive', 'Technical Manager']
    designation = ''
    for i in desig_list:
        if re.search(i, reg):
            designation += i
            reg = reg.replace(i, '')
    # ------------------------------------------Separating Company name (only suitable for this dataset)--------------------------------------
    # ----------------------------------to overcome this combine all the three datas to single column ----------------------------------------
    comp_name_list = ['selva digitals', 'GLOBAL INSURANCE',
                      'BORCELLE AIRLINES', 'Family Restaurant', 'Sun Electricals']
    company_name = ''
    for i in comp_name_list:
        if re.search(i, reg, flags=re.IGNORECASE):
            company_name += i
            reg = reg.replace(i, '')
    name = reg.strip()

    # ------------------------------------reading and getting byte values of image-----------------------------------------------------------
    with open(image, 'rb') as file:
        blobimg = file.read()
    # -----------------------------------------inserting data into table---------------------------------------------------------------------
    image_insert = 'INSERT INTO mytable (Name, Designation, Company_name, Address, Contact_number,Mail_id,Website_link,Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(image_insert, (name, designation, company_name,
                   address, phone_no, email, link, blobimg))
    conn.commit()


def extracted_data(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    img = cv2.imread(image)
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (204, 0, 34), 5)
        img = cv2.putText(img, text, top_left, font, 0.8,
                          (255, 255, 255), 2, cv2.LINE_AA)

    # plt.figure(figsize=(10, 10))
    # plt.imshow(img)
    # plt.show()
    return img


def show_database():
    new_df = cursor.execute("SELECT * FROM mytable;")
    all = cursor.fetchall()
    df = pd.DataFrame(all)
    return df