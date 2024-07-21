import sqlite3
import csv

# Step 1: Connect to or Create a SQLite Database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Step 2: Create a Table
# Adjust data types according to your specific needs
create_table_query = '''
CREATE TABLE IF NOT EXISTS sales (
    InvoiceID TEXT PRIMARY KEY,
    Branch TEXT,
    City TEXT,
    CustomerType TEXT,
    Gender TEXT,
    ProductLine TEXT,
    UnitPrice REAL,
    Quantity INTEGER,
    Tax5Percent REAL,
    Total REAL,
    Date TEXT,
    Time TEXT,
    Payment TEXT,
    cogs REAL,
    GrossMarginPercentage REAL,
    GrossIncome REAL,
    Rating REAL
)
'''
cursor.execute(create_table_query)

# Step 3: Import CSV Data Into the Table
with open('supermarket_sales.csv', 'r') as csv_file:
    # Note: Adjust the CSV file name/path as necessary
    csv_reader = csv.DictReader(csv_file)  # Using DictReader for convenience
    
    for row in csv_reader:
        insert_query = '''
        INSERT INTO sales (InvoiceID, Branch, City, CustomerType, Gender, ProductLine, UnitPrice, Quantity, Tax5Percent, Total, Date, Time, Payment, cogs, GrossMarginPercentage, GrossIncome, Rating) 
        VALUES (:InvoiceID, :Branch, :City, :CustomerType, :Gender, :ProductLine, :UnitPrice, :Quantity, :Tax5Percent, :Total, :Date, :Time, :Payment, :cogs, :GrossMarginPercentage, :GrossIncome, :Rating)
        '''
        cursor.execute(insert_query, row)
    
    conn.commit()

# Don't forget to close the connection when done
conn.close()

