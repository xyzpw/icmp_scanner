#!/usr/bin/env python3
import icmplib, threading, math

active_addresses = []

def scan(current_num):
    global address_range
    packet = icmplib.ping(f"{address_range}{current_num}", count=1, timeout=timeout)
    status = "\033[31mCLOSED\033[0m"
    if packet.is_alive:
        status = "\033[32mACTIVE\033[0m"
        active_addresses.append(f"{address_range}{current_num}")
    print(f"{address_range}{current_num} {status}")

address_range = input("First 3 octets of IPv4: ")
if address_range[len(address_range)-1] != '.': address_range += '.'
timeout = int(input("Timeout: "))
timeout /= 1000

threads = []
for i in range(256):
    t = threading.Thread(target=scan, args=[i], daemon=True)
    threads.append(t)
for i in range(256):
    threads[i].start()
for i in range(256):
    threads[i].join()

print("\nOpen addresses: \n")

if len(active_addresses) > 6:
    print()
    print(*active_addresses, sep='\n')
    print(f"\n({math.floor( len(active_addresses)/256 * 1000 )/10}%)\n")
if len(active_addresses) <= 6: print(f"\n\n{active_addresses}\n\n({math.floor(len(active_addresses)/256 * 1000)/10}%)\n")
