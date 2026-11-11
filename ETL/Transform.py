import pandas as pd
import sqlite3
import logging 
import os
import sys

base_dir = os.path.dirname(__file__)
result_dir = os.path.join(base_dir, '..', 'results')
os.makedirs(result_dir, exist_ok=True)

log_dir_tf = os.path.join(os.path.dirname(__file__), "logs_tf")
os.makedirs(log_dir_tf, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir_tf, 'etl.log_tf'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s, - %(message)s'
)

def db_connect (db_name):
    
    try:
        logging.info("Connecting to data base")
        conn = sqlite3.connect(os.path.join(result_dir, db_name))
        if conn:
            logging.info("Data loaded succesfully")
            df = pd.read_sql_query('SELECT * FROM products', conn)
            print('         DATA LOADED')
        conn.close()
        return df
    
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        

    
def data_transform (df):
    try:
        logging.info("Starting data transform...")

        df = df.drop_duplicates(subset = ['id'])
        df = df.fillna({'brand': 'Unknown brand'})
        df['price'] = df['price'].astype(float)
        df = df.rename(columns={'title':'Product_Name'})
        df['discountAmount'] = round(df['price'] * df['discountPercentage'] / 100, 2)
        df['final_price'] = round(df['price'] - df['discountAmount'], 2)
        df['rating_category'] = pd.cut(
            df['rating'], 
            bins=[0,2,4,5], 
            labels=['Low','Medium','High'], 
            include_lowest=True,
        )

        final_columns=[

            'id',
            'Product_Name',
            'brand',
            'category',
            'price',
            'discountPercentage',
            'discountAmount',
            'final_price',
            'rating',
            'rating_category',
            'stock'

        ]

        df_clean=df[final_columns]
        assert 'id' in df_clean.columns, "Process stopped: Column 'id' does not exist"
        assert 'price' in df_clean.columns, "Process stopped: Column 'price' does not exist"

        df_clean.to_csv(os.path.join(result_dir, 'products_clean.csv'), index=False)
        logging.info("Data transform was succesful.")

        return df_clean
    
    except KeyError as e:
        logging.error(f"Unexpected data transform error {e}")
        print("Unexpected data transform error, check logs_tf file")

        return None
    
    except Exception as e:
        logging.error(f"Unexpected data transform error {e}")
        print("Unexpected data transform error, check logs_tf file")

        return None

def data_load(df_clean,db_name):
    conn = None
    try:
        logging.info("Starting data load...")
        conn = sqlite3.connect(os.path.join(result_dir, db_name))
        df_clean.to_sql('products_clean',
                         conn, 
                         if_exists='replace'
                         , index=False)
        
        logging.info("Data loaded to SQLite was succesful.")
        return True
    
    except sqlite3.Error as e:
        logging.error(f"Unexpected data loaded error {e}")
        print("data loaded error, check logs_tf file")

        return False

    finally:
        if conn is not None:
            conn.close()
            logging.info("Closed connection.")
            print("Clossed connection.")

def main():
    logging.info(" ")
    logging.info("="*70)
    logging.info("                        New process starting...")
    logging.info("="*70)

    db_name = 'ecommerce.db'

    df = db_connect(db_name)
    if df is None:
        return False

    df_clean = data_transform(df)
    if df_clean is None:
        return False

    return data_load(df_clean, db_name)


if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)

    

