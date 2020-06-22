from __future__ import division
import ctypes
import numpy as np
import os
import signal
import gc
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'Library'))
sys.path.append('/home/useme/Przemek/PythonVersion/ISTAlzar/AlzarBenchamark')

import atsapi as ats
from Utils import Utils


class ATSPython:

    def __init__(self):
        self.__utils = Utils()
        self.__captured_time = None
        self.__trigger_delay = None
        self.__bytes_transferred = None

    # Configures a board for acquisition
    def ConfigureBoard(self, board):
        # TODO: Select clock parameters as required to generate this
        # sample rate
        #
        # For example: if samplesPerSec is 100e6 (100 MS/s), then you can
        # either:
        #  - select clock source INTERNAL_CLOCK and sample rate
        #    SAMPLE_RATE_100MSPS
        #  - or select clock source FAST_EXTERNAL_CLOCK, sample rate
        #    SAMPLE_RATE_USER_DEF, and connect a 100MHz signal to the
        #    EXT CLK BNC connector
        global samplesPerSec
        samplesPerSec = 1000000000.0
        board.setCaptureClock(ats.INTERNAL_CLOCK,
                              ats.SAMPLE_RATE_1GSPS,
                              ats.CLOCK_EDGE_RISING,
                              0)

        # TODO: Select channel A input parameters as required.
        board.inputControlEx(ats.CHANNEL_A,
                             ats.DC_COUPLING,
                             ats.INPUT_RANGE_PM_400_MV,
                             ats.IMPEDANCE_50_OHM)

        # TODO: Select channel A bandwidth limit as required.
        board.setBWLimit(ats.CHANNEL_A, 0)

        # TODO: Select channel B input parameters as required.
        board.inputControlEx(ats.CHANNEL_B,
                             ats.DC_COUPLING,
                             ats.INPUT_RANGE_PM_400_MV,
                             ats.IMPEDANCE_50_OHM)

        # TODO: Select channel B bandwidth limit as required.
        board.setBWLimit(ats.CHANNEL_B, 0)

        # TODO: Select trigger inputs and levels as required.
        board.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                                  ats.TRIG_ENGINE_J,
                                  ats.TRIG_CHAN_A,
                                  ats.TRIGGER_SLOPE_POSITIVE,
                                  150,
                                  ats.TRIG_ENGINE_K,
                                  ats.TRIGGER_SLOPE_POSITIVE,
                                  ats.TRIG_DISABLE,
                                  128)

        # TODO: Select external trigger parameters as required.
        board.setExternalTrigger(ats.DC_COUPLING,
                                 ats.ETR_5V)

        # TODO: Set trigger delay as required.
        triggerDelay_sec = 0
        self.__trigger_delay = triggerDelay_sec
        triggerDelay_samples = int(triggerDelay_sec * samplesPerSec + 0.5)
        board.setTriggerDelay(triggerDelay_samples)

        # TODO: Set trigger timeout as required.
        #
        # NOTE: The board will wait for a for this amount of time for a
        # trigger event.  If a trigger event does not arrive, then the
        # board will automatically trigger. Set the trigger timeout value
        # to 0 to force the board to wait forever for a trigger event.
        #
        # IMPORTANT: The trigger timeout value should be set to zero after
        # appropriate trigger parameters have been determined, otherwise
        # the board may trigger if the timeout interval expires before a
        # hardware trigger event arrives.
        triggerTimeout_sec = 0
        triggerTimeout_clocks = int(triggerTimeout_sec / 10e-6 + 0.5)
        board.setTriggerTimeOut(triggerTimeout_clocks)

        # Configure AUX I/O connector as required
        board.configureAuxIO(ats.AUX_OUT_TRIGGER,
                             0)
        return

    def AcquireData(self, board):
        # No pre-trigger samples in NPT mode
        preTriggerSamples = 0

        # TODO: Select the number of samples per record.
        postTriggerSamples = 2048

        # TODO: Select the number of records per DMA buffer.
        recordsPerBuffer = 1

        # TODO: Select the number of buffers per acquisition.
        buffersPerAcquisition = 1

        # TODO: Select the active channels.
        channels = ats.CHANNEL_A | ats.CHANNEL_B
        channelCount = 0
        for c in ats.channels:
            channelCount += (c & channels == c)

        # TODO: Should data be saved to file?
        saveData = True
        dataFile = None

        # TODO : Should averaged data be saved to file?
        saveAvgData = True
        dataAvgFile = None

        if saveData:
            dataFile = open(os.path.join(os.path.dirname(__file__),
                                         "data.bin"), 'wb')

        if saveAvgData:
            dataAvgFile = open(os.path.join(os.path.dirname(__file__),
                                            "data_avg.bin"), 'wb')

        # Compute the number of bytes per record and per buffer
        memorySize_samples, bitsPerSample = board.getChannelInfo()
        bytesPerSample = (bitsPerSample.value + 7) // 8
        samplesPerRecord = preTriggerSamples + postTriggerSamples
        bytesPerRecord = bytesPerSample * samplesPerRecord
        bytesPerBuffer = bytesPerRecord * recordsPerBuffer * channelCount

        # TODO: Select number of DMA buffers to allocate
        bufferCount = 4
        buffer_list = [[] for _ in range(channelCount)]
        # Allocate DMA buffers

        sample_type = ctypes.c_uint8
        if bytesPerSample > 1:
            sample_type = ctypes.c_uint16

        buffers = []
        for i in range(bufferCount):
            buffers.append(ats.DMABuffer(board.handle, sample_type, bytesPerBuffer))

        # Set the record size
        board.setRecordSize(preTriggerSamples, postTriggerSamples)

        recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition

        # Configure the board to make an NPT AutoDMA acquisition
        board.beforeAsyncRead(channels,
                              -preTriggerSamples,
                              samplesPerRecord,
                              recordsPerBuffer,
                              recordsPerAcquisition,
                              ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)

        # Post DMA buffers to board
        for buffer in buffers:
            board.postAsyncBuffer(buffer.addr, buffer.size_bytes)

        start = time.clock()  # Keep track of when acquisition started // It is CPU time so it's good
        try:
            board.startCapture()  # Start the acquisition
            print("Capturing %d buffers. Press <enter> to abort" %
                  buffersPerAcquisition)
            buffersCompleted = 0
            bytesTransferred = 0
            while buffersCompleted < buffersPerAcquisition and not ats.enter_pressed():
                # Wait for the buffer at the head of the list of available
                # buffers to be filled by the board.
                buffer = buffers[buffersCompleted % len(buffers)]
                board.waitAsyncBufferComplete(buffer.addr, timeout_ms=5000)
                buffersCompleted += 1
                bytesTransferred += buffer.size_bytes
                channel_split = np.split(buffer.buffer, channelCount)
                # TODO: Process sample data in this buffer. Data is available
                # as a NumPy array at buffer.buffer

                # NOTE:
                #
                # While you are processing this buffer, the board is already
                # filling the next available buffer(s).
                #
                # You MUST finish processing this buffer and post it back to the
                # board before the board fills all of its available DMA buffers
                # and on-board memory.
                #
                # Samples are arranged in the buffer as follows:
                # S0A, S0B, ..., S1A, S1B, ...
                # with SXY the sample number X of channel Y.
                #
                # Sample code are stored as 8-bit values.
                #
                # Sample codes are unsigned by default. As a result:
                # - 0x00 represents a negative full scale input signal.
                # - 0x80 represents a ~0V signal.
                # - 0xFF represents a positive full scale input signal.
                # Optionaly save data to file
                if dataFile:
                    buffer.buffer.tofile(dataFile)
                # TODO: Check if this is calculated properly and saved properly => In fact we can test already
                #  becnchmark :D
                for channel in range(channelCount):
                    buffer_split = np.split(channel_split[channel], recordsPerBuffer)
                    buffer_mean = np.mean(buffer_split, 0)
                    buffer_list[channel].append(buffer_mean)

                buffer_list_mean = np.mean(buffer_list, 1)
                channel_A = buffer_list_mean[0]
                channel_B = buffer_list_mean[1]
                alternating_buffer_list_mean = np.ravel([channel_A, channel_B], 'F')
                if saveAvgData:
                    alternating_buffer_list_mean.tofile(dataAvgFile)
                # Add the buffer to the end of the list of available buffers.
                board.postAsyncBuffer(buffer.addr, buffer.size_bytes)
        finally:
            board.abortAsyncRead()
        # Compute the average of signal/signals.

        # Compute the total transfer time, and display performance information.
        transferTime_sec = time.clock() - start
        print("Capture completed in %f sec" % transferTime_sec)
        buffersPerSec = 0
        bytesPerSec = 0
        recordsPerSec = 0
        if transferTime_sec > 0:
            buffersPerSec = buffersCompleted / transferTime_sec
            bytesPerSec = bytesTransferred / transferTime_sec
            recordsPerSec = recordsPerBuffer * buffersCompleted / transferTime_sec
        print("Captured %d buffers (%f buffers per sec)" %
              (buffersCompleted, buffersPerSec))
        print("Captured %d records (%f records per sec)" %
              (recordsPerBuffer * buffersCompleted, recordsPerSec))
        print("Transferred %d bytes (%f bytes per sec)" %
              (bytesTransferred, bytesPerSec))
        self.__captured_time = transferTime_sec
        self.__bytes_transferred = bytesTransferred
        del buffer_list_mean
        gc.collect()
        return

    def run_ats(self):
        board = ats.Board(systemId=1, boardId=1)
        self.ConfigureBoard(board)
        self.AcquireData(board)
        results_file_path = "/home/useme/Przemek/CppVersion/ATS9870/DualPort/NPT_Average/resultsFile.txt"
        self.__utils.save_test_data(results_file_path, self.__captured_time,
                                    self.__bytes_transferred, self.__trigger_delay)


def main():
    ats = ATSPython()
    ats.run_ats()


if __name__ == "__main__":
    main()
