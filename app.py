from flask import Flask, Blueprint
from flask import session
import sqlite3
from fileinput import filename 
from flask import *
from database import get_database
import pandas as pd
import secrets


from flask import Flask, render_template,request, redirect, url_for, session, flash, render_template, g
import pdfkit
from flask import make_response

def format_phone_number(std, number):
    number = str(number)
    std = int(std)
    if std == 4:
        # Format for standard 4
        formatted_number = '+61 4' + number[0:2] + ' ' + number[2:5] + ' ' + number[5:]
    else:
        # Format for other standards
        formatted_number = '+61 ' + str(std) + ' ' + number[0:4] + ' ' + number[4:]
    return formatted_number

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # Generate a secure secret key
DATABASE = 'login.db'  # Using your existing database for simplicity
app.jinja_env.globals.update(format_phone_number=format_phone_number)

crm = Blueprint('crm', __name__, url_prefix='/crm')


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_user(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM login WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            flash('You have successfully logged in!')
            return redirect(url_for('index'))  # Redirect to the main CRM page
        else:
            flash('Invalid email or password')
            return render_template('login.html', error='Invalid email or password')  # Pass the error message
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))



from datetime import datetime

def format_date(date_str):
    """Convert date string from database to a more readable format."""
    if date_str:
        # Attempt to parse the date using different expected formats
        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d'):  # Add more formats here if needed
            try:
                date_object = datetime.strptime(date_str, fmt)
                return date_object.strftime('%B %d, %Y')
            except ValueError:
                continue
    return ''


def format_currency(value):
    if value is None or value == '':
        return '$0.00'
    try:
        numeric_value = float(value)
        return f"${numeric_value:,.2f}"
    except ValueError:
        return value  # Log this error as needed
    




@app.template_filter('currency')
def currency_filter(value):
    return format_currency(value)


@app.route('/')
def index():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Connect to the database
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    # Retrieve the list of tables, or any other operation specific to your CRM
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cur = cur.execute(query)
    tables = cur.fetchall()
    table_names = [table['name'] for table in tables]
    
    # Render the index page with the list of tables
    return render_template('index.html', tables=table_names)


@app.route('/caseslist_ATO/<table_name>')
def cases_ato(table_name):
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session['table_name'] = table_name
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Ensuring that only valid table names are processed to prevent SQL injection
    valid_tables = ['MARCH_2024', 'APRIL_2024', 'MAY_2024','FEBRUARY_2024','JANUARY_2024','JUNE_2024','JULY_2024','AUGUST_2024','SEPTEMBER_2024','OCTOBER_2024','NOVEMBER_2024','DECEMBER_2024']  # Update this list with your actual table names
    if table_name not in valid_tables:
        return "Invalid table name", 400

    # Change the query here to sort by "Court Action Amount" in descending order
    query = f"SELECT *, CAST(COALESCE(`Value`, '0') AS INTEGER) AS NumericValue FROM {table_name} WHERE DefaultCreditor IS NOT NULL ORDER BY NumericValue DESC"

    
    cur.execute(query)
    rows = cur.fetchall()
    return render_template('ATODefaults.html', posts=rows,table=table_name)



@app.route('/caseslist_Defaults/<table_name>')
def cases_defaults(table_name):
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session['table_name'] = table_name
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Ensuring that only valid table names are processed to prevent SQL injection
    valid_tables = ['MARCH_2024', 'APRIL_2024', 'MAY_2024','FEBRUARY_2024','JANUARY_2024','JUNE_2024','JULY_2024','AUGUST_2024','SEPTEMBER_2024','OCTOBER_2024','NOVEMBER_2024','DECEMBER_2024']  # Update this list with your actual table names
    if table_name not in valid_tables:
        return "Invalid table name", 400

    # Change the query here to sort by "Court Action Amount" in descending order
    query = f"SELECT *, CAST(COALESCE(`Value`, '0') AS INTEGER) AS NumericValue FROM {table_name} WHERE DefaultCreditor IS NULL ORDER BY NumericValue DESC"

    
    cur.execute(query)
    rows = cur.fetchall()
    return render_template('CourtActions.html', posts=rows,table=table_name)







