# Business Card Information Extraction with Streamlit and easyOCR

This project aims to create a Streamlit application for extracting relevant information from uploaded business card images using easyOCR. The extracted details, including company name, cardholder name, designation, contact details, and address, will be displayed in an intuitive graphical user interface. Additionally, the application allows users to store this information in a database.

## Technologies

1. **easyOCR:** Python library for optical character recognition.
2. **Streamlit GUI:** Framework for creating interactive web applications with Python.
3. **SQL:** Database management system for storing extracted business card information.
4. **Data Extraction:** Techniques for processing images and extracting text.

## Steps

### 1. Installation
Install Python, Streamlit, easyOCR, and a database system like PostgreSQL.

### 2. User Interface Design
Design a user-friendly interface with Streamlit allowing users to upload business card images and extract their information using widgets like file uploaders and buttons.

### 3. Image Processing and OCR
Utilize easyOCR for extracting relevant details from uploaded business card images. Implement image processing techniques to enhance image quality if necessary.

### 4. Display Extracted Information
Present the extracted information in a structured manner within the Streamlit GUI using tables, text boxes, and labels.

### 5. Database Integration
Use SQL (PostgreSQL) to store the extracted information and associated images. Implement functionalities like data insertion, retrieval, updates, and deletion through the Streamlit interface.

### 6. Testing
Thoroughly test the application's functionality, ensuring proper operation. Run the application locally using `streamlit run imgst.py` in the terminal.

### 7. Continuous Improvement
Continuously enhance the application by adding features, optimizing code, and ensuring security with user authentication and authorization.

## Results

The final application will be a Streamlit-based tool that allows users to upload business card images and extract relevant information using easyOCR. Extracted details will include company name, cardholder name, designation, contact information, and address details, displayed in an organized manner within the application's GUI.

Users can store this extracted information in a database along with the uploaded images. The database can manage multiple entries, providing a repository for efficiently managing business card information.

The project demands skills in image processing, OCR, GUI development, and database management. It requires robust architecture planning to ensure scalability, maintainability, and extensibility. Good documentation and code organization are key for a successful project.

Overall, this application is designed to efficiently manage business card information, serving the needs of both businesses and individuals.

## Further Improvements

Using ML and NLP a generalized model can be created.




