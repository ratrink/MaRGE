Changes made during the process of adaption

### controller/controller_history_list.py:
353-:   sequence.mapVals['shimming'] = defaultsequences['Shimming'].mapVals['shimming']
353+:   sequence.mapVals['shimming'] = [0.0, 0.0, 0.0] # defaultsequences['Shimming'].mapVals['shimming']

###  controller/controller_toolbar_sequences.py
95-:    'Shimming',
95+:    # 'Shimming',

108-:   rf_amp = np.pi/(hw.b1Efficiency*hw.reference_time)
108+:   rf_amp = 0.3 # np.pi/(hw.b1Efficiency*hw.reference_time)


### seq/mse_pp_jma.py (as well as all other seq. files)
612-:   title = "Sagittal"     
612+:   title = "Coronal" 

632-:   title = "Coronal"
632+:   title = "Transversal"

656-:   title = "Transversal"
656+:   title = "Sagittal"

### seq/sequences.py
27-:    import seq.sweepImage as sweep
27+:    # import seq.sweepImage as sweep

66-:    'SWEEP': sweep.SweepImage(),
66+:    # 'SWEEP': sweep.SweepImage(),


All absolute paths referencing to MaRGE -> changed into MaRGE_v2 (controller/controller_toolbar_marcos.py, startRP.sh)