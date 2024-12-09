import os
import sys
#*****************************************************************************
# Get the directory of the current script
main_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(main_directory)
parent_directory = os.path.dirname(parent_directory)

# Define the subdirectories you want to add to sys.path
subdirs = ['MaRGE', 'marcos_client']

# Add the subdirectories to sys.path
for subdir in subdirs:
    full_path = os.path.join(parent_directory, subdir)
    sys.path.append(full_path)
#******************************************************************************
import controller.experiment_gui as ex
import numpy as np
import seq.mriBlankSeq as blankSeq  # Import the mriBlankSequence for any new sequence.
import configs.hw_config as hw
import configs.units as units

class TSE(blankSeq.MRIBLANKSEQ):
    def __init__(self):
        super(TSE, self).__init__()

        self.addParameter(key='seqName', string='TSEInfo', val='TSE')

        self.addParameter(key='nScans', string='Number of scans', val=1, field='SEQ') # trs

        self.addParameter(key='larmorFreq', string='Larmor frequency (MHz)', val=16.5, units=units.MHz, field='RF') # lo_freq
        
        self.addParameter(key='rfExAmp', string='RF excitation amplitude (a.u.)', val=0.3, field='RF') # rf_amp excitation

        self.addParameter(key='rfReAmp', string='RF refocusing amplitude (a.u.)', val=0.3, field='RF') #rf_amp refocusing

        self.addParameter(key='rfExTime', string='RF excitation time (us)', val=30.0, units=units.us, field='RF') # rf_pi2_duration (pi/2 = 90 degree flip angle) -> Excitation

        self.addParameter(key='rfReTime', string='RF refocusing time (us)', val=60.0, units=units.us, field='RF') # 2*rf_pi2_duration = rf_pi_duration = pi = 180 degree flip angle -> refocusing

        self.addParameter(key='echoSpacing', string='Echo spacing (ms)', val=10.0, units=units.ms, field='SEQ') # echo_duration

        self.addParameter(key='repetitionTime', string='Repetition time (ms)', val=3000, units=units.ms, field='SEQ') # tr_pause_duration + echo_duration*echos_per_tr

        self.addParameter(key='nPoints', string='Number of acquired points', val=60, field='IM') # non_existent

        self.addParameter(key='fov', string='FOV (cm)', val=[4.0, 4.0, 4.0], field='IM')
        
        self.addParameter(key='dfov', string='dFOV (mm)', val=[0.0, 0.0, 0.0], field='IM')

        self.addParameter(key='etl', string='Echo train length', val=5, field='SEQ') # echos_per_tr
        self.addParameter(key='acqTime', string='Acquisition time (ms)', val=2.0, units=units.ms, field='SEQ') # readout_duration
        self.addParameter(key='shimming', string='shimming', val=[0.0, 0.0, 0.0], units=units.sh, field='OTH') # Shimming (non existent)


    def sequenceInfo(self):
        
        print("TSE")
        print("Author: Raphael Trinkler")
        print("Contact: raphael.trinkler@student.tugraz.at")
        print("This sequence runs a Turbo Spin Echo")

    def sequenceTime(self):
        nScans = self.mapVals['nScans']
        repetitionTime = self.mapVals['repetitionTime']*1e-3
        return(repetitionTime*nScans/60)  # minutes, scanTime
    

    def sequenceRun(self, plotSeq=0, demo=False):
        self.demo = demo
        
        # Create sequence instructions
        
        # Input instructions into the Red Pitaya
        
        # Use the plotSeq argument to control plotting versus running.
        
        # Use the demo argument to control if you want to simulate signals.

    def sequenceAnalysis(self, mode=None):
        self.mode = mode
        ...
        result1 = {}
        result2 = {}
        ...
        self.output = [result1, result2]
        
        return self.output
        
        
        # Implement data analysis logic here