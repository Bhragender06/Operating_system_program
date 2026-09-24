from collections import deque

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]


# ---------------- NON-PREEMPTIVE PRIORITY ----------------

def priority_scheduling(processes):
    current_time = 0
    completed = set()
    result = []

    while len(completed) < len(processes):

        ready = [
            p for p in processes
            if p["arrival"] <= current_time
            and p["pid"] not in completed
        ]

        # CPU is idle
        if not ready:
            next_time = min(
                p["arrival"]
                for p in processes
                if p["pid"] not in completed
            )

            result.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        # Smaller priority number = higher priority
        p = min(
            ready,
            key=lambda x: (
                x["priority"],
                x["arrival"],
                x["pid"]
            )
        )

        start = current_time
        end = start + p["burst"]

        result.append((p["pid"], start, end))

        current_time = end
        completed.add(p["pid"])

    return result


# ---------------- ROUND ROBIN ----------------

def round_robin(processes, quantum):

    if quantum <= 0:
        print("Quantum must be greater than 0")
        return []

    process_list = sorted(
        processes,
        key=lambda x: (x["arrival"], x["pid"])
    )

    remaining = {
        p["pid"]: p["burst"]
        for p in process_list
    }

    queue = deque()
    result = []

    current_time = 0
    i = 0

    while i < len(process_list) or queue:

        # If ready queue is empty, CPU becomes idle
        if not queue:

            if current_time < process_list[i]["arrival"]:
                result.append((
                    "IDLE",
                    current_time,
                    process_list[i]["arrival"]
                ))

                current_time = process_list[i]["arrival"]

            # Add arrived processes
            while (
                i < len(process_list)
                and process_list[i]["arrival"] <= current_time
            ):
                queue.append(process_list[i])
                i += 1

        p = queue.popleft()

        run_time = min(
            quantum,
            remaining[p["pid"]]
        )

        start = current_time
        current_time += run_time

        result.append((
            p["pid"],
            start,
            current_time
        ))

        remaining[p["pid"]] -= run_time

        # Add newly arrived processes
        while (
            i < len(process_list)
            and process_list[i]["arrival"] <= current_time
        ):
            queue.append(process_list[i])
            i += 1

        # If process is not finished, put it back
        if remaining[p["pid"]] > 0:
            queue.append(p)

    return result


# ---------------- DISPLAY RESULT ----------------

def show_result(title, result):

    print("\n" + title)

    print("Process\tStart\tEnd")

    for item in result:
        print(
            item[0],
            "\t",
            item[1],
            "\t",
            item[2]
        )

    sequence = [item[0] for item in result]

    print("Sequence:", " -> ".join(sequence))


# ---------------- MAIN PROGRAM ----------------

print("INPUT DATA")

print("PID\tAT\tBT\tPriority")

for p in processes:
    print(
        p["pid"],
        "\t",
        p["arrival"],
        "\t",
        p["burst"],
        "\t",
        p["priority"]
    )

print("\nPriority Rule: Smaller number = Higher priority")


# Priority Scheduling
priority_result = priority_scheduling(processes)

show_result(
    "NON-PREEMPTIVE PRIORITY",
    priority_result
)


# Round Robin
quantum = 2

print("\nRound Robin Quantum =", quantum)

rr_result = round_robin(
    processes,
    quantum
)

show_result(
    "ROUND ROBIN",
    rr_result
)