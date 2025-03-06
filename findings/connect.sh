#!/bin/bash
IP="10.42.0.249"

cd marcos_extras
./copy_bitstream.sh $IP rp-122

ssh -f root@$IP "./marcos_server"

cd ..
cd marcos_client
python3 examples.py

cd ..
cd MaRGE
python3 main.py

