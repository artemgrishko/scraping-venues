import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment, Font
from copy import copy


def merge_json_to_excel(file1, output_excel):
    if not os.path.exists(file1):
        raise FileNotFoundError(f"File {file1} does not exist")


    df1 = pd.read_json(file1)

    combined_df = pd.concat([df1], ignore_index=True)

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column].width = adjusted_width
            for cell in col:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

        for row in worksheet.iter_rows():
            for cell in row:
                font = copy(cell.font)
                font.size = 11
                cell.font = font

        for cell in worksheet[1]:
            font = copy(cell.font)
            font.bold = True
            font.size = 12
            cell.font = font


