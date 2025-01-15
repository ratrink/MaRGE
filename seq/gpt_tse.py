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

import pypulseq as pp
from scipy.signal import decimate

class TurboSpinEcho(blankSeq.MRIBLANKSEQ):
    def __init__(self):
        super(TurboSpinEcho, self).__init__()
        # Define sequence parameters
        self.addParameter(key='seqName', string='TSEInfo', val='TSE')
        self.addParameter(key='nScans', string='Number of scans', val=1, field='IM')
        self.addParameter(key='rfExFA', string='Excitation flip angle (º)', val=90, field='RF')
        self.addParameter(key='rfReFA', string='Refocusing flip angle (º)', val=180, field='RF')
        self.addParameter(key='echoSpacing', string='Echo spacing (ms)', val=10.0, units=units.ms, field='SEQ')
        self.addParameter(key='fov', string='Field of View [x, y, z] (cm)', val=[15.0, 15.0, 15.0], units=units.cm, field='IM')
        self.addParameter(key='nPoints', string='Matrix size [rd, ph, sl]', val=[128, 128, 128], field='IM')
        self.addParameter(key='etl', string='Echo train length', val=16, field='SEQ')
        self.addParameter(key='repetitionTime', string='Repetition time (ms)', val=500.0, units=units.ms, field='SEQ')
        self.addParameter(key='acqTime', string='Acquisition time (ms)', val=4.0, units=units.ms, field='SEQ')
        self.addParameter(key='rfExTime', string='RF excitation time (us)', val=60.0, units=units.us, field='RF')  # Added
        self.addParameter(key='rfReTime', string='RF refocusing time (us)', val=120.0, units=units.us, field='RF')  # Added
        

    def sequenceRun(self):
        self.rfExFA = self.mapVals['rfExFA']
        self.rfReFA = self.mapVals['rfReFA']
        self.echoSpacing = self.mapVals['echoSpacing']
        self.fov = self.mapVals['fov']
        self.nPoints = self.mapVals['nPoints']
        self.etl = self.mapVals['etl']

        print("Running Turbo Spin Echo sequence...")

        # Define hardware and system options
        self.system = pp.Opts(
            max_grad=hw.gFactor[0] * hw.gammaB * 1e3,  # Max gradient strength (mT/m)
            max_slew=hw.max_slew_rate,                # Max slew rate (mT/m/ms)
            rf_dead_time=hw.blkTime * 1e-6,           # RF dead time (s)
            grad_raster_time=hw.grad_raster_time,     # Gradient raster time (s)
        )

        # Define RF pulses
        flip_ex = self.rfExFA * np.pi / 180
        rf_ex = pp.make_block_pulse(
            flip_angle=flip_ex,
            system=self.system,
            duration=self.mapVals['rfExTime'] * 1e-6  # Convert from us to seconds
        )

        flip_re = self.rfReFA * np.pi / 180
        rf_re = pp.make_block_pulse(
            flip_angle=flip_re,
            system=self.system,
            duration=self.mapVals['rfReTime'] * 1e-6  # Convert from us to seconds
        )

        # Calculate gradient parameters
        fov = np.array(self.fov) * 1e-2  # Convert FOV from cm to m
        matrix_size = np.array(self.nPoints)
        resolution = fov / matrix_size

        rd_grad_amplitude = 1 / (hw.gammaB * resolution[0] * self.mapVals['acqTime'] * 1e-3)
        rd_grad = pp.make_trapezoid(
            channel='x',
            system=self.system,
            amplitude=rd_grad_amplitude,
            flat_time=self.mapVals['acqTime'] * 1e-3,  # Convert from ms to seconds
            rise_time=hw.grad_rise_time
        )

        adc = pp.make_adc(
            num_samples=matrix_size[0],
            dwell=self.mapVals['acqTime'] * 1e-6 / matrix_size[0],
            delay=rd_grad.rise_time
        )

        
        # Slice selection gradient
        slice_thickness = resolution[2]  # Define slice thickness (in meters)
        sl_grad_amplitude = 1 / (hw.gammaB * slice_thickness * self.mapVals['rfExTime'] * 1e-6)
        sl_grad = pp.make_trapezoid(
            channel='z',
            system=self.system,
            amplitude=sl_grad_amplitude,
            flat_time=self.mapVals['rfExTime'] * 1e-6,
            rise_time=hw.grad_rise_time
        )

        # Slice rephasing gradient
        sl_reph_amplitude = -sl_grad_amplitude / 2
        sl_reph = pp.make_trapezoid(
            channel='z',
            system=self.system,
            amplitude=sl_reph_amplitude,
            flat_time=self.mapVals['rfExTime'] * 1e-6 / 2,
            rise_time=hw.grad_rise_time
        )
        
        # Phase encoding gradients
        ph_grad_amplitude = np.linspace(-1, 1, matrix_size[1]) / (hw.gammaB * fov[1])
        phase_gradients = [
            pp.make_trapezoid(
                channel='y',
                system=self.system,
                amplitude=amp,
                flat_time=self.mapVals['echoSpacing'] * 1e-3 / 2 - hw.grad_rise_time,
                rise_time=hw.grad_rise_time
            ) for amp in ph_grad_amplitude
        ]
        # Sequence blocks
        seq = pp.Sequence(self.system)

        for phase_grad in phase_gradients:
            seq.add_block(rf_ex)  # Excitation pulse
            seq.add_block(rd_grad, adc)  # Readout gradient and ADC

            for _ in range(self.etl):
                seq.add_block(rf_re)  # Refocusing pulse
                seq.add_block(phase_grad)  # Phase encoding gradient
                seq.add_block(rd_grad, adc)  # Readout gradient and ADC

        # Save the sequence
        # Save the sequence
        seq.write("turbo_spin_echo.seq")
        print("Turbo Spin Echo sequence saved to 'turbo_spin_echo.seq'")
        
        # Plot the sequence
        seq.plot()  # Plots the sequence, including gradients

if __name__ == "__main__":
    tse = TurboSpinEcho()
    tse.sequenceRun()
