# Get started with MaRGE and produce the first scans

To produce the first scans using MaRGE, one has to follow these steps.

### 1. Start MaRGE software  
#### 1.1 Open terminal and navigate into `~/home`
#### 1.2 Run the shell script to open MaRGE
```
./start_MaRGE.sh
```


### 2. Fill in data from one's phantom  
One can also leave this form without entries.


### 3. Start the main window  
Press the house symbol.  
<img src="house_start.png" alt="start" style="width: 40%;">


### 4. Connect and Initialise RedPitaya  

#### 4.1 MaRCoS init  
First, press "marcos init."  
<img src="marcos_init.png" alt="marcos_init" style="width: 100%;">  
A terminal window with the message "Copying bitstream..." should pop up and close again shortly after.  
<img src="copying_bitstream.png" alt="copying_bitstream" style="width: 50%;">  

#### 4.2 MaRCoS server  
Then, press "MaRCoS server."  
<img src="marcos_server.png" alt="marcos_server" style="width: 100%;">  

Again, a terminal window will pop up and close again.   
<img src="server_connected.png" alt="server_connecred" style="width: 50%;">  

On the left side, in the console section, one will see a message like `READY: Server connected!`.

#### 4.3 Init power modules  
Lastly, press "Init power modules."  
This will enable the GPA.  
<img src="init_power_modules.png" alt="init_power_modules" style="width: 100%;">  
A message `READY: GPA init done!` will appeear in the console. Also, one will hear a sound from the sound simulator.


### 5. Perform Autocalibration and Localizer Sequences  
First, it is recommended to perform an autocalibration. This will include a Larmor Frequency check, a Rabi Flops Sequence, and noise measurement. One does not need to worry about the error message from the AutoTuning Sequence — this is not required.  

<img src="autocalibration.png" alt="autocalibration" style="width: 100%;">  
In addition, a Localizer Sequence will help to produce scans of higher quality (But it takes some time).  
<img src="localizer.png" alt="localizer" style="width: 100%;">


### 6. Run Sequences
Now, every sequence can be run by selecting from the dropdown menu on the left side and press the `Acquire` button.  

<img src="acquire.png" alt="acquire" style="width: 100%;">

## Additional Information
### Axes orientation:
Inside the sequences, there is always this section `Axes [rd, ph, sl]`.
Here, one can define what type of scans gets created.  
The axes of the MRI are orientated this way:  
<img src="3daxes.png" alt="axes" style="width: 50%;">  
This means, one has to select certain axes as slicing axes (put in the last position inside the brackets -> "sl") to get these type of scans:  

| Scan Type   | Slicing Axis   | variable   |
|------------|------------|------------|
| Coronal  | X  | 2  |
| Transversal  | Y  | 1  |
| Sagittal  | Z  | 0  |

For example, to produce a transversal scan, the Axes input could look like this: `[2, 0, 1]`

### Loading parameters
One can always load parameters from previous scans. Therefore one simply has to click on `Sequences` in the menu bar and select `Load parameters`. 
<img src="sequences.png" alt="sequences_toolbar" style="width: 100%;">


This will open an explorer window where one can navigate to the .csv files of previous or predefined sequences.
<img src="explorer_window.png" alt="explorer_window" style="width: 50%;">

For example, in `~/MaRGE_v2/protocols/Localizers/`one can find different Localizer sequences for different vegetables and the TU Logo.


## Troubleshooting Common Issues  

### Software does not respond
If during a sequence, the window `main.py is not responding` pops up, this is not a problem. During some sequences the threading is too slow and then the GUI is not responsive, which results in this error message. However, as soon as the sequence is finished this window should close and the the GUI will be responsive again.

### No gradient output
If no gradients can be heard (even tough there shoudl be), try pressing "Init power modules" again. Sometimes the initiation does not work right at the first try, so doing this 2-3 times will solve this problem.


### No Larmor frequency
The Larmor frequency should be at around 16.55-16.65 MHz depending on the temperature in the room.  
If no Larmor frequency can be found, try starting at one of these frequencies and run the sequencies iteratively, by clicking the button right next to the `Acquire` button (The double arrow symbol) before clicking `Acquire`.  
<img src="iterative.png" alt="iterative" style="width: 100%;">  

This will run the sequence as long as one stops it and therefore may find the Larmor frequency faster.   
One can also adjust the parameters and check with a higher bandwith for example. 

In addition, check if by accident the shimming vector has changed. It should be by default at `[10.0, -10.0, 10.0]`.  
The shimming sequence should NOT be run, as this will just set the shimming values to the boundaries of the range.

