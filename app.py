from time import sleep
import monitorcontrol

from mylogger import get_logger

# List of OLED monitors that we can use to trigger the refreshing 
OLED_list = ["AW3423DWF"]
# The desired waiting time, that the monitor usually take to refresh itself
WAITING_TIME = 300

my_logger = get_logger()

def get_oled_monitors() -> list[monitorcontrol.Monitor]:
    """
    Return the list of monitors currently detected on the system that are OLED monitors 
        
    # Returns: 
    list[monitorcontrol.Monitor]
    """
    OLED_monitors = []
    for monitor in monitorcontrol.get_monitors():
        with monitor:
            try:
                t = monitor.get_vcp_capabilities().get("model")
                if t in OLED_list:
                    OLED_monitors.append(monitor)
            except monitorcontrol.VCPError as e:
                print(e)

    return OLED_monitors


def refresh_monitors(monitors_list: list[monitorcontrol.Monitor]):
    """
    Refresh the list of monitor provided 

    # Args 
    - monitor_list : list[monitorcontrol.Monitor] A list of monirtors that will be refreshed

    # Returns:
    Nothing

    Send a command to shut down the monitor.
    - If the monitor stays "on", it meens that the panel if refreshing. We wait until it shut down, and we send a command to wake it up again
    - If it immediatly shut down, it means it's not refreshing, so we can power it on again 
    """
    for monitor in monitors_list:
        with monitor:
            # Shut down the monitor. 
            monitor.set_power_mode(monitorcontrol.PowerMode.off_soft)
            # Wait for the command to complete and for it to actually shut down
            sleep(10)
            # Check if the pannel is still on or not 
            if monitor.get_power_mode() == monitorcontrol.PowerMode.on:
                # Yes, means that the pannel is refreshing. We wait the ammount of time defined in *WAITING_TIME*
                my_logger.info(f"Refreshing pannel, waiting {WAITING_TIME}s")
                sleep(WAITING_TIME)
                while monitor.get_power_mode() == monitorcontrol.PowerMode.on:
                    my_logger.info("Pannel still refershing")
                    sleep(10)
            # OLED is now off, we now start it
            else:
                my_logger.info("Pannel does not need to be refreshed")
            monitor.set_power_mode(monitorcontrol.PowerMode.on)


if __name__ == "__main__":
    a = get_oled_monitors()
    refresh_monitors(a)
