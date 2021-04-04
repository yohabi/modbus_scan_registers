# pip install pyserial
import serial
import time

modbus_slave_address = 1
modbus_function = 3
modbus_memory_address = 0
modbus_memory_range = 8
modbus_memory_count = 1
port_number = 'COM3'
port_speed = 1200

def modbus_crc16(msg):
    crc = 0xffff
    for i in msg:
        crc ^= i
        for j in range(0, 8):
            if crc&1 == 1:
                crc >>= 1
                crc ^= 0xa001
            else:
                crc >>= 1
    return crc

port = serial.Serial(
    port = port_number,
    baudrate = port_speed,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.2
)
port.reset_input_buffer()

for step in range(modbus_memory_address, modbus_memory_address + modbus_memory_range):
    packet = (
        (modbus_slave_address).to_bytes(1, byteorder='big') +
        (modbus_function).to_bytes(1, byteorder='big') +
        (step).to_bytes(2, byteorder='big') +
        (modbus_memory_count).to_bytes(2, byteorder='big')
    )
    packet += (modbus_crc16(packet)).to_bytes(2, byteorder='little')

    port.write(packet)
    port.flush()
    time.sleep(0.2)
    answer = ''
    answer = port.read(100)
    if answer != '':
        print('[T]', packet.hex(), 'addr', (step).to_bytes(2, byteorder='big').hex(), '[R]', answer.hex())
    else:
        print('[T]', packet.hex(), 'addr', (step).to_bytes(2, byteorder='big').hex(), 'no answer')

port.close()
