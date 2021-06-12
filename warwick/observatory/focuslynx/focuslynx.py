#
# This file is part of focuslynxd
#
# focuslynxd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# focuslynxd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with focuslynxd.  If not, see <http://www.gnu.org/licenses/>.

"""Helper functions for communicating with the Optec Focux Lynx controller"""


class UnexpectedResponseError(Exception):
    def __init__(self, expected, actual):
        super().__init__('Unexpected data returned from FocusLynx: expected `{}`, got `{}`'.format(expected, actual))


def focuslynx_channel_config(port, channel_number):
    """
    Query and validate the initial configuration state of a focuser channel

    :param port: Serial port connection
    :param channel_number: Channel number to query
    :return: Dictionary containing:
        nickname
        device_type
        max_steps

    :raises UnexpectedResponseError if unexpected data or configuration is found
    """
    # Clear any stray data in the input buffer
    port.flushInput()

    port.write('<F{:1d}GETCONFIG>'.format(channel_number).encode('ascii'))
    line = port.readline()
    if line != b'!\n':
        raise UnexpectedResponseError('!', line)

    line = port.readline()
    expected = 'CONFIG{:1d}\n'.format(channel_number).encode('ascii')
    if line != expected:
        raise UnexpectedResponseError(expected, line)

    line = port.readline()
    if not line.startswith(b'Nickname ='):
        raise UnexpectedResponseError('Nickname = ...', line)
    nickname = line[10:].decode('ascii').strip()

    line = port.readline()
    if not line.startswith(b'Max Pos  ='):
        raise UnexpectedResponseError('Max Pos = ...', line)
    max_steps = int(line[10:])

    line = port.readline()
    if not line.startswith(b'Dev Typ  ='):
        raise UnexpectedResponseError('Dev Typ  = ...', line)
    device_type = line[10:].decode('ascii').strip()

    line = port.readline()
    if line != b'TComp ON = 0\n':
        raise UnexpectedResponseError('TComp ON = 0', line)

    # Skip temperature compensation lines
    for _ in range(6):
        port.readline()

    line = port.readline()
    if line != b'BLC En   = 0\n':
        raise UnexpectedResponseError('BLC En   = 0', line)

    # Skip backlash size, LED brightness
    for _ in range(2):
        port.readline()

    line = port.readline()
    if line != b'TC@Start = 0\n':
        raise UnexpectedResponseError('TC@Start = 0', line)

    line = port.readline()
    if line != b'END\n':
        raise UnexpectedResponseError('END', line)

    return {
        'nickname': nickname,
        'device_type': device_type,
        'max_steps': max_steps,
    }


def focuslynx_channel_status(port, channel_number):
    """
    Query the current state of a focuser channel

    :param port: Serial port connection
    :param channel_number: Channel number to query
    :return: Dictionary containing:
        temperature
        current_steps
        target_steps
        is_moving

        or None if no focuser is connected
    :raises UnexpectedResponseError if unexpected data or configuration is found
    """
    # Clear any stray data in the input buffer
    port.flushInput()

    port.write('<F{:1d}GETSTATUS>'.format(channel_number).encode('ascii'))
    line = port.readline()
    if line != b'!\n':
        raise UnexpectedResponseError('!', line)

    line = port.readline()
    expected = 'STATUS{:1d}\n'.format(channel_number).encode('ascii')
    if line != expected:
        raise UnexpectedResponseError(expected, line)

    line = port.readline()
    if not line.startswith(b'Temp(C)  ='):
        raise UnexpectedResponseError('Temp(C)  = ...', line)

    # Use the temperature probe as a proxy for the entire focuser
    if line[10:] == b' NP\n':
        # Skip remaining lines
        for _ in range(11):
            port.readline()

        return None
    temperature = float(line[10:])

    line = port.readline()
    if not line.startswith(b'Curr Pos ='):
        raise UnexpectedResponseError('Curr Pos = ...', line)
    current_steps = int(line[10:])

    line = port.readline()
    if not line.startswith(b'Targ Pos ='):
        raise UnexpectedResponseError('Targ Pos = ...', line)
    target_steps = int(line[10:])

    line = port.readline()
    if not line.startswith(b'IsMoving ='):
        raise UnexpectedResponseError('IsMoving = ...', line)
    is_moving = int(line[10:]) == 1

    #  Skip unused lines:
    #   IsHoming, IsHomed, FFDetect, TmpProbe
    #   RemoteIO, Hnd Ctlr, Reverse
    for _ in range(7):
        port.readline()

    line = port.readline()
    if line != b'END\n':
        raise UnexpectedResponseError('END', line)

    return {
        'temperature': temperature,
        'current_steps': current_steps,
        'target_steps': target_steps,
        'is_moving': is_moving
    }


def focuslynx_set_target_steps(port, channel_number, steps):
    """
    Set the target steps for a focuser channel

    :param port: Serial port connection
    :param channel_number: Channel number to query
    :param steps: Value to set the target steps

    :raises UnexpectedResponseError if unexpected data is returned
    """

    # Clear any stray data in the input buffer
    port.flushInput()

    port.write('<F{:1d}MA{:06d}>'.format(channel_number, steps).encode('ascii'))
    line = port.readline()
    if line != b'!\n':
        raise UnexpectedResponseError('!', line)

    line = port.readline()
    if line != b'M\n':
        raise UnexpectedResponseError('M', line)


def focuslynx_stop(port, channel_number):
    """
    Stops movement in a focuser channel

    :param port: Serial port connection
    :param channel_number: Channel number to query

    :raises UnexpectedResponseError if unexpected data is returned
    """

    # Clear any stray data in the input buffer
    port.flushInput()

    port.write('<F{:1d}HALT>'.format(channel_number).encode('ascii'))
    line = port.readline()
    if line != b'!\n':
        raise UnexpectedResponseError('!', line)

    line = port.readline()
    if line != b'HALTED\n':
        raise UnexpectedResponseError('HALTED', line)


def focuslynx_sync(port, channel_number, steps):
    """
    Set the current focuser position to the given step position

    :param port: Serial port connection
    :param channel_number: Channel number to query
    :param steps: Step count to set the current position

    :raises UnexpectedResponseError if unexpected data is returned
    """
    # Clear any stray data in the input buffer
    port.flushInput()

    # Set the current position to the range midpoint
    port.write('<F{:1d}SCCP{:06d}>'.format(channel_number, steps).encode('ascii'))
    line = port.readline()
    if line != b'!\n':
        raise UnexpectedResponseError('!', line)

    line = port.readline()
    if line != b'SET\n':
        raise UnexpectedResponseError('SET', line)
