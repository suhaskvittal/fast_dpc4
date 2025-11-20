import os

THREADS = 16

for f in os.listdir('json'):
    if not os.path.isdir(f'json/{f}'):
        continue
    for ff in os.listdir(f'json/{f}'):
        path = f'json/{f}/{ff}'
        print(f'BUILDING {f}/{ff} ===============================\n')
        os.system(f'make clean && make configclean && ./config.sh {path} && make -j{THREADS}')
