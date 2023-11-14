from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox, QWidget


class PreProcessingTabWidget(QWidget):
    """
    PreProcessingTabWidget class for displaying a tab widget for image pre-processing options.

    Inherits from QTabWidget provided by PyQt5 to display a tab widget for image pre-processing options.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the PreProcessingTabWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(PreProcessingTabWidget, self).__init__(*args, **kwargs)

        # The 'main' attribute represents the parent widget, which is used to access the main window or controller.
        self.main = parent

        #***********************
        # Cosbell
        #***********************
        #Checkboxes
        self.readout_checkbox = QCheckBox('Readout')
        self.phase_checkbox = QCheckBox('Phase')
        self.slice_checkbox = QCheckBox('Slice')
        self.cosbell_order_label = QLabel('Order')
        self.cosbell_order_field = QLineEdit()
        self.cosbell_order_field.setText('1')
        self.image_cosbell_button = QPushButton('Cosbell filter')

        # Cosbell layout
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.readout_checkbox)
        self.checkbox_layout.addWidget(self.phase_checkbox)
        self.checkbox_layout.addWidget(self.slice_checkbox)

        # Order layout
        self.cosbell_order_layout = QHBoxLayout()
        self.cosbell_order_layout.addWidget(self.cosbell_order_label)
        self.cosbell_order_layout.addWidget(self.cosbell_order_field)

        self.cosbell_layout = QVBoxLayout()
        self.cosbell_layout.addLayout(self.checkbox_layout)
        self.cosbell_layout.addLayout(self.cosbell_order_layout)
        self.cosbell_layout.addWidget(self.image_cosbell_button)

        self.cosbell_group = QGroupBox("Cosbell")
        self.cosbell_group.setLayout(self.cosbell_layout)

        # ***********************
        # Zero Padding
        # ***********************
        self.zero_padding_order_label = QLabel('Order')
        self.zero_padding_order_field = QLineEdit()
        self.zero_padding_order_field.setPlaceholderText("Readout, Phase, Slice")
        self.zero_padding_order_field.setStatusTip('Must be integer numbers')

        self.zero_padding_order_layout = QHBoxLayout()
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_label)
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_field)

        self.image_padding_button = QPushButton('Zero padding')

        self.zero_padding_layout = QVBoxLayout()
        self.zero_padding_layout.addLayout(self.zero_padding_order_layout)
        self.zero_padding_layout.addWidget(self.image_padding_button)

        self.zero_padding_group = QGroupBox("Zero Padding")
        self.zero_padding_group.setLayout(self.zero_padding_layout)

        # Main layout
        self.preprocessing_layout = QVBoxLayout()
        self.preprocessing_layout.addWidget(self.zero_padding_group)
        self.preprocessing_layout.addWidget(self.cosbell_group)
        self.preprocessing_layout.addStretch()
        self.setLayout(self.preprocessing_layout)
