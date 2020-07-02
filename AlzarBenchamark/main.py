import os
import config as cfg
from DataProcessor import DataProcessor
from DataVisualisation import DataVisualisation


def generate_config_file(post_trigger_samples: [], records_per_buff: [],
                         buff_per_acq: [], decimation: int = 1):
    cfg_file = open("./configurationFile.txt", 'a')
    i = 1
    for post_trigger_sample in post_trigger_samples:
        for record in records_per_buff:
            for buffer in buff_per_acq:
                message = "*Set%s\n" % i + \
                          "decimation=%s\n" % decimation + \
                          "recordsPerBuffer=%s\n" % record + \
                          "buffersPerAcquisition=%s\n" % buffer + \
                          "postTriggerSamples=%s\n" % post_trigger_sample + "\n"
                i += 1
                cfg_file.write(message)
    cfg_file.close()
    return


# TODO: Run sh script from here but everything else leave in script
def main():

    d_processor = DataProcessor()
    d_visual = DataVisualisation()

    #pts = cfg.configuration["pts"]
    #rpb = cfg.configuration["rpb"]
    #bpa = cfg.configuration["bpa"]
    #parameter = cfg.configuration["parameter"]
    data_path = cfg.configuration["data_path"]
    data_avg_path = cfg.configuration["data_avg_path"]
    buffers_per_acq = cfg.configuration["buffers_per_acq"]
    records_per_buffer = cfg.configuration["records_per_buffer"]
    results_data_file = cfg.configuration["results_data_file"]
    number_of_averages = cfg.configuration["number_of_averages"]
    #values_of_parameter = cfg.configuration["values_of_parameter"]

    #generate_config_file(post_trigger_samples=pts, records_per_buff=rpb, buff_per_acq=bpa, decimation=1)

    #os.system("./runTests.sh")

    ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B = d_processor.prepare_channel_avg_data(data_path,
                                                                                            data_avg_path,
                                                                                            records_per_buffer,
                                                                                            buffers_per_acq)
    fidelity = d_processor.compare_averages(ch_A_avg, ch_B_avg, data_avg_ch_A, data_avg_ch_B)

    if fidelity:
        print("[INFO]: Signals are okay")
    else:
        print("[ERROR]: Check signals")

    cnv_signal_A, cnv_signal_B = d_processor.get_converted_signal(ch_A_avg, ch_B_avg)
    cnv_data_signal_A, cnv_data_signal_B = d_processor.get_converted_signal(data_avg_ch_A, data_avg_ch_B)

    results_data_prep = d_processor.prepare_data(results_data_file)
    results_data = d_processor.evaluate_efficiency(results_data=results_data_prep, time_of_experiment=10000)
    data_for_histogram = d_processor.account_sets(results_data, number_of_averages)

    # TODO: Modificate it or thoro out
    d_visual.plot_account_sets(data_for_histogram)
    for parameter in ["Records_per_buffer", "Buffers_per_acquisition"]:
        if parameter == "Records_per_buffer":
            values_of_parameter = [100, 500, 1000, 3000, 5000, 7000, 8192]
        else:
            values_of_parameter = [50, 70, 100, 200, 300, 400, 500, 512]
        d_visual.plot_test_data_overall(results_data, values_of_parameter, parameter, d_processor.pass_data_to_plot)
    d_visual.plot_averages(cnv_signal_A, cnv_signal_B, cnv_data_signal_A, cnv_data_signal_B)
    d_visual.plot_density(results_data_prep, "cpp", d_processor.pass_data_to_density_plot)

    del d_processor
    del d_visual
    return


if __name__ == '__main__':
    main()
