"""Profiler module."""

import dataclasses
import inspect
import os
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
    filename: str = ""

    def __str__(self):
        """Return string representation."""
        if self.total > 0:
            info = f"{self.name}: "
            info += f"accumulated {self.elapsed:.3f}s"
            if self.num_calls > 0:
                info += f", per call {self.elapsed/self.num_calls:.3f}s"
            else:
                info += ", per call 0s"
            info += f", {self.num_calls} calls"
            info += f", {self.elapsed/self.total*100:.2f}% of total"
            return info
        else:
            info = f"{self.name}: "
            info += f"accumulated {self.elapsed:.3f}s"
            if self.num_calls > 0:
                info += f", per call {self.elapsed/self.num_calls:.3f}s"
            else:
                info += ", per call 0s"
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

    def start(self, name: str, filename: str = ""):
        """Start profiling."""
        if name not in self._stats:
            self._stats[name] = ProfileStats(
                name=name,
                start_time=time.perf_counter(),
                elapsed=0,
                num_calls=0,
                total=0,
                filename=os.path.basename(filename),
            )
        else:
            self._stats[name].start_time = time.perf_counter()

    def start_total(self, filename: str = ""):
        """Start total profiling."""
        self._total_stats = ProfileStats(
            name="TOTAL",
            start_time=time.perf_counter(),
            elapsed=0,
            num_calls=0,
            total=0,
            filename=os.path.basename(filename),
        )

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
        sorted_stats = dict(
            sorted(self._stats.items(), key=lambda item: item[1].elapsed, reverse=True)
        )
        if self._total_stats is not None:
            total = self._total_stats.elapsed
            headers = [
                "Name",
                "Accumulated [ms]",
                "Num calls",
                "Per call [ms]",
                "Part of total [%]",
                "Filename",
            ]
            data = []
            data.append(
                [
                    self._total_stats.name,
                    self._total_stats.elapsed * 1000,
                    self._total_stats.num_calls,
                    self._total_stats.elapsed / self._total_stats.num_calls * 1000,
                    100,
                    self._total_stats.filename,
                ]
            )
            for stat in sorted_stats:
                data.append(
                    [
                        sorted_stats[stat].name,
                        sorted_stats[stat].elapsed * 1000,
                        sorted_stats[stat].num_calls,
                        sorted_stats[stat].elapsed
                        / sorted_stats[stat].num_calls
                        * 1000,
                        sorted_stats[stat].elapsed / total * 100,
                        sorted_stats[stat].filename,
                    ]
                )
            table = tabulate(
                data, headers, floatfmt=(".1f", ".1f", ".0f", ".1f", ".1f")
            )
        else:
            headers = ["Name", "Accumulated [ms]", "Num calls", "Per call [ms]", "Filename"]
            data = []
            for stat in sorted_stats:
                data.append(
                    [
                        sorted_stats[stat].name,
                        sorted_stats[stat].elapsed * 1000,
                        sorted_stats[stat].num_calls,
                        sorted_stats[stat].elapsed
                        / sorted_stats[stat].num_calls
                        * 1000,
                        sorted_stats[stat].filename,
                    ]
                )
            table = tabulate(data, headers, floatfmt=(".1f", ".1f", ".0f", ".1f"))
        print(table)
