"""
stress_memory.py - Memory Stress Simulation Script

This script simulates memory stress by continuously allocating a large amount of memory.
It utilizes the multiprocessing module to create a pool of processes, each running the stress_memory function
independently.
The stress_memory function allocates memory in the form of a list and continues to manipulate the allocated memory,
causing stress on the RAM. This process is repeated indefinitely. The script is designed for testing how a system
handles sustained memory stress, helping identify potential performance issues or limitations related to memory usage.
"""

import time
from multiprocessing import Pool


def stress_memory(_):
    # Allocate a large amount of memory
    memory_stress = []
    while True:
        # Continue to manipulate the allocated memory to stress RAM
        memory_stress.append([1024 for i in range(0, 1234567)])
        time.sleep(0.001)


if __name__ == "__main__":  # used for real-time monitoring
    try:
        with Pool(12) as pool:
            pool.map_async(stress_memory, [i for i in range(12)])
            time.sleep(2)
            pool.terminate()
    except Exception as e:
        print(f"Error: {e}")
