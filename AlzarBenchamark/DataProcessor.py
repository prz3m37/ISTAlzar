import pandas as pd


class DataProcessor:

    def __init__(self):
        pass

    @staticmethod
    def __prepare_data(results_data: pd.DataFrame) -> pd.DataFrame:
        results_data.columns = ["Code_version", "Test_data", "Captured_time[s]",
                                "Trigger_dela[s]", "Points_number"]
        results_data.sort_values(by=["Code_version"], inplace=True)
        return results_data

    # TODO: Determine the efficiency
    @staticmethod
    def __evaluate_efficiency(results_data: pd.DataFrame):
        return

    def pass_data_to_plot(self):
        return

import numpy as np
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])
c = np.ravel([a, b], 'F')
print(c)