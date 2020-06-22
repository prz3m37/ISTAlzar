import matplotlib.pyplot as plt
from DataProcessor import DataProcessor


class DataVisualisation(DataProcessor):

    def __init__(self):
        self.__data_processor = DataProcessor()

    def __del__(self):
        del self.__data_processor

    def plot_data(self) -> None:
        python_code, cpp_code, decimation = self.__data_processor.pass_data_to_plot()

        x_python = python_code["percentage[%]"].values
        y_python = python_code["Efficiency"].values

        x_cpp = cpp_code["percentage[%]"].values
        y_cpp = cpp_code["Efficiency"].values

        plt.plot(x_python, y_python)
        plt.plot(x_cpp, y_cpp)
        plt.title("NPT Average Cpp vs Python efficiency; decimation = " +
                  str(decimation) + " buffer size = 4")
        plt.show()
        return
