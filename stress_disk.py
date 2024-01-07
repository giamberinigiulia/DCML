"""
stress_disk.py
This script simulates disk stress by continuously writing and reading blocks of data to and from temporary files.
It utilizes the multiprocessing module to create a pool of processes, each running the stress_disk function independently.
The stress_disk function creates a temporary file, writes and reads blocks of data in a loop, and then closes and
deletes the file. This process is repeated indefinitely. The script is designed for testing how a system handles
sustained disk activity, helping identify potential performance issues or limitations related to disk I/O.
"""

import tempfile
import time
from multiprocessing import Pool


def stress_disk(_):
    block_to_write = 'x' * 1048576
    while True:
        filehandle = tempfile.TemporaryFile(dir='./')
        for _ in range(512):
            filehandle.write(block_to_write.encode('utf-8'))
        filehandle.seek(0)
        for _ in range(512):
            content = filehandle.read(1048576)
        filehandle.close()
        del content
        del filehandle


if __name__ == "__main__":  # used for real-time monitoring
    try:
        with Pool(12) as pool:
            pool.map_async(stress_disk, [i for i in range(12)])
            time.sleep(2)
            pool.terminate()
    except Exception as e:
        print(f"Error: {e}")
