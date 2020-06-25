import numpy as np
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

        cpp_code_mean = cpp_code_rpb.groupby(["Records_per_buffer", "percentage[%]"], as_index=False).agg(
            {'Efficiency': ['mean', 'std']})

        python_code_mean = python_code_rpb.groupby(["Records_per_buffer", "percentage[%]"], as_index=False).agg(
            {'Efficiency': ['mean', 'std']})

        x_python = python_code_mean["percentage[%]"].values
        y_python = python_code_mean["Efficiency"]["mean"].values
        y_python_errors = python_code_mean["Efficiency"]["std"].values

        x_cpp = cpp_code_mean["percentage[%]"].values
        y_cpp = cpp_code_mean["Efficiency"]["mean"].values
        y_cpp_errors = cpp_code_mean["Efficiency"]["std"].values

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 7), sharex=True)
        fig.suptitle("NPT Average for Cpp vs Python efficiency; decimation = " +
                     str(1) + " buffer size = 4" + " records_per_buffer = " +
                     str(records_per_buffer) + " buffers_per_acquisition = 100")

        ax1.errorbar(x_cpp, y_cpp, yerr=y_cpp_errors, label='Cpp avg efficiency', fmt='o', c="r", capthick=2,
                     uplims=True, lolims=True)
        ax2.errorbar(x_python, y_python, yerr=y_python_errors, label='Python avg efficiency', fmt='o', c="b",
                     capthick=2, uplims=True, lolims=True)
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

        results_data_file = "/home/useme/Przemek//ATS9870_Results/resultsFile_correct.txt"
        python_code, cpp_code = self.__data_processor.pass_data_to_plot(results_data_file)
        plt.figure(figsize=(18, 10))
        plt.subplot(211)
        for i in [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]:
            print("Plotting for: " + str(i) + " records_per_buffers")
            cpp_code_rpb = cpp_code.loc[cpp_code["Records_per_buffer"] == i]
            cpp_code_mean = cpp_code_rpb.groupby(["Records_per_buffer", "percentage[%]"], as_index=False).agg(
                {'Efficiency': ['mean', 'std']})

            label = str(i) + " RPB"

            x_cpp = cpp_code_mean["percentage[%]"].values
            y_cpp = cpp_code_mean["Efficiency"]["mean"].values
            y_cpp_errors = cpp_code_mean["Efficiency"]["std"].values

            plt.errorbar(x_cpp, y_cpp, yerr=y_cpp_errors, label=label, fmt='o', capthick=2,
                         uplims=True, lolims=True)

        plt.xticks(np.arange(0, 100, step=10))
        plt.axhline(y=0.5, color='r', ls=":")
        plt.yticks(np.arange(0.2, 1.1, step=0.1))
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.1, 1.02), loc="upper right")
        plt.xlabel('t_total/t_trigger [%]')
        plt.ylabel('Efficiency')
        plt.title("NPT Average for Cpp and Python efficiency for all examples")

        plt.subplot(212)
        for i in [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]:
            print("Plotting for: " + str(i) + " records_per_buffers")
            python_code_rpb = python_code.loc[python_code["Records_per_buffer"] == i]

            python_code_mean = python_code_rpb.groupby(["Records_per_buffer", "percentage[%]"], as_index=False).agg(
                {'Efficiency': ['mean', 'std']})

            label_cpp = str(i) + "records per buffer"
            x_python = python_code_mean["percentage[%]"].values
            y_python = python_code_mean["Efficiency"]["mean"].values
            y_python_errors = python_code_mean["Efficiency"]["std"].values

            plt.errorbar(x_python, y_python, yerr=y_python_errors, label=label_cpp, fmt='o', capthick=2,
                         uplims=True, lolims=True)

        plt.xticks(np.arange(0, 100, step=10))
        plt.yticks(np.arange(0.2, 1.1, step=0.1))
        plt.grid(True)
        plt.axhline(y=0.5, color='r', ls=":")
        plt.xlabel('t_total/t_trigger [%]')
        plt.ylabel('Efficiency')

        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/cpp_python_overall.png")


        return


def main():
    dv = DataVisualisation()
    """ for i in [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]:
        print("Plotting for: " + str(i) + " records_per_buffers")
        results_data_file = "/home/useme/Przemek//ATS9870_Results/resultsFile_correct.txt"
        dv.plot_test_data(results_data_file=results_data_file, records_per_buffer=i)"""
    dv.plot_data()
    del dv
    return


if __name__ == '__main__':
    main()
