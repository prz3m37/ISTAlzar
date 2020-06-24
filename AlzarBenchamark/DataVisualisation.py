import matplotlib.pyplot as plt
from DataProcessor import DataProcessor


class DataVisualisation(DataProcessor):

    def __init__(self):
        self.__data_processor = DataProcessor()

    def __del__(self):
        del self.__data_processor

    def plot_test_data(self, results_data_file: str, records_per_buffer: int) -> None:
        python_code, cpp_code = self.__data_processor.pass_data_to_plot(results_data_file)

        python_code_rpb = python_code.loc[python_code["Records_per_buffer"] == records_per_buffer]
        cpp_code_rpb = cpp_code.loc[cpp_code["Records_per_buffer"] == records_per_buffer]

        x_python = python_code_rpb["percentage[%]"].values
        y_python = python_code_rpb["Efficiency"].values

        x_cpp = cpp_code_rpb["percentage[%]"].values
        y_cpp = cpp_code_rpb["Efficiency"].values

        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(15, 7))

        fig.suptitle("NPT Average for Cpp vs Python efficiency; decimation = " +
                     str(1) + " buffer size = 4" + " records_per_buffer = " +
                     str(records_per_buffer) + " buffers_per_acquisition = 100")
        ax1.scatter(x_cpp, y_cpp, c="b", marker="D", label='Cpp code')
        ax2.scatter(x_python, y_python, c="r", marker="D", label='Python code')
        ax1.legend(loc="upper right")
        ax2.legend(loc="upper right")
        fig.text(0.5, 0.04, 't_total/t_trigger [%]', ha='center', va='center')
        fig.text(0.06, 0.5, 'Efficiency', ha='center', va='center', rotation='vertical')
        ax1.grid()
        ax2.grid()
        ax1.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax1.set_xticklabels([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], fontsize=12)
        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/" + "decimation = " +
                    str(1) + " buffer size = 4" + " records_per_buffer = " +
                    str(records_per_buffer) + " buffers_per_acquisition = 100")

        return

    def plot_data(self):
        return


def main():
    dv = DataVisualisation()
    for i in [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]:
        print("Plotting for: " + str(i) + " records_per_buffers")
        results_data_file = "/home/useme/Przemek//ATS9870_Results/resultsFile2.txt"
        dv.plot_test_data(results_data_file=results_data_file, records_per_buffer=i)
    del dv
    return


if __name__ == '__main__':
    main()
