import bluetooth

target_name = "HC-06"
target_address = None

nearby_devices = bluetooth.discover_devices()
print nearby_devices

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"

port = 11

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bdaddr, port))

sock.send(1)

sock.close()
