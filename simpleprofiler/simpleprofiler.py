"""Profiler module."""

import dataclasses
import time


@dataclasses.dataclass
class ProfileStats:
    """Profiler result class."""

    name: str
    start_time: float
    elapsed: float
    num_calls: int
    total: float = 0.0

    def __str__(self):
        """Return string representation."""
        if self.total > 0:
            info = f"{self.name}: "
            info += f"accumulated {self.elapsed:.3f}s"
            info += f", per call {self.elapsed/self.num_calls:.3f}s"
            info += f", {self.num_calls} calls"
            info += f", {self.elapsed/self.total*100:.2f}% of total"
            return info
        else:
            info = f"{self.name}: "
            info += f"accumulated {self.elapsed:.3f}s"
            info += f", per call {self.elapsed/self.num_calls:.3f}s"
            info += f", {self.num_calls} calls"
            return info


    def __eq__(self, other):
        """Return equality."""
        return self.name == other.name


class SimpleProfiler:
    """Simple profiler class."""

    def __init__(self):
        """Initialize profiler."""
        self._stats = {}
        self._total_stats = None

    def start(self, name: str):
        """Start profiling."""
        if name not in self._stats:
            self._stats[name] = ProfileStats(name, time.perf_counter(), 0, 0)
        else:
            self._stats[name].start_time = time.perf_counter()

    def start_total(self):
        """Start total profiling."""
        self._total_stats = ProfileStats("TOTAL", time.perf_counter(), 0, 0)

    def stop(self, name: str):
        """Stop profiling."""
        if name in self._stats:
            self._stats[name].elapsed += (
                time.perf_counter() - self._stats[name].start_time
            )
            self._stats[name].num_calls += 1
        else:
            raise ValueError(f"Profiler: {name} not started")

    def stop_total(self):
        """Stop total profiling."""
        self._total_stats.elapsed += (
            time.perf_counter() - self._total_stats.start_time
        )
        self._total_stats.num_calls += 1

    def print_stats(self):
        """Print profiling stats."""
        total = 0.0
        if self._total_stats is not None:
            print(self._total_stats)
            total = self._total_stats.elapsed
        for stat in self._stats:
            self._stats[stat].total = total
            print(self._stats[stat])
