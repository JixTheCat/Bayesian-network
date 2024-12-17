from cpt import *
import json
from openpyxl import Workbook

file = 'riverland_env.json'

# Load the JSON file
with open(file) as f:
    d = json.load(f)

# Create a new Excel workbook and sheet
wb = Workbook()
ws = wb.active
ws.title = "CPT Results"

# Header row
ws.append(["ID", "Keys", "CPT Result"])  # Adjust headers as needed

# Append data to Excel
for weight in d['weights']:
    row = [weight['id']]  # Start row with ID
    
    if isinstance(weight['scores'], dict):
        scores_values = list(weight['scores'].values())
        
        if sum(scores_values) == 0:  # Skip if weights sum to zero
            row.append("Skipped: sum of weights is zero")
            row.append("")  # Empty CPT result column
        else:
            keys = ','.join(weight['scores'].keys())
            cpt_result = calculate_CPT(scores_values, weight['notideal'], weight['ideal'])
            row.append(keys)  # Add keys
            row.extend(cpt_result)  # Append CPT result list
    else:
        row.append("ideal: {}, notideal: {}".format(weight['ideal'], weight['notideal']))
        row.append("")  # Empty CPT result column

    ws.append(row)  # Write the row to the spreadsheet

# Save the workbook to a file
wb.save("output.xlsx")
print("Results saved to output.xlsx")
