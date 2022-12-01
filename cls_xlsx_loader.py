import pandas as pd


class XLSXLoader:
    def __init__(self, path_in: str):
        self.__xlsx_path = path_in
        self.__sheets: {str, pd.DataFrame} = None

    def load_sheets(self) -> None:
        self.__sheets = pd.read_excel(self.__xlsx_path, sheet_name=None)
        if self.sheets_loaded():
            print(f"{len(self.__sheets)} sheets were loaded.")

    def sheets_loaded(self):
        return self.__sheets is not None

    def debug_stuff(self):
        for (sheet_name, sheet_df) in self.__sheets.items():  # type: str, pd.DataFrame
            print(f"Sheet Name: {sheet_name}")
            print(sheet_df.columns)

    def get_sheets(self) -> {str, pd.DataFrame}:
        return self.__sheets
