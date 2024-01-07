"""
stress_cpu.py
This script is designed to stress the CPU by performing intense mathematical calculations in an infinite loop.
It utilizes the multiprocessing module to create a pool of processes, each running the stress_cpu function independently.
The stress_cpu function involves continuously cubing a given number x.
The main part of the script initiates a pool of four processes, maps the stress_cpu function to each process, sleeps
for 2 seconds, and then terminates the pool.
"""
import time
from multiprocessing import Pool


def stress_cpu(_, x: int = 1234):
    while True:
        x = x * x * x


if __name__ == "__main__":  # used for real-time monitoring
    try:
        with Pool(4) as pool:
            pool.map_async(stress_cpu, [i for i in range(4)])
            time.sleep(2)
            pool.terminate()
    except Exception as e:
        print(f"Error: {e}")
