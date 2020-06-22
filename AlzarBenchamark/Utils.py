from time import gmtime, strftime
import pandas as pd


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def parse_config_file(config_file: str) -> dict:
        params_container = {}
        try:
            cfg_file = open(config_file, 'r')
            for line in cfg_file.readlines():
                param_set = line.split('=')
                param_name, param_value = param_set[0], param_set[1]
                params_container[param_name] = param_value
            cfg_file.close()
            print("[INFO]: All params have been red successfully !")
        except IOError:
            print("[ERROR]: The configFile can't be opened !")
        return params_container

    @staticmethod
    def read_results(results_file: str) -> pd.DataFrame:
        results_data = pd.read_csv(results_file)
        return results_data

    def save_test_data(self, results_file: str, captured_time: float, records_per_buffer: int,
                       buffers_per_acquisition: int, number_of_points: int, decimation:int) -> None:

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
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def __get_test_version(self):
        return
