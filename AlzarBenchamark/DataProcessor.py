import pandas as pd
import numpy as np
from Utils import Utils


class DataProcessor:

    def __init__(self):
        self.__utils = Utils()

    def prepare_data(self, results_data: str) -> pd.DataFrame:
        read_results_df = self.__utils.read_results(results_data)
        read_results_df.columns = ["Code_version", "Test_data", "Captured_time[ns]", "Records_per_buffer",
                                   "Buffers_per_acquisition", "Post_trigger_samples", "decimation"]
        read_results_df.sort_values(by=["Code_version"], inplace=True)
        return read_results_df

    @staticmethod
    def evaluate_efficiency(results_data: pd.DataFrame, time_of_experiment: int):
        results_data["Time_of_experiment[ns]"] = time_of_experiment
        results_data["Total_time[ns]"] = results_data["Post_trigger_samples"] * results_data["decimation"]
        results_data["percentage[%]"] = results_data["Total_time[ns]"] / results_data["Time_of_experiment[ns]"]
        results_data["Efficiency"] =( results_data["Time_of_experiment[ns]"] / \
                                     (results_data["Buffers_per_acquisition"]
                                      * results_data["Records_per_buffer"]
                                      * results_data["Total_time[ns]"])) * 100
        return results_data

    # TODO: Add possibility of different decimations and buffers :D
    @staticmethod
    def pass_data_to_plot(results_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
        python_code = results_data.loc[results_data["Code_version"] == "[PyhCode]"]
        cpp_code = results_data.loc[results_data["Code_version"] == "[CppCode]"]
        decimation = results_data["decimation"].iloc[0]
        return python_code, cpp_code, decimation
