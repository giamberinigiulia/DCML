"""
monitor.py - System Metrics Monitoring Script

This script focuses on monitoring system metrics, particularly CPU, Disk, and Memory.

The 'monitor_all' function collects data from these metrics and compiles them into a structured observation dictionary.

The 'usage_cpu_disk_memory' function initiates continuous monitoring, generating observations at regular intervals. It
creates a CSV file named 'monitorResult.csv' in the 'csvFolder' directory, capturing a specified count of observations.
The progress of data collection is displayed using a progress bar.

The 'monitor' function serves as an entry point, starting the monitoring process in a separate process.
"""
import os
import psutil
import time
from csvGenerator import printCsv, flatten
from multiprocessing import Process
from injector import current_ms
from labeling import labeling
from util import getDestinationFolder, print_progress_bar


def monitor_all():
    cpu_count = psutil.cpu_count(logical=False)
    cpu_times = psutil.cpu_times_percent(interval=1, percpu=False)._asdict()  # CPU monitoring
    load_avg = psutil.getloadavg()

    disk_usage = psutil.disk_usage('/')._asdict()  # Disk monitoring
    disk_io_counters = psutil.disk_io_counters()._asdict()

    memory_usage = psutil.swap_memory()._asdict()  # Memory monitoring

    disk_usage = {f'{key}_disk': value for key, value in disk_usage.items()}  # changing field with the same name as
    # others
    disk_io_counters = {f'{key}_disk_io': value for key, value in disk_io_counters.items()}  # changing field with the
    # same name as others

    observations = {  # creation of the record observed
        'timestamp': current_ms(),
        'cpu_count': cpu_count,
        **cpu_times,
        **flatten(load_avg, 'load_avg'),
        **flatten(memory_usage, 'memory'),
        **flatten(disk_usage, 'disk'),
        **flatten(disk_io_counters, 'disk_io')
    }

    return observations


def usage_cpu_disk_memory(count_of_observation, out_filename):
    destinationFolder = getDestinationFolder()
    if not os.path.exists(destinationFolder):
        os.makedirs(destinationFolder)
    i = 0
    columns = None
    while i < count_of_observation:  # inspect the system for count_of_observation times
        current_time = current_ms()
        observations = monitor_all()
        if columns is None:
            columns = list(observations.keys())
        printCsv(observations, out_filename)
        exec_time = (current_ms() - current_time) * 10 ** -9
        print_progress_bar(i, count_of_observation, prefix='Progress:', suffix='Complete', length=50)
        i += 1
        time.sleep(1 - exec_time * 1e-4)
    print_progress_bar(i, count_of_observation, prefix='Progress:', suffix='Complete', length=50)
    labeling()  # labeling the dataset


def monitor(c_obs, monitorFile):
    print('Starting monitoring the disk, the memory, the CPU and the network...')
    p = Process(target=usage_cpu_disk_memory, args=(c_obs, monitorFile))
    p.start()
