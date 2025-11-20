#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path


def create_base_config():
    """Create the base configuration that's common to all variants."""
    return {
        "block_size": 64,
        "page_size": 4096,
        "heartbeat_frequency": 100000,

        "DIB": {
            "window_size": 16,
            "sets": 512,
            "ways": 8
        },

        "L1I": {
            "sets": 128,
            "ways": 8,
            "rq_size": 64,
            "wq_size": 64,
            "pq_size": 32,
            "mshr_size": 8,
            "latency": 4,
            "max_tag_check": 2,
            "max_fill": 2,
            "prefetch_as_load": False,
            "virtual_prefetch": True,
            "prefetch_activate": "LOAD,PREFETCH",
            "prefetcher": "no"
        },

        "ITLB": {
            "sets": 16,
            "ways": 4,
            "rq_size": 16,
            "wq_size": 16,
            "pq_size": 0,
            "mshr_size": 8,
            "latency": 1,
            "max_tag_check": 2,
            "max_fill": 2,
            "prefetch_as_load": False
        },

        "DTLB": {
            "sets": 16,
            "ways": 4,
            "rq_size": 16,
            "wq_size": 16,
            "pq_size": 0,
            "mshr_size": 8,
            "latency": 1,
            "max_tag_check": 2,
            "max_fill": 2,
            "prefetch_as_load": False
        },

        "STLB": {
            "sets": 128,
            "ways": 12,
            "rq_size": 32,
            "wq_size": 32,
            "pq_size": 0,
            "mshr_size": 16,
            "latency": 8,
            "max_tag_check": 1,
            "max_fill": 1,
            "prefetch_as_load": False
        },

        "PTW": {
            "pscl5_set": 1,
            "pscl5_way": 2,
            "pscl4_set": 1,
            "pscl4_way": 4,
            "pscl3_set": 2,
            "pscl3_way": 4,
            "pscl2_set": 4,
            "pscl2_way": 8,
            "rq_size": 16,
            "mshr_size": 5,
            "max_read": 2,
            "max_write": 2
        },

        "virtual_memory": {
            "pte_page_size": 4096,
            "num_levels": 5,
            "minor_fault_penalty": 200,
            "randomization": 1
        }
    }


def create_cpu_config():
    """Create a single CPU core configuration."""
    return {
        "frequency": 4000,
        "ifetch_buffer_size": 64,
        "decode_buffer_size": 32,
        "dispatch_buffer_size": 32,
        "register_file_size": 288,
        "rob_size": 576,
        "lq_size": 240,
        "sq_size": 112,
        "fetch_width": 8,
        "decode_width": 8,
        "dispatch_width": 8,
        "execute_width": 8,
        "lq_width": 2,
        "sq_width": 2,
        "retire_width": 8,
        "mispredict_penalty": 1,
        "scheduler_size": 160,
        "decode_latency": 1,
        "dispatch_latency": 1,
        "schedule_latency": 0,
        "execute_latency": 0,
        "branch_predictor": "perceptron",
        "btb": "basic_btb"
    }


def create_l1d_config(l1_prefetcher):
    """Create L1D cache configuration."""
    return {
        "sets": 64,
        "ways": 12,
        "rq_size": 64,
        "wq_size": 64,
        "pq_size": 8,
        "mshr_size": 16,
        "latency": 5,
        "max_tag_check": 2,
        "max_fill": 2,
        "prefetch_as_load": False,
        "virtual_prefetch": True,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": l1_prefetcher
    }


def create_l2c_config(l2_prefetcher):
    """Create L2C cache configuration."""
    return {
        "sets": 2048,
        "ways": 16,
        "rq_size": 32,
        "wq_size": 32,
        "pq_size": 16,
        "mshr_size": 32,
        "latency": 10,
        "max_tag_check": 1,
        "max_fill": 1,
        "prefetch_as_load": False,
        "virtual_prefetch": False,
        "prefetch_activate": "LOAD,PREFETCH",
        "prefetcher": l2_prefetcher
    }


