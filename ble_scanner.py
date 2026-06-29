import asyncio
from bleak import BleakScanner, BleakClient

async def main():
    print("Scanning for BLE devices...\n")
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("No devices found.")
        return

    for device in devices:
        print(f"Device: {device.name or 'Unknown'}  |  Address: {device.address}")

        try:
            async with BleakClient(device.address, timeout=5.0) as client:
                for service in client.services:
                    print(f"  Service UUID: {service.uuid}")
                    for char in service.characteristics:
                        print(f"    Characteristic: {char.uuid}  |  properties: {char.properties}")
        except Exception as e:
            print(f"  Could not connect: {e}")

        print()

asyncio.run(main())
