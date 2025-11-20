import os
from sys import argv

#################################
#################################

#TRACES = ['SPEC2017', 'Google_v2', 'Graph/GAP', 'Graph/GMS', 'AI-ML']

GOOGLE_TRACES = ['Google_v2/arizona', 
                  'Google_v2/charlie', 
                  'Google_v2/merced', 
                  'Google_v2/sierra.a.3', 
                  'Google_v2/sierra.a.4',
                  'Google_v2/sierra.a.6',
                  'Google_v2/tahoe',
                  'Google_v2/tango',
                  'Google_v2/yankee'
                 ]
GRAPH_TRACES = ['Graph/GAP', 'Graph/GMS', 'Graph/Ligra']

TRACES = [*GOOGLE_TRACES, 'AI-ML', *GRAPH_TRACES, 'SPEC2017']

#################################
#################################

conf = argv[1]

OK_CONFS = ['1C.fullBW', '1C.limitBW', '4C']
if conf not in OK_CONFS:
    raise ValueError(f'conf must be one of {OK_CONFS}')

INST_SIM = 200_000_000
INST_WARMUP = 50_000_000

if conf == '4C':
    INST_SIM = 50_000_000
    INST_WARMUP = 25_000_000

#################################
#################################

def run_for_policy(policy: str):
    output_folder = f'out/{conf}/{policy}'

    os.system(f'mkdir -p {output_folder}')
    conf_exe_name = conf.replace('.', '_')
    exe_name = f'{policy}_{conf_exe_name}'

    exe = f'./bin/{exe_name}'

    for trace_folder_name in TRACES:
        trace_folder = f'/mnt/traces/{trace_folder_name}'
        os.system(f'mkdir -p {output_folder}/{trace_folder_name}')

        for f in os.listdir(trace_folder):
            if not f.endswith('.gz') and not f.endswith('.xz'):
                continue

            trace_file = f'{trace_folder}/{f}'
            name = f[:f.find('.')]

            output_path = f'{output_folder}/{trace_folder_name}/{name}.out'
            
            trace_list = [trace_file]
            if conf == '4C':
                trace_list = [trace_file for _ in range(4)]
            trace_input = ' '.join(trace_list)

            print(f'{exe} {trace_input} -w {INST_WARMUP} -i {INST_SIM} > {output_path}')

#################################
#################################

def run_all_sweep():
    for l1dpref in ['no', 'berti']:
        for l2pref in ['no', 'ip_stride', 'next_line', 'pythia', 'sms', 'spp_dev', 'va_ampm_lite']:
            run_for_policy(f'{l1dpref}_{l2pref}')

run_all_sweep()
