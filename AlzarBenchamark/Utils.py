from time import gmtime, strftime
import pandas as pd


class Utils:

    def __init__(self):
        self.__current_time = None

    @staticmethod
    def read_results(results_file: str) -> pd.DataFrame:
        results_data = pd.read_csv(results_file)
        return results_data

    def save_test_data(self, results_file: str, captured_time: float,
                       number_of_points: int, trigger_delay: float = None) -> None:
        current_time = self.__current_time
        test_data = "[PythonCode] " + str(current_time) + " " + \
                    str(captured_time) + " " + str(number_of_points) + " " + str(trigger_delay) + "\n"

        res_file = open(results_file, 'a')
        res_file.write(test_data)
        res_file.close()
        return

    def __get_current_time(self) -> None:
        self.__current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return

    def __get_test_version(self):
        return
