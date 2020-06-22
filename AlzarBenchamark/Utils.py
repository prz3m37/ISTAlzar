from time import gmtime, strftime
import pandas as pd


class Utils(object):

    def __init__(self):
        pass

    @staticmethod
    def read_results(results_file: str) -> pd.DataFrame:
        results_data = pd.read_csv(results_file)
        return results_data

    def save_test_data(self, results_file: str, captured_time: float,
                       number_of_points: int, trigger_delay: float = None) -> None:

        current_time = self.__get_current_time()
        test_data = "[PyhCode] " + str(current_time) + " " + \
                    str(captured_time) + " " + str(number_of_points) \
                    + " " + str(trigger_delay) + "\n"
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
