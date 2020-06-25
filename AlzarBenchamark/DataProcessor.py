import pandas as pd
import numpy as np
from Utils import Utils


class DataProcessor:

    def __init__(self):
        self.__utils = Utils()

    def prepare_data(self, results_data_file: str) -> pd.DataFrame:
        read_results_df = self.__utils.read_results(results_data_file)
        read_results_df.columns = ["Code_version", "Test_data", "Captured_time[ns]", "Records_per_buffer",
                                   "Buffers_per_acquisition", "Post_trigger_samples", "decimation"]

        read_results_df["Captured_time[ns]"] = read_results_df["Captured_time[ns]"] * 10**9
        read_results_df.sort_values(by=["Code_version"], inplace=True)
        return read_results_df

    "[CppCode] 2020-06-24-09:51:01 1.41129 1400 100 2048 1"

    def evaluate_efficiency(self, results_data_file: str, time_of_experiment: int = 10000):
        results_data = self.prepare_data(results_data_file)
        results_data["Time_of_experiment[ns]"] = time_of_experiment
        results_data["Total_time[ns]"] = results_data["Post_trigger_samples"] * results_data["decimation"]
        results_data["percentage[%]"] = (results_data["Total_time[ns]"] / results_data["Time_of_experiment[ns]"]) * 100
        results_data["Efficiency"] = ((results_data["Buffers_per_acquisition"]
                                       * results_data["Records_per_buffer"]
                                       * results_data["Time_of_experiment[ns]"]) / results_data["Captured_time[ns]"])
        return results_data

    # TODO: Add possibility of different decimations and buffers :D

    def pass_data_to_plot(self, results_data_file: str) -> (pd.DataFrame, pd.DataFrame):
        results_data = self.evaluate_efficiency(results_data_file)
        python_code = results_data.loc[results_data["Code_version"] == "[PyhCode]"]
        cpp_code = results_data.loc[results_data["Code_version"] == "[CppCode]"]

        return python_code, cpp_code
