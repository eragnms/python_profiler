# simple_profiler
A simple python profiler module

## Installation

    pipenv install -e ../../simpleprofiler

## Usage

    from simpleprofiler.simpleprofiler import SimpleProfiler
    profiler = SimpleProfiler()

    def main()
       profiler.start("test")
       while True
          break
       profiler.stop("test")
       profiler.print_stats()
