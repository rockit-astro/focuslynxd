## RASA prototype focuser daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/rasa-focusd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/rasa-focusd)

Part of the observatory software for the RASA prototype telescope.

`focusd` interfaces with and wraps the Optec focusers and exposes them via Pyro.

`focus` is a commandline utility for controlling the focusers.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Hardware Setup

The QuickSync focusers use relative encoders, but the Focus Lynx units remember their positions
across power cycles.  After setting or changing the nominal focus position the `focus` `zero`
command should be used to reset the limits based on this zero point.

Note that `focusd` maps the strictly positive encoder step range (0..MAX) to a more convenient
signed value (-MAX/2..MAX/2).  This allows `0` to be defined as the nominal focus position.

### Software Setup

After installing `rasa-focuser-server`, the `rasa_focusd` service must be enabled using:
```
sudo systemctl enable rasa_focusd.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start rasa_focusd.service
```

Finally, open ports in the firewall so that other machines on the network can access the daemons:
```
sudo firewall-cmd --zone=public --add-port=9036/tcp --permanent
sudo firewall-cmd --reload
```

