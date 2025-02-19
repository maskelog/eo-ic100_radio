import usb.core
import struct
from enum import Enum

class BesCmd(Enum): # Enums from decompiled Samsung framework.
    WRITE = 64
    READ = 192
    QUERY = 163
    GET = 162
    GET_FM_IC_NO = 1
    GET_FM_IC_POWER_ON_STATE = 2
    GET_CURRENT_FM_BAND = 3
    GET_CURRENT_RSSI = 4
    GET_CURRENT_SPACING = 5
    GET_MUTE_STATE = 6
    GET_FORCED_MONO_STATE = 7
    GET_CURRENT_VOLUME = 8
    GET_RDS_STATUS = 10
    GET_CURRENT_CHANNEL = 13
    GET_CURRENT_SEEKING_DC_THRESHOLD = 14
    GET_CURRENT_SEEKING_SPIKING_THRESHOLD = 15
    GET_CURRENT_FM_IC_INFO = 16
    GET_FM_RECORDING_MODE_STATUS = 17
    GET_FM_PROTOCOL_VERSION = 18
    GET_FM_INDEX = 0
    GET_DATA_LENGTH = 2
    SET = 161
    SET_POWER_STATE = 0
    SET_FM_IC_POWER_OFF = 0
    SET_FM_IC_POWER_ON = 1
    SET_FM_BAND = 1
    SET_CHAN_RSSI_TH = 2
    SET_CHAN_SPACING = 3
    SET_MUTE = 4
    SET_VOLUME = 5
    SET_MONO_MODE = 6
    SET_SEEK_START = 7
    SET_SEEK_UP = 1
    SET_SEEK_DOWN = 2
    SET_SEEK_STOP = 8
    SET_CHANNEL = 9
    SET_RDS = 10
    SET_DC_THRES = 11
    SET_SPIKE_THRES = 12
    SET_TEST_MODE = 13
    SET_RECORDING_MODE = 14
    SET_DATA_LENGTH = 1

class BesFM_Enums(Enum):
    CHAN_SPACING_200KHz = 0
    CHAN_SPACING_100KHz = 1
    CHAN_SPACING_50KHz = 2
    BAND_87MHz_108MHz = 0
    BAND_76MHz_107MHz = 1
    BAND_76MHz_91MHz = 2
    BAND_64MHz_76MHz = 3

