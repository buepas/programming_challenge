import pandas as pd

from cls_analyser import Analyser
from cls_vehicle_data import VehicleData
from cls_xlsx_loader import XLSXLoader

print("### LOAD sheet-data")
xlsx_loader = XLSXLoader("vehicle_data.xlsx")
xlsx_loader.load_sheets()
vehicle_data = VehicleData(xlsx_loader)
print("### BEGIN data clean-up")
# vehicle_data.print_sheet_metadata()
vehicle_data.sanitize_data()
print("### MERGE data into one table")
vehicle_data.create_final_table()
print("### EVALUTE data")
analyser = Analyser(vehicle_data, figure_path="figures")
analyser.evaluate()

# vehicle_data.print_sheet_metadata()
