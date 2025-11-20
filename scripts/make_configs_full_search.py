# author: Suhas Vittal

import os

os.system('rm -rf json/*')

for l1pref in ['no', 'berti']:
    for l2pref in ['no', 'ip_stride', 'next_line', 'pythia', 'sms', 'spp_dev', 'va_ampm_lite']:
        os.system(f'python3 scripts/make_config.py --l1pref {l1pref} --l2pref {l2pref}')
