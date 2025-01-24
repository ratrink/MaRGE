# Get started with MaRGE and produce the first scans

To produce the first pictures using MaRGE, one has to follow these steps.

### 1. Start MaRGE software  
#### 1.1 Navigate into the MaRGE folder
```
cd home/MRI/MaRGE
```

#### 1.2 Activate the Virtual Environment
```
conda activate marge
```

#### 1.2 Start the python script
```
python3 main.py
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
A message `READY: GPA init done!` will appeear in the console.

### 5. Perform Autocalibration and Localizer Sequences  

First, it is recommended to perform an autocalibration. This will include a Lamor Frequency check, a Rabi Flops Sequence, and noise measurement. One does not need to worry about the error message from the AutoTuning Sequence — this is not required.  

<img src="autocalibration.png" alt="autocalibration" style="width: 100%;">  
In addition, a Localizer Sequence will help to produce pictures of higher quality.  
<img src="localizer.png" alt="localizer" style="width: 100%;">





## Troubleshooting Common Issues  
If no gradients can be seen, try pressing "Init power modules" again. Sometimes the initiation does not work right at the first try, so doing this 2-3 times will solve this problem.

