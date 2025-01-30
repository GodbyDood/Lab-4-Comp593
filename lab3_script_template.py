""
from sys import argv 
import os

""
def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)

# Get path of sales data CSV file from the command line
def get_sales_csv():
    # Check whether command line parameter provided
    if len(argv)<2:
           print("Please Provide Required Parameters")
           exit(1)
    # Check whether provide parameter is valid path of file
    sales_csvfile=argv[1]
    if not os.path.isfile(sales_csvfile):
        print("invalid filename")
        exit(1)
    return sales_csvfile

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    # Get directory in which sales data CSV file resides

    # Determine the name and path of the directory to hold the order data files
    # Create the order directory if it does not already exist
    csv_path= os.path.abspath(sales_csv)
    csv_dir = os.path.dirname(csv_path)


    return 

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csv, orders_dir):
    # Import the sales data from the CSV file into a DataFrame
    # Insert a new "TOTAL PRICE" column into the DataFrame
    # Remove columns from the DataFrame that are not needed
    # Group the rows in the DataFrame by order ID
    # For each order ID:
        # Remove the "ORDER ID" column
        # Sort the items by item number
        # Append a "GRAND TOTAL" row
        # Determine the file name and full path of the Excel sheet
        # Export the data to an Excel sheet
        # Format the Excel sheet (
        # Define format for the money columns
        # Format each colunm
        # close the sheet
    return
if __name__ == '__main__':
    main()