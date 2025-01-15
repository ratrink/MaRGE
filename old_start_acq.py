def startAcquisition(self, seq_name=None):
        """
        Run the selected sequence and perform data acquisition.

        Args:
            seq_name (str, optional): Name of the sequence to run. If not provided or False, the current sequence in the sequence list is used.

        Returns:
            int: Return 0 if the sequence run fails.

        Summary:
            This method executes the selected sequence and handles the data acquisition process.
            It performs various operations such as loading the sequence name, deleting output if the sequence has changed,
            saving input parameters, updating sequence attributes, creating and executing the sequence, analyzing the
            sequence output, updating parameters, displaying the output label, saving results to history, adding plots to
            the plot view, and optionally iterating the acquisition in a separate thread.
        """
        # Load sequence name
        if seq_name is None or seq_name is False:
            self.seq_name = self.main.sequence_list.getCurrentSequence()
        else:
            self.seq_name = seq_name

        # Delete ouput if sequence is different from previous one
        if hasattr(self, "old_seq_name"):
            if self.seq_name != self.old_seq_name:
                self.new_run = True
                defaultsequences[self.seq_name].deleteOutput()
        self.old_seq_name = copy.copy(self.seq_name)

        if not hasattr(defaultsequences[self.seq_name], 'output'):
            self.new_run = True

        # Save sequence list into the current sequence, just in case you need to do sweep
        defaultsequences[self.seq_name].sequence_list = defaultsequences

        # Add sequence name for metadata
        defaultsequences[self.seq_name].raw_data_name = self.seq_name

        # Save input parameters
        defaultsequences[self.seq_name].saveParams()

        if self.new_run:
            self.new_run = False

            # Update possible rotation, fov and dfov before the sequence is executed in parallel thread
            defaultsequences[self.seq_name].sequenceAtributes()

            # Create and execute selected sequence
            if defaultsequences[self.seq_name].sequenceRun(0, self.main.demo):
                # Delete previous plots
                self.main.figures_layout.clearFiguresLayout()

                # Create label with rawdata name
                self.label = QLabel()
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setStyleSheet("background-color: black;color: white")
                self.main.figures_layout.addWidget(self.label, row=0, col=0, colspan=2)
            else:
                return 0

            # Do sequence analysis and acquire de plots
            self.old_out = defaultsequences[self.seq_name].sequenceAnalysis()

            # Update parameters, just in case something changed
            self.main.sequence_list.updateSequence()

            # Set name to the label
            file_name = defaultsequences[self.seq_name].mapVals['fileName']
            self.label.setText(file_name)

            # Add item to the history list
            self.main.history_list.current_output = str(datetime.now())[11:23] + " | " + file_name.split('.')[0]
            item_name = str(datetime.now())[11:23] + " | " + file_name
            self.main.history_list.addItem(item_name)

            # Clear inputs
            defaultsequences[self.seq_name].resetMapVals()

            # Save results into the history
            self.main.history_list.outputs[self.main.history_list.current_output] = self.old_out
            self.main.history_list.inputs[self.main.history_list.current_output] = \
                [list(defaultsequences[self.seq_name].mapNmspc.values()),
                 list(defaultsequences[self.seq_name].mapVals.values())]

            # Save the rotation and shifts to the history list
            self.main.history_list.rotations[self.main.history_list.current_output] = \
                defaultsequences[self.seq_name].rotations.copy()
            self.main.history_list.shifts[self.main.history_list.current_output] = \
                defaultsequences[self.seq_name].dfovs.copy()
            self.main.history_list.fovs[self.main.history_list.current_output] = \
                defaultsequences[self.seq_name].fovs.copy()

            # Add plots to the plotview_layout
            self.plots = []
            n_columns = 1
            for item in self.old_out:
                if item['col']+1 > n_columns:
                    n_columns = item['col']+1
                if item['widget'] == 'image':
                    image = Spectrum3DPlot(main=self.main,
                                           data=item['data'],
                                           x_label=item['xLabel'],
                                           y_label=item['yLabel'],
                                           title=item['title'])
                    self.main.figures_layout.addWidget(image, row=item['row'] + 1, col=item['col'])
                    defaultsequences[self.seq_name].deleteOutput()
                elif item['widget'] == 'curve':
                    self.plots.append(SpectrumPlot(x_data=item['xData'],
                                                   y_data=item['yData'],
                                                   legend=item['legend'],
                                                   x_label=item['xLabel'],
                                                   y_label=item['yLabel'],
                                                   title=item['title']))
                    self.main.figures_layout.addWidget(self.plots[-1], row=item['row'] + 1, col=item['col'])
            self.main.figures_layout.addWidget(self.label, row=0, col=0, colspan=n_columns)

            # Iterate in parallel thread (only for 1d plots)
            if self.action_iterate.isChecked() and hasattr(defaultsequences[self.seq_name], 'output'):
                thread = threading.Thread(target=self.repeatAcquisition)
                thread.start()

            # Deactivate the iterative buttom if sequence is not iterable (2d and 3d plots)
            if not hasattr(defaultsequences[self.seq_name], 'output') and self.action_iterate.isChecked():
                self.action_iterate.toggle()

        else:
            thread = threading.Thread(target=self.repeatAcquisition)
            thread.start()