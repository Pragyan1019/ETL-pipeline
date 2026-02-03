from ingest import ingest_data
from validate import validate_all
from clean import clean_all
from load_to_mysql import load_file

def pipeline():
    try:
        print("Starting data pipeline...")
        print("Ingesting data...")
        ingest_data();
        print("Validating data...")
        validate_all();
        print("Cleaning data...")
        clean_all();
        print("Loading data into MySQL...")
        load_file();
        print("Data pipeline completed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise


if __name__  == "__main__":
    pipeline();