def create_llc_config(num_cores):
    """Create LLC configuration based on number of cores."""
    if num_cores == 1:
        return {
            "frequency": 4000,
            "sets": 4096,
            "ways": 12,
            "rq_size": 32,
            "wq_size": 32,
            "pq_size": 32,
            "mshr_size": 64,
            "latency": 35,
            "max_tag_check": 1,
            "max_fill": 1,
            "prefetch_as_load": False,
            "virtual_prefetch": False,
            "prefetch_activate": "LOAD,PREFETCH",
            "prefetcher": "no",
            "replacement": "drrip"
        }
    else:  # 4 cores
        return {
            "frequency": 4000,
            "sets": 16384,
            "ways": 12,
            "rq_size": 128,
            "wq_size": 128,
            "pq_size": 128,
            "mshr_size": 256,
            "latency": 35,
            "max_tag_check": 1,
            "max_fill": 1,
            "prefetch_as_load": False,
            "virtual_prefetch": False,
            "prefetch_activate": "LOAD,PREFETCH",
            "prefetcher": "no",
            "replacement": "drrip"
        }


def create_memory_config(limited_bw=False):
    """Create physical memory configuration."""
    if limited_bw:
        return {
            "data_rate": 800,
            "channels": 1,
            "ranks": 1,
            "bankgroups": 8,
            "banks": 4,
            "bank_rows": 262144,
            "bank_columns": 1024,
            "channel_width": 8,
            "wq_size": 64,
            "rq_size": 64,
            "tCAS": 6,
            "tRCD": 6,
            "tRP": 6,
            "tRAS": 13,
            "refresh_period": 32,
            "refreshes_per_period": 8192
        }
    else:  # full bandwidth
        return {
            "data_rate": 4800,
            "channels": 1,
            "ranks": 1,
            "bankgroups": 8,
            "banks": 4,
            "bank_rows": 262144,
            "bank_columns": 1024,
            "channel_width": 8,
            "wq_size": 64,
            "rq_size": 64,
            "tCAS": 36,
            "tRCD": 36,
            "tRP": 36,
            "tRAS": 78,
            "refresh_period": 32,
            "refreshes_per_period": 8192
        }


def create_config(executable_name, num_cores, l1_prefetcher, l2_prefetcher, limited_bw=False):
    """Create a complete configuration."""
    config = create_base_config()
    config["executable_name"] = executable_name
    config["num_cores"] = num_cores

    # Create CPU configurations (replicate for multi-core)
    config["ooo_cpu"] = [create_cpu_config() for _ in range(num_cores)]

    # Add cache configurations
    config["L1D"] = create_l1d_config(l1_prefetcher)
    config["L2C"] = create_l2c_config(l2_prefetcher)
    config["LLC"] = create_llc_config(num_cores)

    # Add memory configuration
    config["physical_memory"] = create_memory_config(limited_bw)

    return config


def main():
    parser = argparse.ArgumentParser(description='Generate ChampSim configuration files')
    parser.add_argument('--l1pref', default='berti', help='L1 cache prefetcher (default: berti)')
    parser.add_argument('--l2pref', default='pythia', help='L2 cache prefetcher (default: pythia)')

    args = parser.parse_args()

    # Create output directory
    output_dir = Path('json') / f'{args.l1pref}_{args.l2pref}'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Configuration variants to generate
    configs = [
        {
            'filename': '1C.fullBW.json',
            'executable_name': '1C.fullBW',
            'num_cores': 1,
            'limited_bw': False
        },
        {
            'filename': '1C.limitBW.json',
            'executable_name': '1C.limitBW',
            'num_cores': 1,
            'limited_bw': True
        },
        {
            'filename': '4C.json',
            'executable_name': '4C',
            'num_cores': 4,
            'limited_bw': False
        }
    ]

    # Generate each configuration
    for config_spec in configs:
        config = create_config(
            config_spec['executable_name'],
            config_spec['num_cores'],
            args.l1pref,
            args.l2pref,
            config_spec['limited_bw']
        )

        output_file = output_dir / config_spec['filename']
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Generated: {output_file}")

    print(f"\nConfiguration files created in: {output_dir}")


if __name__ == '__main__':
    main()