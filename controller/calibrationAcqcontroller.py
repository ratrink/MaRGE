"""
Calibration Acquisition Controller

@author:    Yolanda Vives
@author:    J.M. Algarín, josalggui@i3m.upv.es
@version:   2.0 (Beta)
"""

from PyQt5.QtWidgets import QTextEdit, QCheckBox, QHBoxLayout, QVBoxLayout
from plotview.spectrumplot import SpectrumPlot
from seq.sequencesCalibration import defaultCalibFunctions
from PyQt5.QtCore import QObject,  pyqtSlot
from manager.datamanager import DataManager
import numpy as np

class CalibrationAcqController(QObject):
    def __init__(self, parent=None, calibfunctionslist=None):
        super(CalibrationAcqController, self).__init__(parent)

        self.parent = parent
        self.calibfunctionslist = calibfunctionslist
        self.acquisitionData = None
        
        self.layout = QVBoxLayout()

        # self.b1 = QCheckBox("Plot Shim x")
        # self.b1.setGeometry(200, 150, 100, 30)   #            setting geometry of check box
        # self.b1.setStyleSheet("QCheckBox::indicator"
        #                        "{"
        #                        "background-color : white;"
        #                        "selection-color: black;"
        #                        "}")     #    adding background color to indicator
        # self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        # self.layout.addWidget(self.b1)
        #
        # self.b2 = QCheckBox("Plot Shim y")
        # self.b2.setGeometry(200, 150, 100, 30)   #            setting geometry of check box
        # self.b2.setStyleSheet("QCheckBox::indicator"
        #                        "{"
        #                        "background-color : white;"
        #                        "selection-color: black;"
        #                        "}")     #    adding background color to indicator
        # self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        # self.layout.addWidget(self.b2)
        #
        # self.b3 = QCheckBox("Plot Shim z")
        # self.b3.setGeometry(200, 150, 100, 30)   #            setting geometry of check box
        # self.b3.setStyleSheet("QCheckBox::indicator"
        #                        "{"
        #                        "background-color : white;"
        #                        "selection-color: black;"
        #                        "}")     #    adding background color to indicator
        # self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        # self.layout.addWidget(self.b3)

    @pyqtSlot(bool)
    def startAcquisition(self):
        print('Start sequence')

        self.parent.clearPlotviewLayout()

        self.calibfunction = defaultCalibFunctions[self.calibfunctionslist.getCurrentCalibfunction()]
        self.funName = self.calibfunction.mapVals['seqName']

        # Create and execute selected sequence
        defaultCalibFunctions[self.funName].sequenceRun(0)  # Run sequence

        # Do sequence analysis and get plots
        out = defaultCalibFunctions[self.funName].sequenceAnalysis()   # Plot results

        # Add plots to layout
        for item in out:
            self.parent.plotview_layout.addWidget(item)

        print('End sequence')

    def startSequencePlot(self):
        """
        @author: J.M. Algarín, MRILab, i3M, CSIC, Valencia
        @email: josalggui@i3m.upv.es
        @Summary: rare sequence class
        """
        # Delete previous plots
        # if hasattr(self.parent, 'clearPlotviewLayout'):
        #     self.parent.clearPlotviewLayout()
        # self.layout.setParent(None)
        self.parent.clearPlotviewLayout()

        self.calibfunction = defaultCalibFunctions[self.calibfunctionslist.getCurrentCalibfunction()]
        self.funName = self.calibfunction.mapVals['seqName']

        # Create selected sequence
        print('Plot sequence')
        defaultCalibFunctions[self.funName].sequenceRun(1)  # Run sequence

        # Get sequence instructions plot
        out = defaultCalibFunctions[self.funName].sequencePlot()  # Plot results

        # Add plots to layout
        for item in out:
            self.parent.plotview_layout.addWidget(item)