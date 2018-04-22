from network import LoRa
import socket
import binascii
import struct
import time
import config

#set the region parameters based on your current location.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)


dev_addr = struct.unpack(">l", binascii.unhexlify('26011C25'))[0] #Manually set 4 byte data. *same should be copied at TTN.*
nwk_swkey = binascii.unhexlify('FF1BFCF6E18EF7F62CED2328FC83456A') #Obtained from TTN
app_swkey = binascii.unhexlify('5BBDA28B0FAD5FD6AC02421F66429664') #Obtained from TTN

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a RAW LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket blocking
s.setblocking(False)


#This part to be modified based on preferences.
for i in range (200):
    pkt = b'This is packet number:' + bytes([i])
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)
