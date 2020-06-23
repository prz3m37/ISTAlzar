from time import gmtime, strftime
import pandas as pd
import numpy as np


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def parse_config_file(config_file: str, configuration_set: str) -> dict:
        params_container = {}
        try:
            cfg_file = open(config_file, 'r')
            for line in cfg_file:
                if configuration_set in line:
                    for sub_line in cfg_file:
                        param_set = sub_line.split('=')
                        if str(param_set[0]).startswith("Set") or str(param_set[0]).startswith("\n"):
                            break
                        else:
                            param_name, param_value = param_set[0], float(param_set[1])
                            params_container[param_name] = param_value
                else:
                    pass
            cfg_file.close()
            print("[INFO]: All params have been red successfully !")
        except IOError:
            print("[ERROR]: The configFile can't be opened !")
        return params_container

    @staticmethod
    def read_results(results_file: str) -> pd.DataFrame:
        results_data = pd.read_csv(results_file, delimiter=" ")
        return results_data

    def save_test_data(self, results_file: str, captured_time: float, records_per_buffer: int,
                       buffers_per_acquisition: int, number_of_points: int, decimation: int) -> None:

        current_time = self.__get_current_time()
        test_data = "[PyhCode] " + str(current_time) + " " + str(captured_time) + " " + str(records_per_buffer) \
                    + " " + str(buffers_per_acquisition) + " " + str(number_of_points) + " " + str(decimation) + "\n"
        try:
            res_file = open(results_file, 'a')
            res_file.write(test_data)
            res_file.close()
            print("[INFO]: Captured time successfully saved !")
        except IOError:
            print("[ERROR]: The resultsFile can't be opened !")
        return

    @staticmethod
    def __get_current_time() -> str:
        return strftime("%Y-%m-%d-%H:%M:%S", gmtime())

    @staticmethod
    def __open_binary_files(data_path, data_avg_path):
        f = open(data_path, "r")
        data = np.fromfile(f, dtype=np.uint8)
        f.close()

        f_avg = open(data_avg_path, "r")
        data_avg = np.fromfile(f, dtype=np.uint8)
        f_avg.close()

        return data, data_avg
'''
    def __parse_binary_data(self):
        self.__open_binary_files()
        return

    def __get_test_version(self):
        return

'''
