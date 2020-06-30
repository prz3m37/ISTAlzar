import pandas as pd
import numpy as np
from Utils import Utils


class DataProcessor:

    def __init__(self):
        self.__utils = Utils()

    def __del__(self):
        del self.__utils

    def prepare_data(self, results_data_file: str) -> pd.DataFrame:
        read_results_df = self.__utils.read_results(results_data_file)
        read_results_df.columns = ["Code_version", "Test_data", "Captured_time[ns]", "Records_per_buffer",
                                   "Buffers_per_acquisition", "Post_trigger_samples", "decimation"]
        read_results_df["Captured_time[ns]"] = read_results_df["Captured_time[ns]"] * 10 ** 9
        read_results_df.sort_values(by=["Code_version"], inplace=True)
        read_results_df["Total_time[ns]"] = read_results_df["Post_trigger_samples"] * read_results_df["decimation"]
        return read_results_df

    @staticmethod
    def evaluate_efficiency(results_data: pd.DataFrame, time_of_experiment: int = 10000):
        results_data["Time_of_experiment[ns]"] = time_of_experiment
        results_data["percentage[%]"] = (results_data["Total_time[ns]"] / results_data["Time_of_experiment[ns]"]) * 100
        results_data["Efficiency"] = ((results_data["Buffers_per_acquisition"]
                                       * results_data["Records_per_buffer"]
                                       * results_data["Time_of_experiment[ns]"]) / results_data["Captured_time[ns]"])
        return results_data

    @staticmethod
    def __group_code_versions(results_data: pd.DataFrame):
        python_code_data = results_data.loc[results_data["Code_version"] == "[PyhCode]"]
        cpp_code_data = results_data.loc[results_data["Code_version"] == "[CppCode]"]
        return python_code_data, cpp_code_data

    def __extract_data(self, results_data: pd.DataFrame, parameter: str, value_of_parameter: int or float):
        python_code_data, cpp_code_data = self.__group_code_versions(results_data)
        python_code_data_extracted = python_code_data.loc[python_code_data[parameter] == value_of_parameter]
        cpp_code_data_extracted = cpp_code_data.loc[cpp_code_data[parameter] == value_of_parameter]
        cpp_code_efficiency = python_code_data_extracted.groupby([parameter, "percentage[%]"],
                                                                 as_index=False).agg({'Efficiency': ['mean', 'std']})
        python_code_efficiency = cpp_code_data_extracted.groupby([parameter, "percentage[%]"],
                                                                 as_index=False).agg({'Efficiency': ['mean', 'std']})
        return cpp_code_efficiency, python_code_efficiency

    @staticmethod
    def account_sets(results_data: pd.DataFrame):
        account_avg_prams = results_data.groupby(['Records_per_buffer',
                                                  'Buffers_per_acquisition',
                                                  'Post_trigger_samples']).size().reset_index().rename(columns={0: ''})
        return account_avg_prams

    def pass_data_to_plot(self, results_data: pd.DataFrame, parameter: str,
                          value_of_parameter: int or float, code_language: str = None):
        cpp_code_efficiency, python_code_efficiency = self.__extract_data(results_data, parameter, value_of_parameter)
        if code_language == "python":
            x_python = python_code_efficiency["percentage[%]"].values
            y_python = python_code_efficiency["Efficiency"]["mean"].values
            y_python_errors = python_code_efficiency["Efficiency"]["std"].values
            return x_python, y_python, y_python_errors
        if code_language == "cpp":
            x_cpp = cpp_code_efficiency["percentage[%]"].values
            y_cpp = cpp_code_efficiency["Efficiency"]["mean"].values
            y_cpp_errors = cpp_code_efficiency["Efficiency"]["std"].values
            return x_cpp, y_cpp, y_cpp_errors
        else:
            x_python = python_code_efficiency["percentage[%]"].values
            y_python = python_code_efficiency["Efficiency"]["mean"].values
            y_python_errors = python_code_efficiency["Efficiency"]["std"].values
            x_cpp = cpp_code_efficiency["percentage[%]"].values
            y_cpp = cpp_code_efficiency["Efficiency"]["mean"].values
            y_cpp_errors = cpp_code_efficiency["Efficiency"]["std"].values
            return x_python, y_python, x_cpp, y_cpp, y_python_errors, y_cpp_errors

    # TODO: Set it properly
    @staticmethod
    def __calculate_average(channel_A: list, channel_B: list):
        channel_A_buffer_avg, channel_B_buffer_avg = [], []
        for num, buffer_A, buffer_B in enumerate(zip(channel_A, channel_B)):
            channel_A_buffer_avg[num] = np.mean(buffer_A, axis=0)
            channel_B_buffer_avg[num] = np.mean(buffer_B, axis=0)
        channel_A_avg = np.mean(channel_A_buffer_avg, axis=0)
        channel_B_avg = np.mean(channel_B_buffer_avg, axis=0)
        return channel_A_avg, channel_B_avg

    @staticmethod
    def compare_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B):
        if np.array_equal(data_avg_ch_A, ch_A_avg) and np.array_equal(data_avg_ch_B, ch_B_avg):
            return True
        else:
            return False

    def prepare_channel_avg_data(self, data_path: str, data_avg_path: str, buffers_per_acq: int):
        ch_A, ch_B, data_avg_ch_A, data_avg_ch_B = self.__utils.prepare_binary_data(data_path, data_avg_path,
                                                                                    buffers_per_acq)
        ch_A_avg, ch_B_avg = self.__calculate_average(ch_A, ch_B)
        return ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B

    @staticmethod
    def __convert_samples_values(sample_value, input_range_volts):
        bits_per_sample = 8
        code_zero = (1 << (bits_per_sample - 1)) - 0.5
        code_range = (1 << (bits_per_sample - 1)) - 0.5
        sample_volts = input_range_volts * float((sample_value - code_zero) / code_range)
        return sample_volts

    def get_converted_signal(self, channel_A_avg, channel_B_avg):
        converted_signal_A, converted_signal_B = [], []
        for sample_A, sample_B in zip(channel_A_avg, channel_B_avg):
            converted_sample_A = self.__convert_samples_values(sample_A, 0.5)
            converted_sample_B = self.__convert_samples_values(sample_B, 0.5)
            converted_signal_A.append(converted_sample_A)
            converted_signal_B.append(converted_sample_B)
        return converted_signal_A, converted_signal_B

import matplotlib.pyplot as plt
d = {'col1': [1, 1, 1, 1, 2, 2, 2, 2], 'col2': [3,3,3,3,3,4,4,4], 'eff': [1,2,3,4,5,6,7,8]}
df = pd.DataFrame(data=d)
print(df)
result = df.groupby(['col1', 'col2']).size().reset_index().rename(columns={0:'count'})
print(result)
result["count"].hist(by = result[['col1', 'col2']])
plt.show()
