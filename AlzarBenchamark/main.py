from Utils import Utils
from DataProcessor import DataProcessor
from DataVisualisation import DataVisualisation


# TODO: Run sh script from here but everything else leave in script
def main():
    d_processor = DataProcessor()
    d_visual = DataVisualisation()
    utils = Utils()

    results_data_file = "/home/useme/Przemek/ATS9870_Results/resultsFile_correct.txt"
    data_path, data_avg_path = None, None
    buffers_per_acq = None
    number_of_averages = 5
    parameter = ""
    values_of_parameter = [1000, 1200, 1400, 1600, 1800, 2000, 2300, 2400, 2789, 3000]
    pts = []
    rpb = []
    bpa = []
    utils.generate_config_file(post_trigger_samples=pts, records_per_buff=rpb, buff_per_acq=bpa, decimation=1)
    # TODO: Run shell script

    ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B = d_processor.prepare_channel_avg_data(data_path, data_avg_path,
                                                                                            buffers_per_acq)
    fidelity = d_processor.compare_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B)
    if fidelity:
        cnv_signal_A, cnv_signal_B = d_processor.get_converted_signal(ch_A_avg, ch_B_avg)
        cnv_data_signal_A, cnv_data_signal_B = d_processor.get_converted_signal(data_avg_ch_A, data_avg_ch_B)

        results_data = d_processor.prepare_data(results_data_file)
        results_data = d_processor.evaluate_efficiency(results_data=results_data, time_of_experiment=10000)
        data_for_histogram = d_processor.account_sets(results_data, number_of_averages)

        d_visual.plot_account_sets(data_for_histogram)
        d_visual.plot_test_data_overall(results_data, values_of_parameter, parameter, d_processor.pass_data_to_plot)
        d_visual.plot_averages(cnv_signal_A, cnv_signal_B, cnv_data_signal_A, cnv_data_signal_B)
        # TODO: Get to work this func !!! d_visual.plot_density(rec_per_buffer, buff_per_acq, efficiency)
    else:
        print("[ERROR]: Check the signals")

    del d_processor
    del d_visual

    return


if __name__ == '__main__':
    main()
