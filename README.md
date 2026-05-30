# Raspberry Pi Fan Controller

A lightweight version of Pironman V2.0 for Raspberry Pi that automatically controls a cooling fan based on CPU temperature.

## Features

* Automatic fan control using CPU temperature
* Configurable temperature threshold
* Low CPU usage
* Systemd service support
* Simple installation
* Works on Raspberry Pi OS and most Debian-based distributions

---

## Hardware Requirements

* Raspberry Pi (any model with GPIO support)
* Cooling fan connected through a transistor, MOSFET, relay, or compatible fan controller
* GPIO pin connected to the fan control circuit

Default GPIO pin:

```text
GPIO 6
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Cman-Github/Sunfounder-Pironman-V2.0-Simplified.git
cd Sunfounder-Pironman-V2.0-Simplified
```

### 2. Install dependencies

```bash
sudo apt update
sudo apt install python3-gpiozero python3-pip -y
pip3 install psutil
```

### 3. Install the service

```bash
sudo python3 install.py
```

---

## Configuration

Configuration file:

```text
.\config.txt
```

Example:

```ini
[fan]
gpio_pin=6
fan_temp=50
temp_lower_set=2
```

### Parameters

| Parameter      | Description                       | Default |
| -------------- | --------------------------------- | ------- |
| gpio_pin       | GPIO used to control the fan      | 6       |
| fan_temp       | Temperature that turns the fan ON | 50°C    |
| temp_lower_set | Hysteresis before turning OFF     | 2°C     |

### Example

With:

```ini
fan_temp=50
temp_lower_set=2
```

Fan behavior:

```text
50°C  -> Fan ON
49°C  -> Fan ON
48°C  -> Fan OFF
```

This prevents constant ON/OFF switching.

---

## Service Management

Start:

```bash
sudo systemctl start fan-controller
```

Stop:

```bash
sudo systemctl stop fan-controller
```

Restart:

```bash
sudo systemctl restart fan-controller
```

Enable at boot:

```bash
sudo systemctl enable fan-controller
```

Disable at boot:

```bash
sudo systemctl disable fan-controller
```

Check status:

```bash
sudo systemctl status fan-controller
```

---

## Manual Launch

Run in foreground:

```bash
python3 fan_controller.py
```

---

## How It Works

The service continuously monitors Raspberry Pi CPU temperature.

Logic:

```text
Temperature > fan_temp
    → Fan ON

Temperature < fan_temp - temp_lower_set
    → Fan OFF
```

Example:

```text
fan_temp = 50°C
temp_lower_set = 2°C

51°C → ON
50°C → ON
49°C → ON
48°C → OFF
```

---

## Supported Operating Systems

Tested on:

* Raspberry Pi OS Bookworm
* Raspberry Pi OS Bullseye
* Raspberry Pi OS Lite
* Ubuntu Server for Raspberry Pi
* Debian ARM

---

## License

GNU GPL v3

You are free to modify, distribute and improve the software under the terms of the GPL license.

---

## Author

Custom Fan Controller for Raspberry Pi

Designed for simple, reliable automatic cooling control.
