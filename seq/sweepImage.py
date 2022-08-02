"""
Created on Thu June 2 2022
@author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
@email: josalggui@i3m.upv.es
@Summary: This class is able to sweep any parameter from any sequence
"""

import numpy as np
import seq.mriBlankSeq as blankSeq
import pyqtgraph as pg              # To plot nice 3d images
from plotview.spectrumplot import SpectrumPlot

class SweepImage(blankSeq.MRIBLANKSEQ):
    def __init__(self):
        super(SweepImage, self).__init__()
        # Input the parameters
        self.addParameter(key='seqName', string='SWEEPinfo', val='SWEEP')
        self.addParameter(key='seqNameSweep', string='Sequence', val='FID', field='OTH')
        self.addParameter(key='parameter0', string='Parameter 0 X-axis', val='rfExTime', field='OTH')
        self.addParameter(key='start0', string='Start point 0', val=0.01, field='OTH')
        self.addParameter(key='end0', string='End point 0', val=50.0, field='OTH')
        self.addParameter(key='nSteps0', string='Number of steps 0', val=2, field='OTH')
        self.addParameter(key='parameter1', string='Parameter 1 Y-axis', val='rfExAmp', field='OTH')
        self.addParameter(key='start1', string='Start point 1', val=0.0, field='OTH')
        self.addParameter(key='end1', string='End point 1', val=0.3, field='OTH')
        self.addParameter(key='nSteps1', string='Number of steps 1', val=2, field='OTH')

    def sequenceInfo(self):
        print(" ")
        print("Genera sweep sequence")
        print("Author: Dr. J.M. Algarín")
        print("Contact: josalggui@i3m.upv.es")
        print("mriLab @ i3M, CSIC, Spain")

    def sequenceTime(self):
        return(0)  # minutes, scanTime

    def sequenceRun(self, plotSeq=0):
        # Inputs
        seqName = self.mapVals['seqNameSweep']
        parameters = [self.mapVals['parameter0'], self.mapVals['parameter1']]
        start = [self.mapVals['start0'], self.mapVals['start1']]
        end = [self.mapVals['end0'], self.mapVals['end1']]
        nSteps = [self.mapVals['nSteps0'], self.mapVals['nSteps1']]

        # Sweep
        sampled = []
        parVector0 = np.linspace(start[0], end[0], nSteps[0]) # Create vector with parameters to sweep
        parVector1 = np.linspace(start[1], end[1], nSteps[1])
        seq = self.sequenceList[seqName] # Select the sequence that we want to sweep with modified parameters
        parMatrix = np.zeros((nSteps[0]*nSteps[1], 2))
        n = 0
        for step0 in range(nSteps[0]):
            for step1 in range(nSteps[1]):
                parMatrix[n, 0] = parVector0[step0]
                parMatrix[n, 1] = parVector1[step1]
                seq.mapVals[parameters[0]] = parVector0[step0]
                seq.mapVals[parameters[1]] = parVector1[step1]
                seq.sequenceRun(0)
                seq.sequenceAnalysis()
                if 'sampledCartesian' in seq.mapVals:
                    sampled.append(seq.mapVals['sampledCartesian']) # sampledCartesian is four column kx, ky, kz and S(kx, ky, kz)
                elif 'sampledPoint' in seq.mapVals:
                    sampled.append(seq.mapVals['sampledPoint'])
                else:
                    print('No signal to plot')
                    return 0
                n += 1

        self.seq = seq
        self.sampled = sampled
        return 0

    def sequenceAnalysis(self, obj=''):
        nPoints = np.array(self.seq.mapVals['nPoints'])
        nSteps = [self.mapVals['nSteps0'], self.mapVals['nSteps1']]
        start = [self.mapVals['start0'], self.mapVals['start1']]
        end = [self.mapVals['end0'], self.mapVals['end1']]
        parVector0 = np.linspace(start[0], end[0], nSteps[0])  # Create vector with parameters to sweep

        self.saveRawData()

        if 'sampledCartesian' in self.seq.mapVals:    # In case of images
            # Initialize data and image variables as zeros
            dataSteps = np.zeros((nSteps[0] * nSteps[1], nPoints[1], nPoints[0]), dtype=complex)
            imageSteps = dataSteps

            # Generate k-space maps and images
            for step in range(nSteps[0]*nSteps[1]):
                data = self.sampled[step][:, 3]
                data = np.reshape(data, (nPoints[2], nPoints[1], nPoints[0]))
                image = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(data)))
                dataSteps[step, :, :] = data[int(nPoints[2]/2), :, :]
                imageSteps[step, :, :] = image[int(nPoints[2]/2), :, :]

            # Plot image
            image = pg.image(np.abs(imageSteps))

            # Plot k-space
            kSpace = pg.image(np.log10(np.abs(dataSteps)))

            return([image, kSpace])

        elif 'sampledPoint' in self.seq.mapVals:  # In case of points (calibration sequences)
            image = np.zeros((nSteps[0], nSteps[1]), dtype=complex)
            n = 0
            for step0 in range(nSteps[0]):
                for step1 in range(nSteps[1]):
                    image[step0, step1] = self.sampled[n]
                    n += 1

            # Plot image
            if nSteps[1]>1:
                map = pg.image(np.abs(image))
            else:
                image = np.reshape(image, -1)
                map = SpectrumPlot(parVector0, [np.abs(image)], [''],
                                   self.seq.mapNmspc[self.mapVals['parameter0']], 'Output amplitude', '%s sweep' % self.mapVals['seqNameSweep'])
            return([map])

# defaultSweep = {
#     'SWEEP': SweepImage(),
# }

