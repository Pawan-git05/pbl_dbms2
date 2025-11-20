import pandas as pd
import os
from datetime import datetime

# Define the database directory
DATABASE_DIR = 'database'

# Define CSV schemas
CSV_SCHEMAS = {
    'cases': ['case_id', 'reporter_name', 'reporter_phone', 'location', 'animal_type', 
              'urgency', 'notes', 'media_url', 'status', 'assigned_hospital', 'created_at'],
    'donations': ['donor_name', 'donor_email', 'amount', 'category', 'created_at'],
    'hospitals': ['name', 'address', 'phone', 'location', 'api_lat', 'api_lon', 'created_at'],
    'emergency': ['case_id', 'hospital_id', 'response_time', 'status', 'created_at']
}

def ensure_csv_exists(table_name):
    """Ensure CSV file exists with proper headers"""
    file_path = os.path.join(DATABASE_DIR, f'{table_name}.csv')
    
    if not os.path.exists(file_path):
        # Create directory if it doesn't exist
        os.makedirs(DATABASE_DIR, exist_ok=True)
        
        # Create empty DataFrame with proper schema
        if table_name in CSV_SCHEMAS:
            df = pd.DataFrame(columns=CSV_SCHEMAS[table_name])
            df.to_csv(file_path, index=False)
            print(f"Created {file_path} with schema: {CSV_SCHEMAS[table_name]}")
        else:
            # Create empty CSV if schema not defined
            pd.DataFrame().to_csv(file_path, index=False)
            print(f"Created empty {file_path}")
    
    return file_path

def read_csv(table_name):
    """Read data from CSV file"""
    file_path = ensure_csv_exists(table_name)
    try:
        df = pd.read_csv(file_path)
        return df
    except pd.errors.EmptyDataError:
        # Return empty DataFrame with proper columns if file is empty
        if table_name in CSV_SCHEMAS:
            return pd.DataFrame(columns=CSV_SCHEMAS[table_name])
        else:
            return pd.DataFrame()

def write_csv(table_name, df):
    """Write data to CSV file"""
    file_path = ensure_csv_exists(table_name)
    df.to_csv(file_path, index=False)

def append_row(table_name, row_dict):
    """Append a new row to CSV file"""
    df = read_csv(table_name)
    new_row = pd.DataFrame([row_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    write_csv(table_name, df)
    return df

def generate_case_id():
    """Generate a unique case ID"""
    df = read_csv('cases')
    if df.empty:
        return 'RSQ-00001'
    
    # Get the last case ID and increment
    last_id = df['case_id'].iloc[-1]
    try:
        num = int(last_id.split('-')[1])
        new_num = num + 1
        return f'RSQ-{new_num:05d}'
    except:
        # If parsing fails, generate a new ID
        return f'RSQ-{len(df)+1:05d}'