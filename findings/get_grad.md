## How to get a gradient signal with MaRGe


1. start bitstream
```
./copy_bitstream 10.42.0.211 rp-122
```

2. start server
```
ssh root@10.42.0.211
./marcos_server
```

3. go to marcos_client and run the examples.py file
```
python3 examples.py
```

4. now start MaRGe
```
python3 main.py./cop
```


## How to get a gradient signal with MRI4ALL

1. Start VM
```
vagrant up
```

2. login to VM (user = pasword = `vagrant`)

3. enter
```
startx
```

4. execute this in Terminal Emulator
```
source /opt/mri4all/env/bin/activate
cd /opt/mri4all/console
python run_recon.py &
python run_acq.py &
python run_ui.py
```

5. on host pc: Connect to Redpitaya and start marcos server
```
cd marcos_extras
./copy_bitstream 10.42.0.211 rp-122
ssh root@10.42.0.211 "./marcos_server"
```
Now you can choose the wanted gradient and run in by clicking on the checkmark symbol.
