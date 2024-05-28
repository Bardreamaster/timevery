# timevery

Python timer for measuring execution time.

## Basic Usage

You can use `timevery.Timer` in several different ways:

1. As a **class**:

    ```python
    a = Timer("Detect", show_freq=True, logger=print)

    for i in range(5):
        a.start()

        time.sleep(0.1)
        a.lap("detect")

        if i % 2 == 0:
            time.sleep(0.1)
            a.lap("segment")

        time.sleep(0.2)
        a.lap("plot")
        a.stop()
    a.report()
    ```

    <details>
    <summary>Click to see the output</summary>

    ```bash
    >>>
        Detect started.
        Elapsed time of detect: 0.1002 seconds.
        Elapsed time of segment: 0.1003 seconds.
        Elapsed time of plot: 0.2003 seconds.
        Elapsed time of Detect: 0.4009 seconds.  Frequency: 2.49 Hz
        Detect started.
        Elapsed time of detect: 0.1001 seconds.
        Elapsed time of plot: 0.2004 seconds.
        Elapsed time of Detect: 0.3006 seconds.  Frequency: 3.33 Hz
        Detect started.
        Elapsed time of detect: 0.1001 seconds.
        Elapsed time of segment: 0.1002 seconds.
        Elapsed time of plot: 0.2004 seconds.
        Elapsed time of Detect: 0.4008 seconds.  Frequency: 2.49 Hz
        Detect started.
        Elapsed time of detect: 0.1001 seconds.
        Elapsed time of plot: 0.2004 seconds.
        Elapsed time of Detect: 0.3006 seconds.  Frequency: 3.33 Hz
        Detect started.
        Elapsed time of detect: 0.1002 seconds.
        Elapsed time of segment: 0.1003 seconds.
        Elapsed time of plot: 0.2004 seconds.
        Elapsed time of Detect: 0.4010 seconds.  Frequency: 2.49 Hz

        |  Name   | Total(s) | Average(s) | Freq(Hz) | Percent(%) | Count |  Min   |  Max   |
        |---------|----------|------------|----------|------------|-------|--------|--------|
        | Detect  |  1.8040  |   0.3608   |  2.7716  |  100.0000  |   5   | 0.3006 | 0.4010 |
        | detect  |  0.5008  |   0.1002   |  9.9831  |  27.7627   |   5   | 0.1001 | 0.1002 |
        | segment |  0.3008  |   0.1003   |  9.9739  |  16.6730   |   3   | 0.1002 | 0.1003 |
        |  plot   |  1.0018  |   0.2004   |  4.9909  |  55.5327   |   5   | 0.2003 | 0.2004 |
    ```

    </details>

2. As a **context manager**:

    ```python
    with Timer("MakeRobot", show_report=True) as t:
        time.sleep(1)
        t.lap("foot")
        time.sleep(1)
        t.lap("hand")
        time.sleep(1)
        t.lap("head")
        time.sleep(2)
        t.lap("body")
        time.sleep(1)
        t.lap("combine")
    ```

    <details>
    <summary>Click to see the output</summary>

    ```bash
    >>>
        MakeRobot started.
        Elapsed time of foot: 1.0011 seconds.
        Elapsed time of hand: 1.0012 seconds.
        Elapsed time of head: 1.0010 seconds.
        Elapsed time of body: 2.0021 seconds.
        Elapsed time of combine: 1.0012 seconds.
        Elapsed time of MakeRobot: 6.0068 seconds.
        |   Name    | Total(s) | Average(s) | Freq(Hz) | Percent(%) | Count |  Min   |  Max   |
        |-----------|----------|------------|----------|------------|-------|--------|--------|
        | MakeRobot |  6.0068  |   6.0068   |  0.1665  |  100.0000  |   1   | 6.0068 | 6.0068 |
        |   foot    |  1.0011  |   1.0011   |  0.9989  |  16.6663   |   1   | 1.0011 | 1.0011 |
        |   hand    |  1.0012  |   1.0012   |  0.9988  |  16.6679   |   1   | 1.0012 | 1.0012 |
        |   head    |  1.0010  |   1.0010   |  0.9990  |  16.6640   |   1   | 1.0010 | 1.0010 |
        |   body    |  2.0021  |   2.0021   |  0.4995  |  33.3309   |   1   | 2.0021 | 2.0021 |
        |  combine  |  1.0012  |   1.0012   |  0.9988  |  16.6674   |   1   | 1.0012 | 1.0012 |
    ```

    </details>

3. As a **decorator**:

    ```python
    @Timer("Locate")
    def locate():
        time.sleep(1)
        print("located")

    locate()
    ```

    <details>
    <summary>Click to see the output</summary>

    ```bash
    >>>
        Locate started.
        located
        Elapsed time of Locate: 1.0011 seconds.
    ```

    </details>

## Acknowledgement

Thanks to [this tutorial](https://realpython.com/python-timer/) and the [`codetiming`](https://github.com/realpython/codetiming) for the inspiration.
