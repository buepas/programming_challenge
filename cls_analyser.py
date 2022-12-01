import os

import matplotlib.pyplot as plt
import pandas as pd

from cls_vehicle_data import VehicleData


class Analyser:
    def __init__(self, vehicle_data: VehicleData, figure_path: str):
        if not vehicle_data.is_final_table_created():
            raise Exception("Final Table is not yet created!")
        self.__final_table = vehicle_data.get_final_table()
        self.__vehicle_data = vehicle_data
        self.__figure_path = figure_path
        if not os.path.exists(self.__figure_path):
            os.mkdir(self.__figure_path)

    def evaluate(self):
        self.__evaluate_top_3_countries_by_sales_in(("2014-01-01", "2020-12-31"))
        self.__evaluate_top_year_sales(("2014-01-01", "2020-12-31"))
        self.__evalute_first_sold_vehicle()
        self.__evaulate_vehicles_sold_in_with_motors(("2017-01-01", "2021-01-01"), ["OM934", "OM936", "OM470", "OM471"])

    def __evaluate_top_3_countries_by_sales_in(self, date_constraint: (str, str)):
        local_df = self.__filter_for_year(date_constraint)
        local_df = local_df.groupby(["country"])["country"].count().sort_values(ascending=False)
        local_df = local_df.head(3).reset_index(name="amount")
        local_df.set_index(["country"]).plot(kind="bar", stacked=False, color=["#ffed00", "#a9ff9e", "orange"],
                                             y="amount", legend=None)
        plt.xlabel("country")
        plt.ylabel("sold units")
        plt.title("Top three countries by sales between 2014-01-01 - 2020-12-31")
        plt.tight_layout()
        plt.savefig(os.path.join(self.__figure_path, "top_3_countries.png"))

    def __evaluate_top_year_sales(self, date_constraint: (str, str)):
        local_df: pd.DataFrame = self.__filter_for_year(date_constraint)
        local_df: pd.Series = local_df["production_date"]
        local_df = pd.DatetimeIndex(local_df).year.value_counts().reset_index(name="sales")
        local_df = local_df.head(1)
        found_year = local_df.get("index")[0]
        found_sales = local_df.get("sales")[0]
        print(f"In {found_year} wurden am meisten Fahrzeuge verkauft: {found_sales}")

    def __evalute_first_sold_vehicle(self):
        local_df: pd.DataFrame = self.__final_table.copy()
        first_fin_sold = local_df.nsmallest(1, "production_date")['fin'].values[0]
        first_fin_sold_date = local_df[local_df["fin"] == first_fin_sold]['production_date'].values[0]
        print(f"fin {first_fin_sold} sold in {first_fin_sold_date}")

    def __evaulate_vehicles_sold_in_with_motors(self, date_constraint: (str, str), motors: [str]):
        local_df = self.__filter_for_year(date_constraint)
        local_df["sales_code_array"] = local_df["sales_code_array"].str.split(", ")

        engines_df: pd.DataFrame = self.__vehicle_data.get_sheets()["engines"]
        engines_df["Code Descrition En"] = engines_df['Code Description En'].str.replace(" ", "")
        engines_df = engines_df[engines_df["Code Descrition En"].str.contains("|".join(motors))]

        engine_to_sales_codes = list(zip(engines_df["Code Descrition En"], engines_df["Sales Code"]))
        filtered_engines = {}
        for (engine, sales_code) in engine_to_sales_codes:
            mask = [(sales_code in x) for x in local_df["sales_code_array"]]
            test_value: int = local_df[mask]['fin'].count()
            filtered_engines[engine] = test_value

        plt.bar(*zip(*filtered_engines.items()), color=["red","green","blue","orange"])
        plt.title("Verkaufte Fahrzeuge zwischen 01.01.2017 und 01.01.2021")
        plt.xlabel("Motor-Typ")
        plt.ylabel("Anzahl Fahrzeuge")
        plt.tight_layout()
        plt.savefig(os.path.join(self.__figure_path, "motoren_nach_datum.png"))

    def __filter_for_year(self, date_constraint: (str, str)) -> pd.DataFrame:
        local_df: pd.DataFrame = self.__final_table.copy()
        return local_df[
            (local_df["production_date"] >= date_constraint[0]) & (local_df["production_date"] <= date_constraint[1])]
