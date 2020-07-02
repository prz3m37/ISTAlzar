import numpy as np
import matplotlib.pyplot as plt
from DataProcessor import DataProcessor
import seaborn as sns


class DataVisualisation(DataProcessor):

    def __init__(self):
        sns.set()
        self.__data_processor = DataProcessor()

    def __del__(self):
        del self.__data_processor

    @staticmethod
    def plot_test_data(x_python, y_python, x_cpp, y_cpp, y_python_errors, y_cpp_errors,
                       title: str) -> None:

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 7), sharex=True)
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
        fig.suptitle(title)
        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/" + str(title) + ".png")
        plt.close()
        return

    @staticmethod
    def plot_test_data_overall(results_data, values_of_parameter, parameter, pass_data_to_plot):
        plt.figure(figsize=(18, 10))
        #plt.subplot(211)
        for value in values_of_parameter:
            label = str(value) + " " + parameter
            x_c, y_c, y_c_err = pass_data_to_plot(results_data=results_data, parameter=parameter,
                                                  value_of_parameter=value, code_language="cpp")
            plt.errorbar(x_c, y_c, yerr=y_c_err, label=label, fmt='o', capthick=2,
                         uplims=True, lolims=True)

            plt.xticks(np.arange(0, 100, step=10))
            plt.axhline(y=0.5, color='r', ls=":")
            plt.yticks(np.arange(0.2, 1.1, step=0.1))
            plt.grid(True)
            plt.legend(bbox_to_anchor=(1.1, 1.02), loc="upper right")
            plt.xlabel('t_total/t_trigger [%]')
            plt.ylabel('Efficiency')
            plt.title("NPT Average for Cpp efficiency for all examples")
            plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/Cpp_90_overall.png")
            plt.close()

        """  plt.subplot(212)
        for value in values_of_parameter:
            label = str(value) + " " + parameter
            x_p, y_p, y_p_err = pass_data_to_plot(results_data=results_data, parameter=parameter,
                                                  value_of_parameter=value, code_language="python")
            plt.errorbar(x_p, y_p, yerr=y_p_err, label=label, fmt='o', capthick=2,
                         uplims=True, lolims=True)

        plt.xticks(np.arange(0, 100, step=10))
        plt.yticks(np.arange(0.2, 1.1, step=0.1))
        plt.grid(True)
        plt.axhline(y=0.5, color='r', ls=":")
        plt.xlabel('t_total/t_trigger [%]')
        plt.ylabel('Efficiency')"""


        return

    @staticmethod
    def plot_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B):
        time = np.arange(0, 64, 1)
        plt.figure(figsize=(18, 10))
        plt.subplot(211)
        plt.plot(time, ch_A_avg, '-o', label="Channel A post averaging")
        plt.plot(time, data_avg_ch_A, '-o', label="Channel A code averaging")
        plt.axvline(x=50, color='r', ls=":")
        plt.xlabel('Time[ns]')
        plt.ylabel('Voltage[V]')
        plt.legend()
        plt.title("Channel averages comparision")

        plt.subplot(212)
        plt.plot(time, ch_B_avg, '-o', label="Channel B post averaging")
        plt.plot(time, data_avg_ch_B, '-o', label="Channel B code averaging")
        plt.axvline(x=50, color='r', ls=":")
        plt.xlabel('Time[ns]')
        plt.ylabel('Voltage[V]')
        plt.legend()
        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/channels_data_avg_comparison.png")
        plt.close()
        return

    @staticmethod
    def plot_account_sets(data) -> None:
        data.plot.bar(x="Data", y="Count", rot=45, figsize=(15, 17))
        plt.title("Statistic for sets")
        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/values_histogram.png")
        plt.close()
        return

    @staticmethod
    def plot_density(results_data, code_language, pass_data_to_density_plot):
        rec_per_buffer, buff_per_acq, efficiency = pass_data_to_density_plot(results_data, code_language)
        plt.figure(figsize=(15, 10))
        plt.scatter(rec_per_buffer, buff_per_acq, cmap='inferno', c=efficiency, s=100)
        plt.colorbar()
        plt.title("Efficiency for PTS=9088 and different RPB and BPA")
        plt.ylabel('Buffers per acquisition')
        plt.xlabel('Records per buffer')
        plt.savefig("/home/useme/Przemek/ATS9870_Results/PlotResults/density_plot.png")
        plt.close()
        return
