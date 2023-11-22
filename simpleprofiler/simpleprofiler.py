"""Profiler module."""

import dataclasses
import time

from tabulate import tabulate


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
        self._total_stats.elapsed += time.perf_counter() - self._total_stats.start_time
        self._total_stats.num_calls += 1

    def print_stats(self):
        """Print profiling stats."""
        total = 0.0
        if self._total_stats is not None:
            total = self._total_stats.elapsed
            headers = [
                "Name",
                "Accumulated [s]",
                "Num calls",
                "Per call [s]",
                "Part of total [%]",
            ]
            data = []
            data.append(
                [
                    self._total_stats.name,
                    self._total_stats.elapsed,
                    self._total_stats.num_calls,
                    self._total_stats.elapsed / self._total_stats.num_calls,
                    100,
                ]
            )
            for stat in self._stats:
                data.append(
                    [
                        self._stats[stat].name,
                        self._stats[stat].elapsed,
                        self._stats[stat].num_calls,
                        self._stats[stat].elapsed / self._stats[stat].num_calls,
                        self._stats[stat].elapsed / total * 100,
                    ]
                )
                table = tabulate(
                    data, headers, floatfmt=(".3f", ".3f", ".0f", ".3f", ".2f")
                )
        else:
            headers = ["Name", "Accumulated [s]", "Num calls", "Per call [s]"]
            data = []
            for stat in self._stats:
                data.append(
                    [
                        self._stats[stat].name,
                        self._stats[stat].elapsed,
                        self._stats[stat].num_calls,
                        self._stats[stat].elapsed / self._stats[stat].num_calls,
                    ]
                )
                table = tabulate(data, headers, floatfmt=(".3f", ".3f", ".0f", ".3f"))
        print(table)
