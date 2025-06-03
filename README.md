# raspberry-pi-single-button-multi-function

Script can be used to give a single button on the Raspberry Pi multiple
functions (with led0/led1 feedback) depending on how many presses, for example 2
presses to pause a docker service, 4 presses to stop a docker service, and 6 to
power off. Its setup for a Raspberry Pi 3, but can be used for other Pi models
as well, just doublecheck which gpio pins to use.

Some items, images/text are from
[Howchoo Raspberry Pi power button guide](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi).

## Installation

1. [Connect to your Raspberry Pi via SSH](https://howchoo.com/g/mgi3mdnlnjq/how-to-log-in-to-a-raspberry-pi-via-ssh)
1. Clone this repo:
   `git clone https://github.com/davidchilin/raspberry-pi-single-button-multi-function`
1. Edit lines 25, 30, 35 to perform the functions you want, default is set to
   pause a docker service with 2 presses, 4 will stop the docker service, and 6
   will power off the Pi. **Optional:** Edit line 9 in multifunction_button.py
   to your preferred pin (currently set to pin 5/gpio 3 which has power ON
   functionality)
1. Either:
   - Create a new systemd service
     1. with a new "multibuton.service" file in /etc/systemd/system with contents:
        ```
        [Unit]
        Description=Multifunction Button Thread
        [Service]
        Type=simple
        ExecStart=/file/path_to/multifunction_button.py
        Restart=always
        [Install]
        WantedBy=multi-user.target
        ```
     3. add execute permission with command:
        `sudo chmod +x /file/path_to/multifunction_button.py`
     4. enable and start the service:
        `sudo systemctl enable multifunction_button` then
        `sudo systemctl start multifunction_button`
   - OR Run the setup script, to install and use init.d:
     `./raspberry-pi-single-button-multi-function/script/install`

## Uninstallation

Uninstall the way you installed, either:

- stop the service 'sudo systemctl disable multifunction_button' and delete
  relevant files
- run uninstall script:
  `./raspberry-pi-single-button-multi-function/script/uninstall`

## Hardware

A full list of what you'll need can be found
[here](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi#parts-list).
At a minimum, you'll need a normally-open (NO) power button, and some jumper
wires.

Connect the power button to Pin 5 (GPIO 3/SCL) and Pin 6 (GND) as shown in the
diagram:

![Connection Diagram](https://raw.githubusercontent.com/davidchilin/raspberry-pi-single-button-multi-function/master/diagrams/pinout.png)

### Is it possible to use another pin other than Pin 5 (GPIO 3/SCL)?

Yes, if you do not need power on functionality for the Pi, you can use gpio
21/pin 40 or gpio 7/pin 26.

There are two main features of the button using Pin 5/GPIO 3:

1. **Shutdown functionality:** Shut the Pi down safely when the button is
   pressed. The Pi now consumes zero power.
1. **Wake functionality:** Turn the Pi back on when the button is pressed again.

The **wake functionality** requires the SCL pin, Pin 5 (GPIO 3). There's simply
no other pin that can "hardware" wake the Pi from a zero-power state. If you
don't care about turning the Pi back _on_ using the power button, you could use
a different GPIO pin for the **shutdown functionality** and still have a working
multifunction_button button. Then, to turn the Pi back on, you'll just need to
disconnect and reconnect power (or use a cord with a physical switch in it) to
"wake" the Pi.

Of course, for the GND connection, you can use
[any other ground pin you want](https://pinout.xyz/).
