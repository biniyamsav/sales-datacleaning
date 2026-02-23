import pandas as pd
from word2number import w2n
import math
import mysql.connector

# Load the CSV
data = pd.read_csv(
    "your_file_path_here.csv",
     usecols=["Product", "Category", "Quantity", "Unit_Price"]
                   )  # use your file path
# Convert to list of lists
data_list = data.values.tolist()
def names2small(data_list):
    for item in data_list:
         item[0]=item[0].lower()
         item[1]=item[1].lower()
         if isinstance(item[2],str):
             item[2]=item[2].lower()
         if isinstance(item[3],str):
              item[3]=item[3].lower()
    return data_list
def clean_space(data_list):
    for item in data_list:
         item[0]=item[0].strip()
         item[1]=item[1].strip()
         if isinstance(item[2],str):
             item[2]=item[2].strip()
         if isinstance(item[3],str):
             item[3]=item[3].strip()
    return data_list
def none_removal(data_list):
    data_list = [
    row for row in data_list
    if not (
        row[2] is None or (isinstance(row[2], float) and math.isnan(row[2])) or
        row[3] is None or (isinstance(row[3], float) and math.isnan(row[3])) or
        row[1] is None
    )
]
    return data_list
def unreal_number_remove(data_list):
     new_list=[]
     for item in data_list:
         try:
            if item[2] >= 10000:
                item[2] = None
            if item[2] <= 0:
                item[2] = None
            if item[3] <= 0:
                item[3] = None
            if item[3] > 10000000:
                item[3] = None
         except:
             continue
         new_list.append(item)

     return new_list
def word2number(data_list):
    for item in data_list:
        if isinstance(item[2],str) :
            try:
                if any(ch.isdigit() for ch in item[2]):
                    for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,":
                        if ch=="o" or ch=="O":
                           item[2] = item[2].replace(ch, "0") 
                        else:
                            item[2] = item[2].replace(ch, "")
                    item[2]=int(item[2])
                elif not any(ch.isdigit() for ch in item[2]):
                     item[2] = w2n.word_to_num(item[2])
                    
            except:
                item[2]=None
        if isinstance(item[3],str) :
            try:
                if any(ch.isdigit() for ch in item[3]):
                    for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,":
                        if ch=="o" or ch=="O":
                            item[3] = item[3].replace(ch, "0") 
                        else:                           
                            item[3] = item[3].replace(ch, "")
                    item[3]=int(item[3])
                elif not any(ch.isdigit() for ch in item[3]) :
                 item[3] = w2n.word_to_num(item[3])
                
            except:
                 item[3]=None
    return data_list
def save_to_sql(new_data):
    conn = mysql.connector.connect(
        # Update your MySQL credentials
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_database_name"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cleaned_sales_data (
        Product VARCHAR(100),
        Category VARCHAR(100),
        Quantity FLOAT,
        Unit_Price FLOAT
    )
    """)
    
    cursor.execute("TRUNCATE TABLE cleaned_sales_data")
    
    for item in new_data:
        cursor.execute(
            "INSERT INTO cleaned_sales_data (Product, Category, Quantity, Unit_Price) VALUES (%s, %s, %s, %s)",
            item
        )
    
    conn.commit()
    conn.close()
def main():
    # Step 1: lowercase and strip strings
     data_list_clean = names2small(data_list)
     data_list_clean = clean_space(data_list_clean)

    # Step 2: convert words and messy strings to numbers
     data_list_clean = word2number(data_list_clean)

    # Step 3: remove impossible numbers
     data_list_clean = unreal_number_remove(data_list_clean)

    # Step 4: remove rows with None, NaN, or missing important data
     new_data = none_removal(data_list_clean)
     save_to_sql(new_data)
main()
