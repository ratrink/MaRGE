#!/bin/sh

../MaRGE_v2/copy_bitstream.sh $1 $2
timeout 2s ssh root@$1 "~/marcos_server &"
