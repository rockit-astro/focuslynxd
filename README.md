## Focuser daemon

`focusd` interfaces with and wraps the Optec focusers and exposes them via Pyro.

`focus` is a commandline utility for controlling the focusers.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the software architecture and instructions for developing and deploying the code.

The QuickSync focusers use relative encoders, but the Focus Lynx units remember their positions
across power cycles.  After setting or changing the nominal focus position the `focus` `zero`
command should be used to reset the limits based on this zero point.

Note that `focusd` maps the strictly positive encoder step range (0..MAX) to a more convenient
signed value (-MAX/2..MAX/2).  This allows `0` to be defined as the nominal focus position.

### Configuration

Configuration is read from json files that are installed by default to `/etc/focusd`.
A configuration file is specified when launching the server, and the `focus` frontend will search this location when launched.

The configuration options are:
```python
{
  "daemon": "localhost_test3", # Run the server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "log_name": "focusd@test", # The name to use when writing messages to the observatory log.
  "control_machines": ["LocalHost"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `warwick.observatory.common.IP`.
  "serial_port": "/dev/focuser", # Serial FIFO for communicating with the focuser
  "serial_baud": 115200, # Serial baud rate (always 115200)
  "serial_timeout": 5, # Serial comms timeout
  "idle_loop_delay": 5, # Delay in seconds between focuser status polls when idle
  "moving_loop_delay": 0.5, # Delay in seconds between focuser status polls when moving
  "move_timeout": 180, # Maximum time expected for a focus movement
  "home_reset_timeout": 2, # Maximum time expected when resetting the home position
  "soft_step_limits": [-50000, 50000] # Prevent movement commands outside this range
}

```

## Initial Installation


The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package           | Description |
| ----------------- | ------ |
| observatory-focuslynx-server | Contains the `focusd` server and systemd service file. |
| observatory-focuslynx-client | Contains the `focus` commandline utility for controlling the focuser server. |
| python3-warwick-observatory-focuslynx | Contains the python module with shared code. |
| clasp-focuslynx-data | Contains the json configuration for the CLASP telescope. |

`obsevatory-focuslynx-server` and `observatory-focuslynx-client` and `clasp-focuslynx-data` should be installed on the `clasp-tcs` machine.

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable focusd@<config>
sudo systemctl start focusd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `warwick.observatory.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl stop focusd@<config>
sudo systemctl start focusd@<config>
```

### Testing Locally

The camera server and client can be run directly from a git clone:
```
./focusd test.json
FOCUSD_CONFIG_PATH=./test.json ./focus status
```
