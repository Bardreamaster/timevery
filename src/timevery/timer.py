import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Union


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class."""


@dataclass
class TimeRecord:
    total_time: float = 0
    time: List[float] = field(default_factory=list)


@dataclass
class Timer(ContextDecorator):
    def __init__(
        self,
        name: Optional[str] = None,
        text: Optional[str] = "Elapsed time of {name}: {:0.4f} seconds. ",
        initial_text: Union[bool, str] = False,
        show_freq: bool = False,
        show_report: bool = False,
        logger: Optional[Callable] = print,
        time_function: Optional[Callable] = time.perf_counter,
    ):
        if name is None:
            name = "Timer"
        self.name = name
        self.text = text
        if isinstance(initial_text, bool):
            initial_text = "{name} started."
        self.initial_text = initial_text
        self.show_freq = show_freq
        self.show_report = show_report
        self.logger = logger
        self.time_function = time_function  # get a time in seconds
        self._records = {name: TimeRecord()}
        self._start_time = None
        self._lap_start_time = None

    def start(self):
        """Start a new timer."""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        # Log initial text when timer starts
        if self.logger:
            initial_text = self.initial_text.format(name=self.name)
            self.logger(initial_text)

        self._start_time = self.time_function()
        self._lap_start_time = self._start_time

    def lap(self, name: Optional[str] = None) -> float:
        """Record a lap time."""
        if name is None:
            name = str(len(self._records))
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = self.time_function() - self._lap_start_time
        self._update_record(name, elapsed_time)
        self._lap_start_time = self.time_function()

        if self.logger:
            attributes = {
                "name": name,
                "milliseconds": elapsed_time * 1000,
                "seconds": elapsed_time,
                "minutes": elapsed_time / 60,
            }
            text = self.text.format(elapsed_time, **attributes)
            self.logger(str(text))

        return elapsed_time

    def stop(
        self,
    ) -> float:
        """Stop the timer, and report the elapsed time."""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = self.time_function() - self._start_time
        self._update_record(self.name, elapsed_time)
        self._start_time = None
        self._lap_start_time = None

        # Report elapsed time
        if self.logger:
            attributes = {
                "name": self.name,
                "milliseconds": elapsed_time * 1000,
                "seconds": elapsed_time,
                "minutes": elapsed_time / 60,
            }
            text = self.text.format(elapsed_time, **attributes)

            if self.show_freq:
                freq = 1 / elapsed_time
                freq_text = f" Frequency: {freq:.2f} Hz"
                text += freq_text

            self.logger(str(text))
        if self.show_report:
            self.report()
        return elapsed_time

    def report(self):
        from rich import box
        from rich.console import Console
        from rich.table import Table

        c = Console()

        headers = [
            "Name",
            "Total(s)",
            "Average(s)",
            "Freq(Hz)",
            "Percent(%)",
            "Count",
            "Min",
            "Max",
        ]
        t = Table(show_header=True, header_style="bold magenta", box=box.MARKDOWN)
        for header in headers:
            t.add_column(header, justify="center")

        total_time = self._records[self.name].total_time
        for name, record in self._records.items():
            total = record.total_time
            average = total / len(record.time)
            freq = 1 / average
            percent = total / total_time * 100
            count = len(record.time)
            min_time = min(record.time)
            max_time = max(record.time)

            t.add_row(
                name,
                f"{total:.4f}",
                f"{average:.4f}",
                f"{freq:.4f}",
                f"{percent:.4f}",
                f"{count}",
                f"{min_time:.4f}",
                f"{max_time:.4f}",
            )
        c.print(t)

    def _update_record(self, name: str, time: float):
        if name not in self._records:
            self._records[name] = TimeRecord()
        self._records[name].time.append(time)
        self._records[name].total_time += time

    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.stop()