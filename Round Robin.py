from collections import deque

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority

    def __str__(self):
        
        return f"Process {self.pid}: arrival time={self.arrival_time}, burst time={self.burst_time}, remaining time={self.remaining_time}, priority={self.priority}"


def update_queue(queue, new_queue, process):
    if process.priority <= 30:
        new_queue.append(process)
    elif 60 >= process.priority > 30:
        if process.remaining_time == 0:
            queue.append(process)
        else:
            new_queue.appendleft(process)
    else:
        queue.append(process)

def round_robin(processes, quantum):
    high_queue = deque()
    med_queue = deque()
    low_queue = deque()
    current_time = 0
    priority_increment = 1  # Increment value for high and medium priority levels
    #high_decrement = 1  # Decrement value for high priority level
    #low_med_decrement = 1  # Decrement value for low and medium priority levels
    #low_med_increment = 1
    while processes or high_queue or med_queue or low_queue:
        # Add arriving processes to the appropriate queue
        while processes and processes[0].arrival_time <= current_time:
            process = processes.pop(0)
            if 1 < process.priority <= 30:
                high_queue.append(process)
            elif 60 >= process.priority > 30:
                med_queue.append(process)
            elif 90>= process.priority > 60:
                low_queue.append(process)
    
        # Check the high-priority queue first
        if high_queue:
            process = high_queue.popleft()
            if process.priority ==31:
                med_queue.append(process)
                continue
            print(f"Process {process.pid} starts at time {current_time} - Queue: High")
            if process.remaining_time <= quantum:
                current_time += process.remaining_time
                process.remaining_time = 0
                print(f"Process {process.pid} - Priority: {process.priority}")
                print(f"Process {process.pid} finishes at time {current_time } - Queue: High")
            else:
                process.priority += 1
                current_time += quantum
                process.remaining_time -= quantum
                print(f"Process {process.pid} preempted at time {current_time}- Queue: High ")
                print(f"Process {process.pid} - Priority: {process.priority}")
                high_queue.append(process)

            #for process in list(high_queue) + list(med_queue) + list(low_queue):
            #    if process.priority == 1:
            #        process.priority += 1
        # If there are no high-priority processes, check the medium-priority queue
        elif med_queue:
            process = med_queue.popleft()
            if process.priority ==61:
                low_queue.append(process)
                continue
            process.priority = min(process.priority + priority_increment, 90)
            print(f"Process {process.pid} starts at time {current_time}- Queue: med")
            print(f"Process {process.pid} - Priority: {process.priority}")
            if process.remaining_time <= quantum:
                current_time += process.remaining_time
                process.remaining_time = 0
                print(f"Process {process.pid} finishes at time {current_time}- Queue: med")
            else:
                current_time += quantum
                process.remaining_time -= quantum
                print(f"Process {process.pid} preempted at time {current_time}- Queue: med")
                med_queue.append(process)

        # If there are no high- or medium-priority processes, check the low-priority queue
        elif low_queue:
            process = low_queue.popleft()
            process.priority = min(process.priority + priority_increment, 90)
            if process.priority ==90:
                process.priority=1
                high_queue.append(process)  # Move process back to high priority queue
                continue  # Skip the remaining code and move to the next iteration of the while loop
            
            print(f"Process {process.pid} starts at time {current_time}- Queue: low")
            print(f"Process {process.pid} - Priority: {process.priority}")
            if process.remaining_time <= quantum:
                current_time += process.remaining_time
                process.remaining_time = 0
                print(f"Process {process.pid} finishes at time {current_time}- Queue: low")
            else:
                current_time += quantum
                process.remaining_time -= quantum
                print(f"Process {process.pid} preempted at time {current_time}- Queue: low")
                low_queue.append(process)


# Example usage:
processes = [
    Process(1, 0, 6, 10),
    Process(2, 1, 5, 20),
    Process(3, 3, 20, 34),
    Process(4, 4, 10, 40),
    Process(5, 5, 5, 50),
    Process(8, 0, 6, 60),
    Process(9, 1, 5, 70),
    Process(10, 3, 20, 30),
    Process(11, 4, 10, 80),
    Process(12, 5, 5, 88),
    Process(13, 0, 6, 10),
    Process(14, 1, 5, 15),
    Process(15, 3, 20, 24),
    Process(16, 4, 10, 31),
    Process(17, 5, 5, 61)]
print(processes[0].priority)
round_robin(processes, 2)
#1-30 high
#31-60 middle
#61-90 low