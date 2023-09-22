from src.models import Timezones, Store_status, Store_hours
from datetime import datetime, timedelta
import pytz

class Store:  

    def get_timezone(storeID):

        timezone = Timezones.query.filter_by(store_id = storeID).first()
        if timezone == None:
            timezone = "America/Chicago"
        else:
            timezone = timezone.timezone_str
        return timezone

    def get_operational_hours(storeID):

        operational_hours = {'0': None, '1': None, '2': None, '3': None, '4': None, '5': None, '6': None}
        for day in range(7):
            try:
                store_timings = Store_hours.query.filter_by(store_id = storeID, day = day).all()[-1]
                operational_hours[str(day)] = {"start" :  store_timings.start_time_local, "end" : store_timings.end_time_local}
            except:
                operational_hours[str(day)] = {"start" :  "00:00:00", "end" : "00:00:00"}
        return operational_hours

    def get_current_local_time(timezone):

        local_timezone = pytz.timezone(timezone)  # Replace with your desired time zone
        current_utc_time = datetime.utcnow()
        current_local_time = current_utc_time.replace(tzinfo=pytz.UTC).astimezone(local_timezone)
        return current_local_time

    def filter_by_operational_hours(timestamps, operational_hours, diffrence_term):
        calculated_time = 0
        usable_timestamps = []
        for index in range(len(timestamps)):
            timestamp = timestamps[index]
            weekday = timestamp.weekday() + 1
            if weekday == 7:
                weekday = 0 # Sunday
            weekday_operational_hours = operational_hours.get(str(weekday))
            start_time =  weekday_operational_hours.get('start')
            end_time = weekday_operational_hours.get('end')
            if start_time != end_time:
                start_time = datetime.strptime(start_time, "%H:%M:%S").time()
                end_time = datetime.strptime(end_time, "%H:%M:%S").time()
                timestamp_time = timestamp.time()
                if (start_time <= timestamp_time <= end_time):
                    usable_timestamps.append(timestamp)
        timestamps = sorted(usable_timestamps)
        dates = set()
        for i in timestamps:
            print(i)
        for timestamp in timestamps:
            date = str(timestamp)[0:10]
            dates.add(date)
        for date in dates:
            times = set()
            for timestamp in timestamps:
                if date in str(timestamp):
                    times.add(timestamp)
            times = sorted(list(times))
            start, end= datetime.strptime(str(times[0]), "%Y-%m-%d %H:%M:%S.%f"), datetime.strptime(str(times[-1]), "%Y-%m-%d %H:%M:%S.%f")
            time_difference_seconds = (end - start).total_seconds()
            if diffrence_term == "hours":
                calculated_time += round(time_difference_seconds / 3600, 1)
            else: # minutes
                calculated_time += round(time_difference_seconds / 60) 
        return calculated_time
    
def generate_report(storeID):

    timezone = Store.get_timezone(storeID)
    current_local_time = Store.get_current_local_time(timezone)
    operational_hours = Store.get_operational_hours(storeID)
    print(operational_hours)
    
    active_timestamps = Store_status.query.filter_by(store_id = storeID, status = "active").with_entities(Store_status.timestamp_utc).all()
    inactive_timestamps = Store_status.query.filter_by(store_id = storeID, status = "inactive").with_entities(Store_status.timestamp_utc).all()

    last_hour_timestamp = (current_local_time - timedelta(hours=1)).replace(tzinfo=None)
    last_day_timestamp = (current_local_time - timedelta(days=1)).replace(tzinfo=None)
    last_week_timestamp = (current_local_time - timedelta(weeks=40)).replace(tzinfo=None)

    last_hour_active_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in active_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_hour_timestamp] 
    last_day_active_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in active_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_day_timestamp] 
    last_week_active_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in active_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_week_timestamp] 
    
    last_hour_inactive_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in inactive_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_hour_timestamp] 
    last_day_inactive_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in inactive_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_day_timestamp] 
    last_week_inactive_timestamps = [datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") for timestamp in inactive_timestamps if datetime.strptime(timestamp[0], "%Y-%m-%d %H:%M:%S.%f UTC") >= last_week_timestamp] 

    # last_hour_active_timestamps = Store.filter_by_operational_hours(last_hour_active_timestamps, operational_hours, "minutes")
    # last_day_active_timestamps = Store.filter_by_operational_hours(last_day_active_timestamps, operational_hours, "hours")
    # last_week_active_timestamps = Store.filter_by_operational_hours(last_week_active_timestamps, operational_hours, "hours")

    uptime_last_hour = Store.filter_by_operational_hours(last_hour_active_timestamps, operational_hours, "minutes")
    uptime_last_day = Store.filter_by_operational_hours(last_day_active_timestamps, operational_hours, "hours")
    uptime_last_week = Store.filter_by_operational_hours(last_week_active_timestamps, operational_hours, "hours")

    # last_day_inactive_timestamps = Store.filter_by_operational_hours(last_day_inactive_timestamps, operational_hours, "uptime", "hours")
    # last_week_inactive_timestamps = Store.filter_by_operational_hours(last_week_inactive_timestamps, operational_hours, "uptime", "hours")

    downtime_last_hour = Store.filter_by_operational_hours(last_hour_inactive_timestamps, operational_hours, "minutes")
    downtime_last_day = Store.filter_by_operational_hours(last_day_inactive_timestamps, operational_hours, "hours")
    downtime_last_week = Store.filter_by_operational_hours(last_week_inactive_timestamps, operational_hours, "hours")

    return [
        ("store_id", "uptime_last_hour(in minutes)", "uptime_last_day(in hours)", "update_last_week(in hours)", "downtime_last_hour(in minutes)", "downtime_last_day(in hours)", "downtime_last_week(in hours"),
        (storeID, uptime_last_hour, uptime_last_day, uptime_last_week, downtime_last_hour, downtime_last_day, downtime_last_week)
        ]