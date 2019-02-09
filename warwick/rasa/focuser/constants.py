#
# This file is part of rasa-camd
#
# rasa-camd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rasa-camd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rasa-camd.  If not, see <http://www.gnu.org/licenses/>.

"""Constants and status codes used by rasa-camd"""

# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name

FMT_GREEN = u'\033[92m'
FMT_RED = u'\033[91m'
FMT_CYAN = u'\033[96m'
FMT_YELLOW = u'\033[93m'
FMT_BOLD = u'\033[1m'
FMT_CLEAR = u'\033[0m'

class CommandStatus:
    """Numeric return codes"""
    # General error codes
    Succeeded = 0
    Failed = 1
    Blocked = 2
    InvalidControlIP = 3

    InvalidChannel = 4
    ChannelNotAvailable = 5
    PositionOutsideLimits = 6

    _messages = {
        # General error codes
        1: 'error: command failed',
        2: 'error: another command is already running',
        3: 'error: command not accepted from this IP',
        4: 'error: invalid channel',
        5: 'error: channel disconnected or in error state',
        6: 'error: requested position outside channel range',

        -100: 'error: terminated by user',
        -101: 'error: unable to communicate with focus daemon',
    }

    @classmethod
    def message(cls, error_code):
        """Returns a human readable string describing an error code"""
        if error_code in cls._messages:
            return cls._messages[error_code]
        return 'error: Unknown error code {}'.format(error_code)

class FocuserStatus:
    """Status of the focuser hardware"""
    Disconnected, Error, Idle, Moving = range(4)

    _labels = {
        0: 'DISCONNECTED',
        1: 'ERROR',
        2: 'IDLE',
        3: 'MOVING',
    }

    _formats = {
        0: FMT_BOLD + FMT_RED,
        1: FMT_BOLD,
        2: FMT_BOLD,
        3: FMT_BOLD + FMT_YELLOW,
    }

    @classmethod
    def label(cls, status, formatting=False):
        """Returns a human readable string describing a status
           Set formatting=true to enable terminal formatting characters
        """
        if formatting:
            if status in cls._formats and status in cls._formats:
                return cls._formats[status] + cls._labels[status] + FMT_CLEAR
            return FMT_RED + FMT_BOLD + 'UNKNOWN' + FMT_CLEAR
        else:
            if status in cls._labels:
                return cls._labels[status]
            return 'UNKNOWN'
