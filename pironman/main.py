import os
import sys
import time

from gpiozero import DigitalOutputDevice as Fan
from configparser import ConfigParser

from system_status import *
from utils import log, run_command
from app_info import __app_name__, __version__, username, config_file

# =================================================================
# print info
# =================================================================

line = '-' * 24
_time = time.strftime("%y/%m/%d %H:%M:%S", time.localtime())

log('\n%s%s%s' % (line, _time, line), timestamp=False)
log('%s version: %s' % (__app_name__, __version__), timestamp=False)
log('username: %s' % username, timestamp=False)
log('config_file: %s' % config_file, timestamp=False)

# Kernel Version
status, result = run_command("uname -a")
if status == 0:
    log("\nKernel Version:", timestamp=False)
    log(f"{result}", timestamp=False)

# OS Version
status, result = run_command("lsb_release -a|grep Description")
if status == 0:
    log("OS Version:", timestamp=False)
    log(f"{result}", timestamp=False)

# PCB information
status, result = run_command("cat /proc/cpuinfo|grep -E 'Revision|Model'")
if status == 0:
    log("PCB info:", timestamp=False)
    log(f"{result}", timestamp=False)

# =================================================================
# Config
# =================================================================

fan_pin = 6
update_frequency = 0.5

temp_unit = 'C'
fan_temp = 50
temp_lower_set = 2

config = ConfigParser()

if not os.path.exists(config_file):
    log('Configuration file does not exist, recreating ...')

    status, result = run_command(
        cmd=f'sudo touch {config_file} && sudo chmod 774 {config_file}'
    )

    if status != 0:
        log('create config_file failed:\n%s' % result)
        raise Exception(result)

try:
    config.read(config_file)

    temp_unit = config['all']['temp_unit']
    fan_temp = float(config['all']['fan_temp'])

except Exception as e:
    log(f"read config error: {e}")

    config['all'] = {
        'temp_unit': temp_unit,
        'fan_temp': fan_temp,
    }

    with open(config_file, 'w') as f:
        config.write(f)

log("fan_pin : %s" % fan_pin)
log("update_frequency : %s" % update_frequency)
log("temp_unit : %s" % temp_unit)
log("fan_temp : %s" % fan_temp)
log(">>>", timestamp=False)

# =================================================================
# Fan init
# =================================================================

fan_ok = False

try:
    fan = Fan(fan_pin)
    fan_ok = True
    log('fan init success')

except Exception as e:
    fan_ok = False
    log(f'fan init failed:\n{e}')

# =================================================================
# Exit handler
# =================================================================

def exit_handler():
    try:
        if fan_ok:
            fan.off()
            fan.close()

        sys.exit(0)

    except:
        pass

# =================================================================
# Main
# =================================================================

def main():
    global fan_temp

    while True:

        CPU_temp_C = float(get_cpu_temperature())
        CPU_temp_F = float(CPU_temp_C * 1.8 + 32)

        if fan_ok:

            if temp_unit == 'C':

                if CPU_temp_C > fan_temp:
                    fan.on()

                elif CPU_temp_C < fan_temp - temp_lower_set:
                    fan.off()

            elif temp_unit == 'F':

                if CPU_temp_F > fan_temp:
                    fan.on()

                elif CPU_temp_F < fan_temp - temp_lower_set * 1.8:
                    fan.off()

            else:

                if CPU_temp_C > 50:
                    fan.on()

                elif CPU_temp_C < 40:
                    fan.off()

        time.sleep(update_frequency)

# =================================================================

if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        log(f'error\n{e}')

    finally:
        exit_handler()
