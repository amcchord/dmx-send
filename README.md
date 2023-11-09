# dmx-send
This is a simple python script that will send DMX over ArtNet as a CLI

This script runs in Python 3

# Command line options
  * -ip 192.168.10.10 #Set the ip address of the artnet device you want to recieve the packets
  * -u 0 #set the DMX univers
  * -z # Send a packet with all 0's (not required or event suggested to be used)
  * -c 1,255 #Channel,Value set a DMX channel you can set many of these.

# Example

```# python3 dmx-send.py -ip 192.168.100.29 -u 0 -c 1,255 -c 2,64 -c 3,128 -c 4,255```
