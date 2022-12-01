import pandas as pd
from datetime import datetime

from cls_xlsx_loader import XLSXLoader


class VehicleData:
    def __init__(self, xlsx_loader: XLSXLoader):
        if not xlsx_loader.sheets_loaded():
            raise Exception("Sheets not loaded!")
        self.__sheets: {} = xlsx_loader.get_sheets()
        self.__final_table: pd.DataFrame = None

    def __drop_duplicates(self) -> None:
        for (sheet_name, sheet_df) in self.__sheets.items():  # type: str, pd.DataFrame
            sheet_length_before_removal: int = len(sheet_df)
            self.__sheets[sheet_name] = sheet_df.drop_duplicates()
            sheet_length: int = len(self.__sheets[sheet_name])
            print(f"removed {(sheet_length_before_removal - sheet_length)} duplicated entries in {sheet_name}.")

    def __drop_invalid_fin(self, num_of_digits_in_fin=17) -> None:
        sheet_df: pd.DataFrame = self.__sheets["vehicle_hash"]
        sheet_length_before_removal: int = len(sheet_df)
        self.__sheets["vehicle_hash"] = sheet_df[sheet_df["fin"].str.len() >= num_of_digits_in_fin]
        sheet_length: int = len(self.__sheets["vehicle_hash"])
        print(f"removed {(sheet_length_before_removal - sheet_length)} entries with an invalid #fin in vehicle_hash.")

    def __drop_na(self) -> None:
        for (sheet_name, sheet_df) in self.__sheets.items():  # type: str, pd.DataFrame
            sheet_length_before_removal: int = len(sheet_df)
            self.__sheets[sheet_name] = sheet_df.dropna()
            sheet_length: int = len(self.__sheets[sheet_name])
            print(f"removed {(sheet_length_before_removal - sheet_length)} n/a entries in {sheet_name}.")

    def __drop_invalid_dates(self) -> None:
        sheet_df: pd.DataFrame = self.__sheets["sales_codes"]
        sheet_length_before_removal: int = len(sheet_df)
        sheet_df["production_date"] = pd.to_datetime(sheet_df["production_date"], dayfirst=True, errors="coerce")
        sheet_df = sheet_df[sheet_df["production_date"] < datetime.today()]
        sheet_df = sheet_df[sheet_df["production_date"] > "2000-01-01"]
        sheet_length: int = len(sheet_df)
        self.__sheets["sales_codes"] = sheet_df
        print(f"removed {(sheet_length_before_removal - sheet_length)} invalid date entries in sales_codes.")

    def __drop_unwanted_columns(self) -> None:
        for (sheet_name, sheet_df) in self.__sheets.items():  # type: str, pd.DataFrame
            sheet_length_before_removal: int = len(sheet_df)
            if "Unnamed: 0" in sheet_df.columns:
                sheet_df = sheet_df.drop(columns=["Unnamed: 0"])
            if "record_source" in sheet_df.columns:
                sheet_df = sheet_df.drop(columns=["record_source"])
            if "load_ts" in sheet_df.columns:
                sheet_df = sheet_df.drop(columns=["load_ts"])
            self.__sheets[sheet_name] = sheet_df
            print(f"removed unwanted columns in {sheet_name}.")
    def sanitize_data(self):
        self.__drop_duplicates()
        self.__drop_invalid_fin()
        self.__drop_invalid_dates()
        self.__drop_na()
        self.__drop_unwanted_columns()

    def print_sheet_metadata(self) -> None:
        for (sheet_name, sheet_df) in self.__sheets.items():  # type: str, pd.DataFrame
            print(f"Sheet: {sheet_name}")
            print(f"\trows:\t{len(sheet_df)}")
            print(f"\tcols:\t{len(sheet_df.columns)}")

    def create_final_table(self) -> None:
        self.__final_table = pd.merge(self.__sheets["vehicle_hash"], self.__sheets["sales_codes"], how="left",
                                      on="h_vehicle_hash").drop(columns=["h_vehicle_hash"])

    def is_final_table_created(self) -> bool:
        return self.__final_table is not None

    def get_final_table(self) -> pd.DataFrame:
        return self.__final_table

    def get_sheets(self) -> {}:
        return self.__sheets
