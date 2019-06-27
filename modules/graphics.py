import matplotlib, requests
matplotlib.use('Agg') # Fixes a runtime error (related to tkinter and it's execution not being in the main thread)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib import style
from psutil import virtual_memory
import math
from collections import deque
style.use('fivethirtyeight')

def cpuUsageGraph(name, data, max):
    times = []
    cpu_usages = []
    date = None
    cpu_usages_median = 0
    for row in data:
        date = datetime.fromtimestamp(row[6])
        times.append(date)
        cpu_usages.append(math.floor(row[0]))
    for i in range(0, len(cpu_usages)):
        cpu_usages_median += cpu_usages[i]
    cpu_usages_median = round(cpu_usages_median / len(cpu_usages), 2)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(times, cpu_usages, label="Autopsy", linewidth=0.7)
    #plt.xticks(times, rotation=25)
    #plt.locator_params(axis='x', nbins=xNumValues)
    plt.axhline(max, label="Maximum threshold ({}%)".format(max), linestyle='--', color='r', linewidth=1)
    plt.axhline(cpu_usages_median, label="Median CPU Usage ({}%)".format(cpu_usages_median), linestyle='--', color='b', linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.ylim(0, 100)
    plt.title("CPU Usage (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()

def cpuCoresGraph(name, data):
    times = []
    cpu_cores = []
    date = None
    for row in data:
        date = datetime.fromtimestamp(row[6])
        times.append(date)
        cpu_cores.append(math.floor(row[1]))
    #plt.xticks(times, rotation=25)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(times, cpu_cores, label="Autopsy", linewidth=0.7)
    #plt.locator_params(axis='x', nbins=xNumValues)
    plt.xlabel("Time")
    plt.ylabel("CPU cores")
    plt.yticks(list(range(0, 21, 4)))
    plt.title("CPU affinity number (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()

def cpuThreadsGraph(name, data):
    times = []
    cpu_threads = []
    date = None
    for row in data:
        date = datetime.fromtimestamp(row[6])
        times.append(date)
        cpu_threads.append(math.floor(row[2]))
    #plt.xticks(times, rotation=25)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(times, cpu_threads, label="Autopsy", linewidth=0.7)
    #plt.locator_params(axis='x', nbins=xNumValues)
    plt.xlabel("Time")
    plt.ylabel("CPU threads")
    #plt.ylim(0, 100)
    plt.title("CPU threads (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()

def cpuTimeGraph(name, data):
    times = []
    cpu_times = []
    cpu_times_rate = []
    date = None
    for row in data:
        date = datetime.fromtimestamp(row[6])
        times.append(date)
        cpu_times.append(math.floor(row[3]))

    for i in range(0, len(cpu_times) - 1):
        cpu_times_rate.append(cpu_times[i+1] - cpu_times[i])

    last_cpu_time = cpu_times[(len(cpu_times) - 1)]

    x = deque(times)
    x.popleft()
    x = list(x)

    #plt.xticks(times, rotation=25)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(x, cpu_times_rate, label="Autopsy", linewidth=0.7)
    #plt.locator_params(axis='x', nbins=xNumValues)
    plt.xlabel("Time")
    plt.ylabel("CPU time (CPU seconds/second)")
    plt.ylim(0, 5)
    plt.title("CPU time (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()

    return last_cpu_time

def ioGraph(name, data):
    times = []
    io_read_bytes = []
    io_read_MBs = []
    io_write_bytes = []
    io_write_MBs = []
    io_write_MBs_median = 0
    io_read_MBs_median = 0
    date = None
    for row in data:
        date = datetime.fromtimestamp(row[6])
        times.append(date)
        io_read_bytes.append(int(row[2]))
        io_write_bytes.append(int(row[3]))

    for i in range(0, len(io_write_bytes) - 1):
        io_write_MBs.append(abs(math.floor((io_write_bytes[i+1] - io_write_bytes[i]) * 0.000000953674)))

    for i in range(0, len(io_read_bytes) - 1):
        io_read_MBs.append(abs(math.floor((io_read_bytes[i+1] - io_read_bytes[i]) * 0.000000953674)))

    for i in range(0, len(io_write_MBs)):
        io_write_MBs_median += io_write_MBs[i]

    for i in range(0, len(io_read_MBs)):
        io_read_MBs_median += io_read_MBs[i]

    io_read_MBs_median = round(io_read_MBs_median / len(io_read_MBs), 2)
    io_write_MBs_median = round(io_write_MBs_median / len(io_write_MBs), 2)
    x = deque(times)
    x.popleft()
    x = list(x)

    #plt.xticks(rotation=25)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    #plt.plot(times, io_read_count, label="Autopsy read count")
    #plt.plot(times, io_write_count, label="Autopsy write count")
    plt.plot(x, io_read_MBs, label="Autopsy read MB/s", linewidth=0.7)
    plt.plot(x, io_write_MBs, label="Autopsy write MB/s", linewidth=0.7)
    plt.axhline(io_write_MBs_median, label="Median Write MB/s ({}MB/s)".format(io_write_MBs_median), linestyle='--', color='b', linewidth=1)
    plt.axhline(io_read_MBs_median, label="Median Read MB/s ({}MB/s)".format(io_read_MBs_median), linestyle='--', color='y', linewidth=1)
    plt.ylim(bottom=0)
    plt.xlabel("Time")
    plt.ylabel("MB/s")
    plt.title("IO read/write MBytes (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()


def memoryUsageGraph(name, data, max_solr, max):
    #Needs pagefaults
    totalMemory = int(virtual_memory()[0]) / 1000000
    times = []
    mem_usages = []
    solr_mem = []
    date = None
    memory_usage_median = 0
    system_mem_usages = []

    for row in data:
        date = datetime.fromtimestamp(row[4])
        times.append(date)
        mem_usages.append(int(row[0]) / 1000000)
        solr_mem.append(row[5])
        system_mem_usages.append(int(row["system_memory_usage"]) / 1000000)
    for i in range(0, len(mem_usages)):
        memory_usage_median += mem_usages[i]

    memory_usage_median = round(memory_usage_median / len(mem_usages), 2)
    #plt.xticks(times, rotation=25)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(times, mem_usages, label="Autopsy", linewidth=0.7)
    plt.plot(times, solr_mem, label="Solr", linewidth=0.7)
    plt.plot(times, system_mem_usages, label="System", linewidth=0.7)
    #plt.locator_params(axis='x', nbins=xNumValues)
    plt.axhline(max, label="Maximum threshold ({}MB)".format(max), linestyle='--', color='r', linewidth=1)
    plt.axhline(memory_usage_median, label="Median Memory Usage ({}MB)".format(memory_usage_median), linestyle='--', color='b', linewidth=1)
    plt.axhline(max_solr, label="Solr Maximum memory({}MB)".format(max_solr), linestyle='--', color='y', linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Memory usage (MB)")
    plt.ylim(0, totalMemory)
    plt.title("Memory usage (" + str(datetime.strftime(date, '%d-%m-%Y')) + ")")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()

def freeDiskSpaceGraph(name, data):
    for key in data:
        values = data[key]
        freeDiskSpace = []
        times = []
        for value in values:
            splitted = str.split(value, ", ")
            freeDiskSpace.append(splitted[0])
            times.append(datetime.fromtimestamp(float(splitted[1])))
        plt.plot(times, freeDiskSpace, label="Disk " + str(key), linewidth=0.7)
    ax = plt.gca()
    xfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xlabel("Time")
    plt.ylabel("Disk Space (GB)")
    plt.title("Free Disk Space (GB)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gcf().autofmt_xdate()
    plt.savefig(name, bbox_inches='tight')
    plt.cla()