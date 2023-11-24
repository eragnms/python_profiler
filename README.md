# simple_profiler
A simple python profiler module

## Installation

    pipenv install ../../simpleprofiler

## Usage

Example 1:

    from simpleprofiler.simpleprofiler import SimpleProfiler
    profiler = SimpleProfiler()

    def main()
       profiler.start_total()
       profiler.start("test")
       while True
          break
       profiler.stop("test")
       profiler.stop_total()
       profiler.print_stats()

Example 2 (to get the filename of the calling file):

    profiler.start("test", __file__)

## Reuse across files
In a file profiling.py:

    from simpleprofiler.simpleprofiler import SimpleProfiler
    shared_profiler = SimpleProfiler()

In any other file that is to do profiling:

    from .profiling import shared_profiler as profiler
