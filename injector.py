"""
injector.py - Stress Injector for Anomaly Detection Dataset Generation

This script simulates stress on the system by injecting artificial load on CPU, memory, and disk. It creates
synthetic observations and appends them to the 'csvFolder/dataset.csv' file. The script generates random injections
of CPU, memory, and disk stress, records the start and end times, and appends the observations to the dataset.
"""
import os
import sys
import time
import random
from multiprocessing import Pool, cpu_count
from random import shuffle

from csvGenerator import flatten, printCsv
from stress_cpu import stress_cpu
from stress_disk import stress_disk
from stress_memory import stress_memory
from util import current_ms


def injector(c_obs, out_filename):
    if not os.path.exists("csvFolder"):
        os.makedirs("csvFolder")
    if not os.path.exists("csvFolder/" + out_filename):
        with open("csvFolder/" + out_filename, 'w') as file:
            pass
    i = 0
    while not os.path.exists("csvFolder/dataset.csv"):  # while the dataset is not completed
        injections_to_execute = ['cpu', 'memory', 'disk']
        shuffle(injections_to_execute)
        time.sleep(((c_obs // 15) + 1) * random.random())  # initial waiting before starting the injection
        i += 1
        for injection_type in injections_to_execute:
            returnValue = stress(injection_type, i, out_filename)
            while not returnValue:
                time.sleep(0.01)
        if os.path.exists("csvFolder/dataset.csv"):
            sys.exit()


def stress(injection_type, counter, out_filename):
    stressFunction = {
        'cpu': stress_cpu,
        'memory': stress_memory,
        'disk': stress_disk
    }[injection_type]  # the injection is chosen

    start_time = current_ms()
    duration_ms = round(random.uniform(50, 80)) * 100
    number_count = cpu_count()
    if injection_type in ('memory', 'disk'):
        number_count = number_count * 2
    pool = Pool(number_count)
    pool.map_async(stressFunction, [i for i in range(number_count)])  # creating the pool
    time.sleep((duration_ms - (current_ms() - start_time)) / 1000.0)  # waiting until the time of the injection is over
    if pool is not None:
        pool.terminate()
        pool.join()
    end_time = current_ms()
    printCsv(flatten(
        {'counter': counter, 'start_time': start_time, 'end_time': end_time, 'injection_type': injection_type}),
        out_filename)  # print in the csv the start and end time for the injection
    return True
