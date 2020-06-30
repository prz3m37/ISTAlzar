from DataProcessor import DataProcessor
from DataVisualisation import DataVisualisation


def main():
    data_processor = DataProcessor()
    data_visualisations = DataVisualisation()

    results_data_file = "/home/useme/Przemek//ATS9870_Results/resultsFile_correct.txt"
    data_path, data_avg_path = None, None
    buffers_per_acq = None
    parameter = ""
    values_of_parameter = [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]

    ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B = data_processor.prepare_channel_avg_data(data_path, data_avg_path,
                                                                                               buffers_per_acq)

    fidelity = data_processor.compare_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B)
    if fidelity:
        results_data = data_processor.prepare_data(results_data_file)
        results_data = data_processor.evaluate_efficiency(results_data=results_data, time_of_experiment=10000)
        data_visualisations.plot_test_data_overall(results_data, values_of_parameter,
                                                   parameter, data_processor.pass_data_to_plot)
        data_visualisations.plot_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B)
    else:
        print("[ERROR] Check the signals")

    del data_processor
    del data_visualisations

    return


if __name__ == '__main__':
    main()
