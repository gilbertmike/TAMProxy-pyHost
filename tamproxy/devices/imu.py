from .device import Device
from .. import config as c

class IMU(Device):

    DEVICE_CODE = c.devices.imu.code
    READ_CODE = c.devices.imu.quat_code

    def __init__(self, tamproxy, continuous=False):
        super(IMU, self).__init__(tamproxy)
        while self.id is None: pass
        if continuous:
            self.start_continuous()

        self.q0 = 0
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        
    @property
    def add_payload(self):
        return self.DEVICE_CODE

    def update(self):
        self.tamp.send_request(self.id, self.READ_CODE, self.handle_update)

    def handle_update(self, request, response):
        assert len(response) == 8
        self.q0 = (ord(response[0]) << 8) + ord(response[1])
        self.q1 = (ord(response[2]) << 8) + ord(response[3])
        self.q2 = (ord(response[4]) << 8) + ord(response[5])
        self.q3 = (ord(response[6]) << 8) + ord(response[7])