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
        axesEnable = self.mapVals['axesEnable']
        # Get axes in strings
        axes_dict = {'x': 0, 'y': 1, 'z': 2}
        axes_keys = list(axes_dict.keys())
        axes_vals = list(axes_dict.values())
        axes_str = ['', '', '']
        n = 0
        for val in self.axesOrientation:
            index = axes_vals.index(val)
            axes_str[n] = axes_keys[index]
            n += 1

        if (axesEnable[1] == 0 and axesEnable[2] == 0):
            bw = self.mapVals['bw']*1e-3 # kHz
            t_vector = np.linspace(-self.acq_time/2, self.acq_time/2, self.nPoints[0])*1e-3 # ms
            s_vector = self.mapVals['sampled'][:, 3]
            f_vector = np.linspace(-bw/2, bw/2, self.nPoints[0])
            i_vector = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(s_vector)))
            result1 = {'widget': 'curve',
                       'xData': t_vector,
                       'yData': [np.abs(s_vector), np.real(s_vector), np.imag(s_vector)],
                       'xLabel': 'Time (ms)',
                       'yLabel': "Signal amplitude (mV)",
                       'title': "Signal",
                       'legend': ['Magnitude', 'Real', 'Imaginary'],
                       'row': 0,
                       'col': 0}

            result2 = {'widget': 'curve',
                       'xData': f_vector,
                       'yData': [np.abs(i_vector)],
                       'xLabel': "Frequency (kHz)",
                       'yLabel': "Amplitude (a.u.)",
                       'title': "Spectrum",
                       'legend': ['Spectrum magnitude'],
                       'row': 1,
                       'col': 0}

            self.output = [result1, result2]

        else:
            # Plot image
            image = np.abs(self.mapVals['image3D'])
            image = image / np.max(np.reshape(image, -1)) * 100

            if not self.unlock_orientation:  # Image orientation
                if self.axesOrientation[2] == 2:  # Sagittal
                    title = "Sagittal"
                    if self.axesOrientation[0] == 0 and self.axesOrientation[1] == 1:  # OK
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        xLabel = "(-Y) A | PHASE | P (+Y)"
                        yLabel = "(-X) I | READOUT | S (+X)"
                    else:
                        image = np.transpose(image, (0, 2, 1))
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        xLabel = "(-Y) A | READOUT | P (+Y)"
                        yLabel = "(-X) I | PHASE | S (+X)"
                elif self.axesOrientation[2] == 1:  # Coronal
                    title = "Coronal"
                    if self.axesOrientation[0] == 0 and self.axesOrientation[1] == 2:  # OK
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        image = np.flip(image, axis=0)
                        xLabel = "(+Z) R | PHASE | L (-Z)"
                        yLabel = "(-X) I | READOUT | S (+X)"
                    else:
                        image = np.transpose(image, (0, 2, 1))
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        image = np.flip(image, axis=0)
                        xLabel = "(+Z) R | READOUT | L (-Z)"
                        yLabel = "(-X) I | PHASE | S (+X)"
                elif self.axesOrientation[2] == 0:  # Transversal
                    title = "Transversal"
                    if self.axesOrientation[0] == 1 and self.axesOrientation[1] == 2:
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        xLabel = "(+Z) R | PHASE | L (-Z)"
                        yLabel = "(+Y) P | READOUT | A (-Y)"
                    else:  # OK
                        image = np.transpose(image, (0, 2, 1))
                        image = np.flip(image, axis=2)
                        image = np.flip(image, axis=1)
                        xLabel = "(+Z) R | READOUT | L (-Z)"
                        yLabel = "(+Y) P | PHASE | A (-Y)"
            else:
                xLabel = "%s axis" % axesStr[1]
                yLabel = "%s axis" % axesStr[0]
                title = "Image"

            result1 = {}
            result1['widget'] = 'image'
            result1['data'] = image
            result1['xLabel'] = xLabel
            result1['yLabel'] = yLabel
            result1['title'] = title
            result1['row'] = 0
            result1['col'] = 0

            result2 = {}
            result2['widget'] = 'image'
            if self.sl_fraction == 1:
                result2['data'] = np.log10(np.abs(self.mapVals['kSpace3D']))
            else:
                result2['data'] = np.abs(self.mapVals['kSpace3D'])
            result2['xLabel'] = "k%s" % axes_str[1]
            result2['yLabel'] = "k%s" % axes_str[0]
            result2['title'] = "k-Space"
            result2['row'] = 0
            result2['col'] = 1

            # Reset rotation angle and dfov to zero
            self.mapVals['angle'] = 0.0
            self.mapVals['dfov'] = [0.0, 0.0, 0.0]
            hw.dfov = [0.0, 0.0, 0.0]

            # DICOM TAGS
            # Image
            imageDICOM = np.transpose(image, (0, 2, 1))
            # If it is a 3d image
            if len(imageDICOM.shape) > 2:
                # Obtener dimensiones
                slices, rows, columns = imageDICOM.shape
                self.meta_data["Columns"] = columns
                self.meta_data["Rows"] = rows
                self.meta_data["NumberOfSlices"] = slices
                self.meta_data["NumberOfFrames"] = slices
            # if it is a 2d image
            else:
                # Obtener dimensiones
                rows, columns = imageDICOM.shape
                self.meta_data["Columns"] = columns
                self.meta_data["Rows"] = rows
                self.meta_data["NumberOfSlices"] = 1
                self.meta_data["NumberOfFrames"] = 1
            imgAbs = np.abs(imageDICOM)
            imgFullAbs = np.abs(imageDICOM) * (2 ** 15 - 1) / np.amax(np.abs(imageDICOM))
            x2 = np.amax(np.abs(imageDICOM))
            imgFullInt = np.int16(np.abs(imgFullAbs))
            imgFullInt = np.reshape(imgFullInt, (slices, rows, columns))
            arr = np.zeros((slices, rows, columns), dtype=np.int16)
            arr = imgFullInt
            self.meta_data["PixelData"] = arr.tobytes()
            self.meta_data["WindowWidth"] = 26373
            self.meta_data["WindowCenter"] = 13194
            # Sequence parameters
            self.meta_data["RepetitionTime"] = self.mapVals['repetition_time']
            self.meta_data["EchoTime"] = self.mapVals['echo_time']

            # Add results into the output attribute (result1 must be the image to save in dicom)
            self.output = [result1, result2]

        # Save results
        self.saveRawData()
        self.save_ismrmrd()

        if self.mode == 'Standalone':
            self.plotResults()
            
        return self.output
        
        
        # Implement data analysis logic here