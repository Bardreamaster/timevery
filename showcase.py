import time

from timevery import Timer

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


@Timer("Locate")
def locate():
    time.sleep(1)
    print("located")


locate()

t = Timer("Sleep until next period", period=0.5, show_report=True)

for i in range(5):
    t.start()
    time.sleep(0.1)
    t.lap("do something")
    t.sleep_until_next_period_and_stop()
