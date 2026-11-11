import pandas as pd
import requests
import sqlite3
import logging
import os
import sys

base_dir = os.path.dirname(__file__)
result_dir = os.path.join(base_dir,'..','results')
os.makedirs(result_dir, exist_ok=True)


log_dir=os.path.join(base_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir,'etl.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def data_extraction(url):
    try:

        logging.info("starting data extraction")
        response = requests.get(url)
        response.raise_for_status()
        data=response.json()
        logging.info("Data extrated succesfully")
        return data

    except requests.exceptions.RequestException as e:

        logging.error(f"Data extract error: {e}")
        print("It didn't work out obtain data")
        return None
    

def data_transform (data):
    try:
        logging.info('Starting data transform...')
        df= pd.DataFrame(data['products'])
        assert not df.empty,"The data frame its empty, stopping process..."

        df.to_csv(os.path.join(result_dir, 'products.csv'), index=False)

        for col in df.columns :
            if isinstance(df[col].iloc[0], list):
                print(f"columna con lista: {col}")

        main_columns = [
            'id', 
            'title', 
            'description', 
            'price', 
            'discountPercentage', 
            'rating', 
            'stock', 
            'brand', 
            'category'
            ]
        
        df_main = df[main_columns]
        assert 'id' in df_main.columns, "Process stopped: Column 'id' doesn't exist."
        assert 'price' in df_main.columns, "Process stopped: Column 'price' doesn't exist."
        assert 'title' in df_main.columns, "Process stopped: Column 'title' doesn't exist"

        logging.info(f"Main dataFrame created with {len(df_main)} records.")

        df_images = df[['id','images']].copy()
        df_images = df_images.explode('images')
            # Renombrar columnas para que sean claras
        df_images.columns = ['product_id', 'image_url']
        if df_images.empty:
            logging.warning("df_images does not have any records.")
            df_images = pd.DataFrame(columns=['product_id', 'image_url'])
        else:
            logging.info(f"Images dataFrame created with {len(df_images)} records.")

        df_tags = df[['id', 'tags']].copy()
        df_tags = df_tags.explode('tags')
        df_tags.columns = ['product_id', 'tag']
        if df_tags.empty:
            logging.warning("df_tags does not have any records.")
        else:
            logging.info(f"Tags dataFrame created with {len(df_tags)} records.")
        return df_main, df_images, df_tags

    
    except KeyError as e:

        logging.error(f"Unexpected transform data error {e}")
        print("Transform error, check log file")
        exit()

    except Exception as e:
        logging.error(f"Unexpected transform data error {e}")
        print("Transform error, check log file")
        exit()


def data_load(df_main, df_images, df_tags, db_name):
    try:
        logging.info("Starting data load...")

        conn = sqlite3.connect(os.path.join(result_dir, db_name))
        print(df_images.columns)
        
        df_main.to_sql('products', conn, if_exists='replace', index=False)
        df_images.to_sql('products_images', conn, if_exists='replace', index=False)
        df_tags.to_sql('products_tags', conn, if_exists='replace', index=False)
        logging.info("Data loaded succesfuly at SQLite")
        return conn

    except sqlite3.Error as e:
        logging.info(f"Unexpected data load error {e}")
        print(f"Unexpected data load error, check log file")
        exit()

def sql_verification(conn):
    exito= False
    try:
        print(" "*15,">>> VERIFICACION SQL <<<")
        print("="*60)

        logging.info("Starting SQL verification...")
        cursor = conn.cursor()
        

        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"total de productos guardados: {count}")
        
            print("\n Muestra de productos (id, title, price):")
            cursor.execute("SELECT id, title, price FROM products LIMIT 5")
            for row in cursor.fetchall():
                print(f"ID: {row[0]}, Titulo: {row[1]}, Precio: {row[2]}")
        else: 
            logging.info("there weren't products saved")
            return exito


        print("\n Imagenes del producto con ID 1: ")
        cursor.execute("SELECT image_url FROM products_images WHERE product_id = 1")
        image = cursor.fetchall()
        if image:
            for img in image:
                    print(f"- {img[0]}")
        else:
            print(" No se encontraron imagenes para el producto 1.")
            
        print("\n", "="*60)
        exito = True
        
            

    except sqlite3.Error as e:
        logging.error(f"SQL verification error: {e}")
        print("Data verification error, check log file")
        exito = False

    finally:
        if conn:
            conn.close()
            print("Closed connection")
        if exito:    
            logging.info(f"Data verification was succesful, closed connection")
    return exito

def main():

    logging.info(" ")
    logging.info("="*70)
    logging.info("                        New process starting...")
    logging.info("="*70)
    
    url = 'https://dummyjson.com/products'
    db_name = 'ecommerce.db'

    data= data_extraction(url)
    if data is None:
        return False

    df_main, df_images, df_tags = data_transform(data)
    if df_main is None:
        return False

    conn = data_load(df_main,df_images,df_tags,db_name)
    if conn is None:
        return False

    return sql_verification(conn)

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)


