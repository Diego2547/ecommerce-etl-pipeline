import schedule
import time 
import subprocess
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__),'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'automation.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

etl_path=os.path.join(os.path.dirname(__file__), '..','ETL','ETL.py')
transform_path=os.path.join(os.path.dirname(__file__), '..','ETL','Transform.py')

def run_script(path, name):
    try:
        logging.info(f"starting {name} execution...")
        result=subprocess.run(
            ['python', path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            logging.info(f"{name} execution successful")
            return True
        else:
            logging.error(f"Error on {name}:{result.stderr}")
            return False
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

def run_pipeline():
    if run_script(etl_path, "ETL"):
        logging.info("Executing Transform script")
        if run_script(transform_path, "Transform"):
            logging.info("Transform executed succesfully.")
        else:
            logging.error("Transform failed. Pipeline stopped.")
    else:
        logging.error("ETL  failed. Pipeline stopped.")

schedule.every().day.at("09:00").do(run_pipeline)

logging.info("Automation started. Waiting for next execution...")
print("Automation started. Waiting for next execution...")

while True:
    schedule.run_pending()
    time.sleep(1)