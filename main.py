import psutil
import time
from notifypy import Notify

battery = psutil.sensors_battery()
battery_percentage = battery.percent
remaining_hours = battery.secsleft
notification = Notify()

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

def plugged_battery_status():
    if battery_percentage == 100 and battery.power_plugged:
        notification.title = "Full Battery"
        notification.message = "battery is fully charged! Please unplugged the charger!"
        notification.send()

def unplugged_battery_status():
    if not battery.power_plugged and battery_percentage == 80:
        notification.title = "High Battery"
        notification.message = "Battery is %s%% and %s hours remaining to shutdown." % (battery_percentage, secs2hours(remaining_hours))
        notification.send()

    elif not battery.power_plugged and battery_percentage == 50:
        notification.title = "Half Battery"
        notification.message = "Battery is %s%% and %s hours remaining to shutdown. Please connect the charger." % (battery_percentage, secs2hours(remaining_hours))
        notification.send()

    elif not battery.power_plugged and battery_percentage == 20:
        notification.title = "Low Battery"
        notification.message = "Battery is %s%% and %s hours remaining to shutdown. Please connect the charger." % (battery_percentage, secs2hours(remaining_hours))
        notification.send()

def battery_damaged():
    if battery.power_plugged and battery_percentage < 0:
        notification.title = "Damaged Battery"
        notification.message = "Battery is damaged. Please replace it as soon as possible."
        notification.send()

while not battery.power_plugged and battery_percentage < 10:
        notification.title = "Battery is Low!"
        notification.message = "Battery is %s%% and %s hours remaining to shutdown. Please connect the charger." % (battery_percentage, secs2hours(remaining_hours))
        notification.send()
        time.sleep(120)

plugged_battery_status()
unplugged_battery_status()
battery_damaged()