@app.route('/caseslist/<table_name>')
def cases(table_name):
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    con = sqlite3.connect("books.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Ensuring that only valid table names are processed to prevent SQL injection
    valid_tables = ['MARCH_2024', 'APRIL_2024', 'MAY_2024','FEBRUARY_2024','JANUARY_2024','JUNE_2024','JULY_2024','AUGUST_2024','SEPTEMBER_2024','OCTOBER_2024','NOVEMBER_2024','DECEMBER_2024']  # Update this list with your actual table names
    if table_name not in valid_tables:
        return "Invalid table name", 400

    # Change the query here to sort by "Court Action Amount" in descending order
    query = f"SELECT *, CAST(COALESCE(`Value`, '0') AS INTEGER) AS NumericValue FROM {table_name} ORDER BY NumericValue DESC"
    
    cur.execute(query)
    rows = cur.fetchall()
    return render_template('CaseMonth.html', posts=rows,table=table_name)



@app.route('/widget')
def widget():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('widget.html')
@app.route('/form')
def form():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('form.html')
@app.route('/table')
def table():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('table.html')
@app.route('/chart')
def chart():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Retrieve the table name from the session
    table_name = session.get('table_name')
    if not table_name:
        return "No table name found", 400

    # You can now use `table_name` in your chart logic
    return render_template('chart.html', table_name=table_name)
    
@app.route('/signin')
def signin():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('signin.html')
@app.route('/signup')
def signup():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/404')
def _404():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('404.html')
@app.route('/blank')
def blank():
     # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('blank.html')

@app.route('/success', methods=['POST'])
def success():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Get the file and the selected month from the request
        f = request.files['file']
        selected_month = request.form['month']

        # Validate the selected month to prevent SQL injection
        if selected_month not in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            return "Invalid month selected", 400
        
        # Create the table name based on the selected month and the static year
        table_name = f"{selected_month.upper()}_2024"

        # Determine the file type from the file extension
        file_extension = f.filename.split('.')[-1].lower()
        
        # Read the file into a DataFrame based on the file extension
        if file_extension in ['csv']:
            df = pd.read_csv(f)
        elif file_extension in ['xls', 'xlsx']:
            #df = pd.read_excel(f)
            df = pd.read_excel(f, dtype={'PhoneNo': str})

        else:
            return "Unsupported file type", 400

        print(df)  # Optional: print the DataFrame to the console for debugging
	
        # Get the database connection
        db = get_database()

    # Write the DataFrame to SQL, replacing the table if it exists
        df.to_sql(table_name, con=db, if_exists="replace")

        con = sqlite3.connect("books.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN 'Status' TEXT DEFAULT 'Not Started'")
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN 'Notes' TEXT DEFAULT ' '")
        # Ensure to provide a default value properly for the new column "Additional Phone No"
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN 'Additional Phone No' TEXT DEFAULT ''")

        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN \"Value\" TEXT DEFAULT ''")
        con.commit()
        cur.execute(f"UPDATE {table_name} SET \"Value\" = COALESCE(\"Court Action Amount\", \"DefaultAmount\")")
        con.commit()
        
        
    # Commit the transaction
        db.commit()
        #f.save(f.filename) 
        return render_template("Acknowledgement.html", name = f.filename) 


# in app.py
# @app.route('/CaseDetailsSheet/<int:id>/<table>')
# def details(id, table):
#     conn = sqlite3.connect('books.db')
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()

#     cur.execute(f"SELECT * FROM {table} WHERE `index` = ?", (id,))
#     row = cur.fetchone()

#     return render_template('CaseDetailsSheet.html', row=row, table=table)

@app.route('/CaseDetailsSheet/<int:id>/<table>')
def details(id, table):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {table} WHERE `index` = ?", (id,))
    row = cur.fetchone()
    if not row:
        return "No such record found", 404

    # Convert the immutable Row object to a mutable dictionary
    row = dict(row)
    if 'Action_date' in row:
        row['Action_date'] = format_date(row['Action_date'])
    if 'DefaultDate' in row:
        row['DefaultDate'] = format_date(row['DefaultDate'])


    # Convert to string first if the value is not None
   
    if row['PhoneNo'] is not None:
        num = row['PhoneNo']

    if row['PhoneSTD'] is not None:
        std = row['PhoneSTD']
        # Extracts the first digit from the PhoneSTD field
        first_digit_match = re.search(r'\d', str(row['PhoneSTD']))
        row['PhoneSTD'] = int(first_digit_match.group(0)) if first_digit_match else None
    else:
        std = 0 
    formated_number = format_phone_number(std, num)
    print("hello world")
    print("STD:", std, "Number:", num)
    formatted_number = format_phone_number(std, num)
    print("Formatted Number:", formatted_number)

       # Fetch the next larger value (for the "Next" button)
        # Fetch the previous and next record IDs based on the 'Value'
    prev_record = cur.execute(f"SELECT `index` FROM {table} WHERE CAST(COALESCE(`Value`, '0') AS INTEGER) > (SELECT CAST(COALESCE(`Value`, '0') AS INTEGER) FROM {table} WHERE `index` = ?) ORDER BY CAST(COALESCE(`Value`, '0') AS INTEGER) ASC LIMIT 1", (id,)).fetchone()
    next_record = cur.execute(f"SELECT `index` FROM {table} WHERE CAST(COALESCE(`Value`, '0') AS INTEGER) < (SELECT CAST(COALESCE(`Value`, '0') AS INTEGER) FROM {table} WHERE `index` = ?) ORDER BY CAST(COALESCE(`Value`, '0') AS INTEGER) DESC LIMIT 1", (id,)).fetchone()

    prev_id = prev_record['index'] if prev_record else None
    next_id = next_record['index'] if next_record else None

    return render_template('CaseDetailsSheet.html', row=row, table=table, prev_id=prev_id, next_id=next_id, formated_number=formated_number)
    # return render_template('CaseDetailsSheet.html', row=row, table=table)


