#!/usr/bin/env python3
import socket
import struct
import argparse

# Configuration
ARTNET_PORT = 6454
ARTNET_HEADER = b'Art-Net\x00'
OP_OUTPUT = 0x5000
SEQUENCE = 0
PHYSICAL = 0
MAX_CHANNELS = 512  # Maximum number of DMX channels

def send_artnet(ip, universe, channel_data, zero_out):
    """
    Send an ArtNet packet to the specified IP and universe with the given DMX data.
    """
    # Initialize DMX data with zeros if zero_out is True, else with zeros up to the highest channel number
    highest_channel = max(channel_data.keys(), default=0)
    dmx_data = [0] * highest_channel

    # Set specified channel values
    for channel, value in channel_data.items():
        dmx_data[channel - 1] = value  # DMX channels start at 1

    # Convert DMX data to bytes
    dmx_data = bytes(dmx_data)

    # Length of the DMX data (number of channels)
    dmx_data_length = len(dmx_data)

    # Construct the ArtDMX packet with the ArtNet header and the DMX data
    packet = struct.pack('!8sBHHBBH', ARTNET_HEADER, 0x00, OP_OUTPUT, SEQUENCE, PHYSICAL, universe, dmx_data_length) + dmx_data

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the packet to the specified IP address using the ArtNet port
    sock.sendto(packet, (ip, ARTNET_PORT))

    # Close the socket
    sock.close()

    print(f"Sent ArtNet DMX data to {ip} on universe {universe} {'with zeroing out channels' if zero_out else ''}")
    print("ArtNet packet data:", packet.hex())

def parse_channel_args(channel_args):
    """
    Parse the channel arguments into a dictionary mapping channel numbers to values.
    """
    channel_data = {}
    for arg in channel_args:
        try:
            channel, value = map(int, arg.split(','))
            channel += 1
            if channel < 1 or channel > MAX_CHANNELS + 1:
                raise ValueError(f"Channel number must be between 1 and {MAX_CHANNELS}.")
            if value < 0 or value > 255:
                raise ValueError("Channel value must be between 0 and 255.")
            channel_data[channel] = value
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)

    return channel_data

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Send ArtNet DMX data.')
    parser.add_argument('-ip', '--ip-address', required=True, type=str, help='The IP address of the ArtNet device.')
    parser.add_argument('-u', '--universe', required=True, type=int, help='The ArtNet universe (0-65535).')
    parser.add_argument('-c', '--channel', action='append', required=True, help='The DMX channel and value in the format channel-value, e.g., 1-255. Can be repeated.')
    parser.add_argument('-z', '--zero-out', action='store_true', help='Zero out all channels before setting specified values.')

    # Parse command line arguments
    args = parser.parse_args()

    # Parse channel-value pairs
    channel_data = parse_channel_args(args.channel)

    # Send the ArtNet packet
    send_artnet(args.ip_address, args.universe, channel_data, args.zero_out)

if __name__ == '__main__':
    main()
