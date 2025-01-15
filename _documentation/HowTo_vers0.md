# Get started with MaRGE and produce the first pictures

To produce the first  pictures using MaRGE, one has to follow these steps.

### 1. start MaRGE software:  
#### 1.1 navigate into MaRGE folder

```
cd home/MRI/MaRGE
```
#### 1.2 activate virtual environment
```
conda activate marge
```
#### 1.3. start main.py file
```
python3 main.py
```
### 2. Fill in data from your phantom
One can also leave this form without entries.

### 3. Start main window
Press onto the house symbol.  
<img src="house_start.png" alt="start" style="width: 40%;">

### 4. Connect and initialise RedPitaya

#### 4.1. MaRCoS init
First, press "marcos init"  
<img src="marcos_init.png" alt="marcos_init" style="width: 100%;">
A terminal window whith the message "Copying bitstream..." should pop up and close again shortly after.

#### 4.2. MaRCoS server
Then, press "MaRCoS server"
<img src="marcos_server.png" alt="marcos_server" style="width: 100%;">

Again, a terminal window will pop up and close again.  
On the left side in the console section one will see a message like `blablabla`.

#### 4.3. Init power modules
Last, press "Init power modules".
This will enable the GPA.
<img src="init_power_modules.png" alt="init_power_modules" style="width: 100%;">


### 5. Do Autocalibration an Localizer Sequences

First, it is recommended to do an autocalibration, this will include a Lamor Frequence check, as well as an Rabi Flops Sequence and a noise measuring. One does not have to worry about the error mesaage from the AutoTuning Sequence - this is not needed.  


<img src="autocalibration.png" alt="autocalibration" style="width: 100%;">
In addition, a Localizer Sequence will also help to get pictures of higher quality.  
<img src="localizer.png" alt="localizer" style="width: 100%;">



## Troubleshooting common issues.
TODO
