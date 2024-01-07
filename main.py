"""
main.py - Command-line Interface for System Monitoring and Machine Learning

This script serves as the main entry point for executing different functionalities based on command-line arguments.
It provides options for live monitoring, machine learning training (supervised and unsupervised), and displaying help
information.

Usage:
- To start live monitoring, use the '-m' or '--monitor' option.
- For machine learning training, choose between supervised and unsupervised options using '-s' or '--supervised' and '-u'
  or '--unsupervised' respectively.
- The training process can be customized by specifying the number of observations with the '-n' or '--counter' option.
- The default option '-a' or '--all' trains all available functionalities with a default count of observations (500).

For additional information, use the '-h' or '--help' option to display the usage instructions.
"""
import getopt
import sys

import injector
from liveMonitor import liveMonitor
from monitor import monitor
from supervisedML import training as sup_training
from unsupervisedML import training as unsup_training


def usage_instruction(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(content)
        sys.exit(0)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    fileInjection = "injection_timestamps.csv"
    fileMonitor = "monitorResult.csv"
    fileAnomalies = "anomaly_detector/anomaly_detection_log.txt"
    fileInstruction = "instruction.txt"
    try:
        if len(sys.argv) < 2:
            print("Invalid number of parameters.")
        else:
            c_obs = 500
            if len(sys.argv) == 2 and sys.argv[1].lower() in ("-m", "--monitor"):
                print("monitoring live")
                liveMonitor(fileAnomalies)
            elif len(sys.argv) == 2 and sys.argv[1].lower() in ("-h", "--help"):
                usage_instruction(fileInstruction)
            elif len(sys.argv) == 3 and sys.argv[1].lower() in ("-ml", "--machinelearner") and sys.argv[2].lower() in (
                    "-s", "--supervised"):
                print("Machine learner supervised")
                sup_training()
            elif len(sys.argv) == 3 and sys.argv[1].lower() in ("-ml", "--machinelearner") and sys.argv[2].lower() in (
                    "-u", "--unsupervised"):
                print("Machine learner unsupervised")
                unsup_training()
            elif len(sys.argv) == 3 and sys.argv[1].lower() in ("-t", "--training") and sys.argv[2].lower() in (
                    "-a", "--all"):
                print("training all with c_obs default")
                monitor(c_obs, fileMonitor)
                injector.injector(c_obs, fileInjection)
            elif len(sys.argv) == 5 and sys.argv[1].lower() in ("-t", "--training") and sys.argv[2].lower() in (
                    "-n", "--counter") and sys.argv[3].isnumeric() and sys.argv[4] in ("-a", "--all"):
                c_obs = int(sys.argv[3])
                print(f"training all with {c_obs}")
                monitor(c_obs, fileMonitor)
                injector.injector(c_obs, fileInjection)
            else:
                print("Error: invalid arguments.")
                exit(1)
    except getopt.error as err:
        print(str(err))
