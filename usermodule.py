import time

def handler(input: dict, context: object) -> dict:
    if not hasattr(context, 'env'):
        context.env = {}

    timestamp = input['timestamp']
    bytes_sent = input['net_io_counters_eth0-bytes_sent1']
    bytes_recv = input['net_io_counters_eth0-bytes_recv1']
    cached_memory = input['virtual_memory-cached']
    buffer_memory = input['virtual_memory-buffers']
    total_memory = input['virtual_memory-total']
    num_cpus = len([key for key in input if key.startswith('"cpu_percent-"')])

    percent_network_egress = (bytes_sent / (bytes_sent + bytes_recv)) * 100

    percent_memory_cache = ((cached_memory + buffer_memory) / total_memory) * 100

    cpu_utilization = {}
    for cpu_id in range(num_cpus):
        cpu_key = f"cpu_percent-{cpu_id}"
        cpu_utilization[cpu_key] = input[cpu_key]

        if f"cpu_percent-{cpu_id}" not in context.env:
            context.env[f"cpu_percent-{cpu_id}"] = []

        context.env[f"cpu_percent-{cpu_id}"].append(cpu_utilization)
        if len(context.env[f"cpu_percent-{cpu_id}"]) > 12:
            context.env[f"cpu_percent-{cpu_id}"].pop(0)

        avg_util = sum(context.env[f"cpu_avg_{cpu_id}"]) / len(context.env[f"cpu_avg_{cpu_id}"])
        cpu_utilization[f"avg-util-cpu{cpu_id}-60sec"] = avg_util

    return {
        'timestamp': timestamp,
        'percent_network_egress': percent_network_egress,
        'percent_memory_cache': percent_memory_cache,
        **cpu_utilization
    }