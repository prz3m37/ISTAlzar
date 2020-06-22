import pandas as pd
import numpy as np

class DataProcessor:

    def __init__(self):
        pass

    @staticmethod
    def __prepare_data(results_data: pd.DataFrame) -> pd.DataFrame:
        results_data.columns = ["Code_version", "Test_data", "Captured_time[ns]", "Records_per_buffer",
                                "Buffers_per_acquisition", "Post_trigger_samples", "decimation"]
        results_data.sort_values(by=["Code_version"], inplace=True)
        return results_data

    @staticmethod
    def __evaluate_efficiency(results_data: pd.DataFrame, time_of_experiment: int):
        results_data["Time_of_experiment[ns]"] = time_of_experiment
        results_data["Total_time[ns]"] = results_data["Post_trigger_samples"] * results_data["decimation"]
        results_data["percentage[%]"] = results_data["Total_time[ns]"] / results_data["Time_of_experiment[ns]"]
        results_data["Efficiency"] = results_data["Time_of_experiment"] / \
                                     (results_data["Buffers_per_acquisition"]
                                      * results_data["Records_per_buffer"]
                                      * results_data["Total_time"])
        return results_data

    # TODO: Add possibility of different decimations and buffers :D
    @staticmethod
    def pass_data_to_plot(results_data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
        python_code = results_data.loc[results_data["Code_version"] == "[PyhCode]"]
        cpp_code = results_data.loc[results_data["Code_version"] == "[CppCode]"]
        decimation = results_data["decimation"].iloc[0]
        return python_code, cpp_code, decimation
