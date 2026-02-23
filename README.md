# sales-datacleaning
Python project to clean messy sales data and save to MySQL
# Sales Data Cleaning and Import Script

A Python project that automates the cleaning, preprocessing, and storage of sales data from a CSV file into a MySQL database. It ensures data consistency by handling messy inputs such as inconsistent capitalization, extra spaces, numeric values written as words, and unrealistic numbers.

---

## Features

- Normalize product and category names (lowercase, trimmed spaces)
- Convert numeric words (e.g., `"ten"`) to integers
- Clean corrupted numeric strings (e.g., `"1O0O"` → `1000`)
- Remove invalid or unrealistic values:
  - `Quantity <= 0`
  - `Unit_Price <= 0`
  - Extremely large values
  - Missing data
- Save cleaned data into a MySQL table

---

## Requirements

- Python 3.8+
- MySQL server
- Install dependencies:

```bash
pip install pandas word2number mysql-connector-python
```

---

## Usage

1. **Update CSV path** in the script:

```python
data = pd.read_csv("your_file_path_here.csv", usecols=["Product", "Category", "Quantity", "Unit_Price"])
```

2. **Update MySQL credentials** in `save_to_sql()`:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_database_name"
)
```

3. **Run the script**:

```bash
python your_script_name.py
```

4. Cleaned data will be stored in the `cleaned_sales_data` table.

---

## Functions Overview

- `names2small(data_list)` → Converts string fields to lowercase  
- `clean_space(data_list)` → Removes extra spaces  
- `word2number(data_list)` → Converts word numbers and messy numeric strings to integers  
- `unreal_number_remove(data_list)` → Removes unrealistic numeric values  
- `none_removal(data_list)` → Removes rows with missing or invalid data  
- `save_to_sql(new_data)` → Saves the cleaned data to MySQL  

---
## License

This project is licensed under the MIT License.
