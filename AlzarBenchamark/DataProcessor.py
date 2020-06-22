import pandas as pd


class DataProcessor:

    def __init__(self):
        pass

    @staticmethod
    def __prepare_data(results_data: pd.DataFrame) -> pd.DataFrame:
        results_data.columns = ["Code_version", "Test_data", "Captured_time[s]", "Records per buffer",
                                "Buffers per acquisition", "Post trigger samples", "decimation"]
        results_data.sort_values(by=["Code_version"], inplace=True)
        return results_data

    @staticmethod
    def __evaluate_efficiency(results_data: pd.DataFrame, time_of_experiment: int):
        results_data["Time of experiment"] = time_of_experiment
        results_data["Total time"] = results_data["Post trigger samples"] * results_data["decimation"]
        results_data["Efficiency"] = results_data["Time of experiment"] / \
                                     (results_data["Buffers per acquisition"]
                                      * results_data["Records per buffer"]
                                      * results_data["Total time"])
        return results_data

    # TODO: Today (Monday)
    def pass_data_to_plot(self):
        return

