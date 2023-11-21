"""Profiler module."""

import dataclasses
import time

__version__ = "0.0.1"


@dataclasses.dataclass
class ProfileStats:
    """Profiler result class."""

    name: str
    start_time: float
    elapsed: float
    num_calls: int

    def __str__(self):
        """Return string representation."""
        return f"{self.name}: {self.elapsed:.2f}s, {self.num_calls} calls"

    def __eq__(self, other):
        """Return equality."""
        return self.name == other.name


class SimpleProfiler:
    """Simple profiler class."""

    def __init__(self):
        """Initialize profiler."""
        self._stats = {}

    def start(self, name: str):
        """Start profiling."""
        if name not in self._stats:
            self._stats[name] = ProfileStats(name, time.perf_counter(), 0, 0)
        else:
            self._stats[name].start_time = time.perf_counter()

    def stop(self, name: str):
        """Stop profiling."""
        if name in self._stats:
            self._stats[name].elapsed += (
                time.perf_counter() - self._stats[name].start_time
            )
            self._stats[name].num_calls += 1
        else:
            raise ValueError(f"Profiler: {name} not started")

    def print_stats(self):
        """Print profiling stats."""
        for stat in self._stats:
            print(self._stats[stat])
