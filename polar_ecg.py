import asyncio
import struct
from bleak import BleakScanner, BleakClient

PMD_CONTROL = "fb005c81-02e7-f387-1cad-8acd2d8df0c8"
PMD_DATA    = "fb005c82-02e7-f387-1cad-8acd2d8df0c8"
START_ECG   = bytearray([0x02, 0x00, 0x00, 0x01, 0x82, 0x00, 0x01, 0x01, 0x0E, 0x00])

def handle_ecg(sender, data):
    data = bytearray(data)
    if data[0] != 0x00 or len(data) < 10:
        return
    for i in range(9, len(data) - 2, 3):
        raw = data[i:i+3]
        val = struct.unpack('<i', raw + (b'\xff' if raw[2] & 0x80 else b'\x00'))[0]
        print(f"ECG: {val} µV")

async def main():
    print("Scanning for Polar H10...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, _: d.name and "Polar" in d.name, timeout=10.0
    )
    if not device:
        print("Device not found.")
        return

    print(f"Found: {device.name} ({device.address})")
    async with BleakClient(device) as client:
        await client.write_gatt_char(PMD_CONTROL, START_ECG, response=True)
        await client.start_notify(PMD_DATA, handle_ecg)
        print("Streaming ECG... Ctrl+C to stop.\n")
        await asyncio.sleep(999999)

asyncio.run(main())
