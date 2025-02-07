from sys import argv, exit
import os
import pandas as pd  # Changed to 'pd' for consistency and readability
import re
import xlsxwriter  # Keeping xlsxwriter for possible formatting
import openpyxl
from datetime import date

def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)

# Get path of sales data CSV file from the command line
def get_sales_csv():
    # Check whether command line parameter provided
    if len(argv) < 2:
        print("Please Provide Required Parameters")
        exit(1)
    # Check whether provided parameter is a valid file path
    sales_csvfile = argv[1]
    if not os.path.isfile(sales_csvfile):
        print("Invalid filename")
        exit(1)
    return sales_csvfile

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    # Get directory in which sales data CSV file resides
    csv_path = os.path.abspath(sales_csv)
    csv_dir = os.path.dirname(csv_path)
    # Determine the name and path of the directory to hold the order data files
    todaysdate = date.today().isoformat()
    order_dir = os.path.join(csv_dir, f'Orders_{todaysdate}')

    # Create the order directory if it does not already exist
    if not os.path.isdir(order_dir):
        os.makedirs(order_dir)

    return order_dir

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csvfile, orders_dir):
    # Import the sales data from the CSV file into a DataFrame
    sales_df = pd.read_csv(sales_csvfile)  # Changed to use sales_csvfile parameter
    # Insert a new "TOTAL PRICE" column into the DataFrame
    sales_df.insert(7, "TOTAL PRICE", sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])
    # Remove columns from the DataFrame that are not needed
    sales_df.drop(columns=['ADDRESS', 'CITY'], inplace=True)
    # Group the rows in the DataFrame by order ID
    grouped_orders = sales_df.groupby('ORDER ID')  # Assigned the group to a variable

    # For each order ID:
    for order, order_dataframe in grouped_orders:
        # Remove the "ORDER ID" column
        order_dataframe.drop(columns=['ORDER ID'], axis=1, inplace=True)
        # Sort the items by item number
        order_dataframe.sort_values(by='ITEM NUMBER', inplace=True)
        # Append a "GRAND TOTAL" row
        order_dataframe['ITEM_PRICE'] = order_dataframe['ITEM QUANTITY'] * order_dataframe['ITEM PRICE']
        grand_total = order_dataframe[['ITEM QUANTITY', 'ITEM_PRICE']].sum()
        grand_total['ITEM NUMBER'] = 'GRAND TOTAL'
        
        # Convert grand_total into a DataFrame and concatenate it with order_dataframe
        grand_total_df = pd.DataFrame([grand_total])
        order_dataframe = pd.concat([order_dataframe, grand_total_df], ignore_index=True)  # Using concat instead of append idk why concat is depricated
        # Determine the file name and full path of the Excel sheet
        order_filename = f'Order_{order}.xlsx'
        order_filepath = os.path.join(orders_dir, order_filename)

        # Export the data to an Excel sheet
        with pd.ExcelWriter(order_filepath, engine='xlsxwriter') as writer:
            order_dataframe.to_excel(writer, index=False, sheet_name='Order')

            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Order']

            # Define format for the money columns
            money_format = workbook.add_format({'num_format': '$#,##0.00'})

            # Apply the money format to the appropriate column (assuming 'TOTAL PRICE' is in column F)
            worksheet.set_column('F:F', None, money_format)

            # Automatically adjust column width based on the maximum length of the data in each column
            for i, column in enumerate(order_dataframe.columns):
                # Calculate the max width of the column's data
                column_width = max(order_dataframe[column].astype(str).map(len).max(), len(column)) + 2
                worksheet.set_column(i, i, column_width)

        # Close the Excel writer after processing each order

    return

if __name__ == '__main__':
    main()
