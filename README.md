# Enhancing Legal Case Management with Customized CRM and OCR Solution

## Project Overview

This project focuses on the development of a tailored Customer Relationship Management (CRM) solution for Direct Counsel Australia. By integrating Optical Character Recognition (OCR) technology, the CRM automates data entry, streamlining case management processes. The system is designed to manage extensive case data, featuring custom tables and advanced search functions, leading to a significant reduction in data management time and improved data accuracy.

### **Key Features**
- **OCR Integration**: Automates data entry by extracting relevant information from documents, reducing manual input.
- **Customized CRM System**: Manages complex legal case data using custom tables for efficient tracking and retrieval.
- **Advanced Search Functions**: Implements advanced search capabilities to quickly filter and retrieve relevant case information.
- **Efficiency Gains**: Achieves a 50% reduction in data management time, improving overall productivity and client satisfaction.
- **Web Development**: Developed a user-friendly interface to manage legal case data with real-time updates and seamless navigation.
- **DevOps**: Implemented continuous integration and deployment (CI/CD) pipelines for automated testing and deployment, ensuring smooth updates and system stability.
- **Machine Learning**: Incorporated machine learning algorithms to enhance decision-making processes, improving case management efficiency and predictive capabilities.

## Technologies Used
- **HTML**: For structuring the web pages.
- **CSS**: For styling and enhancing the user interface.
- **JavaScript**: For dynamic functionalities and interactivity.
- **SQLite**: For lightweight database management and storage of case data.
- **Python**: Used for backend development and OCR functionality, ensuring smooth data processing and automation.
- **DevOps**: Implemented for continuous integration and deployment (CI/CD), ensuring streamlined updates and maintenance of the system.
- **API Integration**: For seamless connections between the CRM system and external services like counselor referral systems.

## Setup Instructions

To get the CRM system running locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VeritasAnalytica/LegalCaseManagementCRM.git
   ```
2. **Navigate to the project folder**:
   ```bash
   cd project-folder
   ```
4. **Create a virtual environment (if not already created)**:
   ```bash
   python3 -m venv venv
   ```
   After creation, activate the virtual environment:
  
     - On Windows:
        ```bash
        venv\Scripts\activate
        ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
6. **Install dependencies**:
```bash
Flask==2.2.3
Flask-Caching==2.0.3
Flask-SQLAlchemy==3.0.2
pdfkit==0.6.1
pytesseract==0.3.9
pytz==2022.7
pandas==1.5.3
playwright==1.21.2
beautifulsoup4==4.11.1
pdfplumber==0.7.6
python-dotenv==0.21.1
```
7. **Run the Application**:
  ```bash
  python app.py
  ```
8. **Configure Database**:
   
   Make sure the SQLite database is set up properly.

## Features and Benefits

- **OCR Technology**: Simplifies the process of extracting and entering data from legal documents.
- **Improved Data Accuracy**: Ensures that case data is accurate and up-to-date, reducing the chances of human error.
- **Enhanced Client Engagement**: With automated workflows and real-time updates, the CRM enhances client satisfaction by providing faster response times and better service.
