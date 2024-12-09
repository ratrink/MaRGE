# Import necessary libraries and base class
import os
import sys
main_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(main_directory)
parent_directory = os.path.dirname(parent_directory)
# Define the subdirectories you want to add to sys.path
subdirs = ['MaRGE', 'marcos_client']

# Add the subdirectories to sys.path
for subdir in subdirs:
    full_path = os.path.join(parent_directory, subdir)
    sys.path.append(full_path)


    
import experiment as ex
import numpy as np
import seq.mriBlankSeq as blankSeq  # Import the mriBlankSequence for any new sequence.
import scipy.signal as sig
import configs.hw_config as hw
import configs.units as units
from scipy.optimize import curve_fit

# Define the TSE sequence
class TSESequence(blankSeq.MRIBLANKSEQ):
    def __init__(self):
        super(TSESequence, self).__init__()
        # Set up parameters
        self.addParameter(key='seqName', string='TSEInfo', val='TSE')
        self.addParameter(key='nScans', string='Number of scans', val=1, field='SEQ')
        self.addParameter(key='larmorFreq', string='Larmor frequency (MHz)', val=3.08, field='RF')
        self.addParameter(key='rfExAmp', string='RF excitation amplitude (a.u.)', val=0.3, field='RF')
        self.addParameter(key='rfReAmp', string='RF refocusing amplitude (a.u.)', val=0.3, field='RF')
        self.addParameter(key='rfExTime', string='RF excitation time (us)', val=30.0, field='RF')
        self.addParameter(key='rfReTime', string='RF refocusing time (us)', val=60.0, field='RF')
        self.addParameter(key='echoSpacing', string='Echo spacing (ms)', val=10.0, field='SEQ')
        self.addParameter(key='repetitionTime', string='Repetition time (ms)', val=1000.0, field='SEQ')
        self.addParameter(key='nPoints', string='Number of acquired points', val=256, field='IM')
        self.addParameter(key='etl', string='Echo train length', val=50, field='SEQ')

    def sequenceRun(self, demo=False):
        self.demo = demo

        # Initialize sequence timing
        t0 = 20e3  # us
        self.iniSequence(t0, shimming=[0, 0, 0])

        # Excitation and Echo Train
        for scan in range(self.mapVals['nScans']):
            tEx = t0 + scan * self.mapVals['repetitionTime'] * 1e3
            self.rfRecPulse(tEx - hw.blkTime - self.mapVals['rfExTime'] / 2,
                            self.mapVals['rfExTime'], self.mapVals['rfExAmp'])

            for echo_idx in range(self.mapVals['etl']):
                tEcho = tEx + (echo_idx + 1) * self.mapVals['echoSpacing'] * 1e3

                # Refocusing pulse
                self.rfRecPulse(tEcho - self.mapVals['echoSpacing'] * 1e3 / 2 - hw.blkTime - self.mapVals['rfReTime'] / 2,
                                self.mapVals['rfReTime'], self.mapVals['rfReAmp'])

                # Acquisition gate
                self.rxGate(tEcho - self.mapVals['rfExTime'] / 2, self.mapVals['rfExTime'])

        # Finalize sequence
        self.endSequence(t0 + self.mapVals['nScans'] * self.mapVals['repetitionTime'] * 1e3)
        print("Sequence complete.")

# Instantiate and run the TSE sequence
# tse_seq = TSESequence()
# tse_seq.sequenceRun(demo=True)