class BesFM:
    def __init__(self, dev: usb.core.Device):
        self._dev = dev
        if self._dev.is_kernel_driver_active(4):
            self._dev.detach_kernel_driver(4)
        self._notify_ep = self._dev.get_active_configuration()[4,0][0]

    def _set(self, cmd, value):
        self._dev.ctrl_transfer(
            BesCmd.READ.value,
            BesCmd.SET.value,
            cmd, value, bytearray(BesCmd.SET_DATA_LENGTH.value)
        )

    def _get(self, cmd):
        return self._dev.ctrl_transfer(
            BesCmd.READ.value,
            BesCmd.GET.value,
            cmd, BesCmd.GET_FM_INDEX.value,
            bytearray(BesCmd.GET_DATA_LENGTH.value)
        )

    def _query(self):
        return self._dev.ctrl_transfer(
            BesCmd.READ.value,
            BesCmd.QUERY.value,
            0, 0,
            bytearray(12)
        )

    def _wait(self, timeout=None):
        try:
            resp = self._notify_ep.read(5, timeout=timeout).tobytes()
        except usb.core.USBError as e:
                if e.errno != 110:
                    raise e
        else:
            if resp[0:3] == b'\x01\x00\x08':
                return True

    def set_power(self, b):
        if self.get_recording():
            return
        if b:
            self._set(
                BesCmd.SET_POWER_STATE.value,
                BesCmd.SET_FM_IC_POWER_ON.value
            )
        else:
            self._set(
                BesCmd.SET_POWER_STATE.value,
                BesCmd.SET_FM_IC_POWER_OFF.value
            )

    def get_power(self):
        if self._get(BesCmd.GET_FM_IC_POWER_ON_STATE.value)[0]:
            return True
        else:
            return False

    def set_recording(self, b):
        if self.get_power():
            return
        if b:
            self._set(
                BesCmd.SET_RECORDING_MODE.value,
                BesCmd.SET_FM_IC_POWER_ON.value
            )
        else:
            self._set(
                BesCmd.SET_RECORDING_MODE.value,
                BesCmd.SET_FM_IC_POWER_OFF.value
            )

    def get_recording(self):
        if self._get(BesCmd.GET_FM_RECORDING_MODE_STATUS.value)[0]:
            return True
        else:
            return False

    def set_band(self, band):
        assert band in BesFM_Enums
        self._set(BesCmd.SET_FM_BAND.value, band.value)

    def get_band(self):
        return self._get(BesCmd.GET_CURRENT_FM_BAND.value)[0]

    def set_rssi_threshold(self, value):
        raise NotImplementedError

    def get_rssi_threshold(self):
        raise NotImplementedError

    def set_channel_spacing(self, spacing):
        assert spacing in BesFM_Enums
        self._set(BesCmd.SET_CHAN_SPACING.value, spacing.value)

    def get_channel_spacing(self):
        return self._get(BesCmd.GET_CURRENT_SPACING.value)[0]

    def set_mute(self, b):
        if b:
            self._set(BesCmd.SET_MUTE.value, 1)
        else:
            self._set(BesCmd.SET_MUTE.value, 0)

    def get_mute(self):
        if self._get(BesCmd.GET_MUTE_STATE.value)[0]:
            return True
        else:
            return False

    def set_volume(self, volume):
        assert 0 <= volume <= 15
        self._set(BesCmd.SET_VOLUME.value, volume)

    def get_volume(self):
        return self._get(BesCmd.GET_CURRENT_VOLUME.value)[0]

    def set_mono(self, b):
        if b:
            self._set(BesCmd.SET_MONO_MODE.value, 1)
        else:
            self._set(BesCmd.SET_MONO_MODE.value, 0)

    def get_mono(self):
        if self._get(BesCmd.GET_FORCED_MONO_STATE.value)[0]:
            return True
        else:
            return False

    def _set_seek(self, seek):
        self._set(BesCmd.SET_SEEK_START.value, seek.value)

    def seek_up(self):
        self._set_seek(BesCmd.SET_SEEK_UP)

    def seek_down(self):
        self._set_seek(BesCmd.SET_SEEK_DOWN)

    def seek_stop(self):
        self._set(BesCmd.SET_SEEK_STOP.value, 0)

    def set_channel(self, freq):
        self._set(
            BesCmd.SET_CHANNEL.value, int(freq * 100)
            )

    def get_channel(self):
        return struct.unpack('<H',self._get(BesCmd.GET_CURRENT_CHANNEL.value))[0] / 100

    def set_rds(self, b):
        if b:
            self._set(BesCmd.SET_RDS.value, 1)
        else:
            self._set(BesCmd.SET_RDS.value, 0)

    def get_rds(self):
        if self._get(BesCmd.GET_RDS_STATUS.value)[0]:
            return True
        else:
            return False

    def set_dc_threshold(self, value):
        raise NotImplementedError

    def get_dc_threshold(self):
        raise NotImplementedError

    def set_spike_threshold(self, value):
        raise NotImplementedError

    def get_spike_threshold(self):
        raise NotImplementedError

    def get_status(self):
        res = self._query()
        if res[0] == 0:
            success, freq, strength = struct.unpack('<?HB', res[1:5])
            return {'type': 'seek', 'success':success, 'freq':freq/100, 'strength':strength}
        elif res[0] == 1:
            success, freq, strength = struct.unpack('<?HB', res[1:5])
            return {'type': 'tune', 'success':success, 'freq':freq/100, 'strength':strength}
        elif res[0] == 2:
            error, strength = struct.unpack('<BB', res[1:3])
            rds = res[3:-1].tobytes()
            return {'type': 'rds', 'error':error, 'strength':strength, 'data':rds[1::-1]+rds[3:1:-1]+rds[5:3:-1]+rds[7:5:-1]}
        else:
            return res