from datetime import datetime
import re, json  # Import json for parsing JSON input from Tagify
@app.route('/update_data/<int:id>/<table>', methods=['POST'])
def update_data(id, table):
    # List of valid table names for security checks
    valid_tables = ['MARCH_2024', 'APRIL_2024', 'MAY_2024', 'FEBRUARY_2024', 'JANUARY_2024', 'JUNE_2024', 'JULY_2024', 'SEPTEMBER_2024', 'OCTOBER_2024', 'NOVEMBER_2024', 'DECEMBER_2024']
    if table not in valid_tables:
        return "Invalid table name", 400

    
    # Open a connection to the database
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()

    # # Retrieve and parse the phone numbers from Tagify input for the primary phone number
    # phone_numbers_json = request.form.get('PhoneNumber', '[]')
    # phone_numbers = []
    # try:
    #     phone_numbers = json.loads(phone_numbers_json)
    #     phone_numbers = [phone['value'] for phone in phone_numbers]
    # except (TypeError, ValueError):
    #     pass

    # phone_std, phone_no = '', ''
    # # Process each phone number
    # for phone in phone_numbers:
    #     phone_match = re.match(r'(\+\d+)(\d+)', phone)
    #     if phone_match:
    #         phone_std, phone_no = phone_match.groups()

    # # Remove any decimal points from phone_std and phone_no
    # phone_std = str(phone_std).replace('.0', '')
    # phone_no = str(phone_no).replace('.0', '')

    

    # Other form data
    key_decision_maker_full_name = request.form.get('KeyDecisionMakerFullName', '')
    try:
        key_decision_maker_full_name = json.loads(key_decision_maker_full_name)
        key_decision_maker_full_name = ', '.join([tag['value'] for tag in key_decision_maker_full_name])
    except (TypeError, ValueError):
        pass

    key_decision_maker_position = request.form.get('KeyDecisionMakerPosition', '')
    email = request.form.get('EMAIL', '')
    status = request.form.get('status', '')
    notes = request.form.get('notes', '')
    additionalphoneno = request.form.get('additionalPhoneNo', '')

    # Status dates handling
    status_date1 = request.form.get('statusDate1', '')
    status_date2 = request.form.get('statusDate2', '')
    if "DD/MM/YY" in status:
        dates_to_replace = status.count("DD/MM/YY")
        if dates_to_replace > 0 and status_date1:
            formatted_date1 = datetime.strptime(status_date1, '%Y-%m-%d').strftime('%B %d, %Y')
            status = status.replace("DD/MM/YY", formatted_date1, 1)
        if dates_to_replace > 1 and status_date2:
            formatted_date2 = datetime.strptime(status_date2, '%Y-%m-%d').strftime('%B %d, %Y')
            status = status.replace("DD/MM/YY", formatted_date2, 1)

    # SQL query to update the database
    sql_query = f"""
        UPDATE {table}
        SET 
            `Key Decision Maker Full Name` = ?, 
            `Key Decision Maker Position` = ?,
            `EMAIL` = ?,
            `Status` = ?, 
            `Notes` = ?,
            `Additional Phone No` = ?
        WHERE `index` = ?
    """
    # Execute the SQL query
    cur.execute(sql_query, (key_decision_maker_full_name, key_decision_maker_position,email, status, notes,additionalphoneno,id))
    conn.commit()
    conn.close()

    # Redirect to the details page of the updated record
    return redirect(url_for('details', id=id, table=table))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')



app.register_blueprint(crm)

