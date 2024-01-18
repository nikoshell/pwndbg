import time
import cProfile

_profiler = cProfile.Profile()
_start_time = time.time()
_profiler.enable()

import pwndbg
import pwndbg.profiling

pwndbg.profiling.init(_profiler, _start_time)
pwndbg.profiling.profiler.stop("pwndbg-load.pstats")
pwndbg.profiling.profiler.start()
