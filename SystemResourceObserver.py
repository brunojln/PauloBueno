import psutil
import time

class SystemResourceObserver:
    def __init__(self):
        self.continue_processing = True

    def run(self):
        while True:
            # Get and display the CPU usage percentage
            cpu_usage = psutil.cpu_percent()
            # print(f"CPU Usage: {cpu_usage}%")

            # Get and display the memory usage percentage
            memory_usage = psutil.virtual_memory().percent
            # print(f"Memory Usage: {memory_usage}%")

            if memory_usage > 70 or cpu_usage > 80:
                print(f"Alert: High memory usage ({memory_usage:.2f}%) and CPU usage ({cpu_usage:.2f}%)")
                self.set_continue(False)  # Interrupt
            else:
                self.set_continue(True)  # Continue

            # Wait for a time interval before checking again
            time.sleep(1)  # Wait for 1 second

    def set_continue(self, usage_bool):
        self.continue_processing = usage_bool

    def get_continue(self):
        return self.continue_processing

    @staticmethod
    def get_continue_ss(model):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        if model == 1:
            return memory_usage <= 65 and cpu_usage <= 75
        else:
            return memory_usage <= 80 and cpu_usage <= 80