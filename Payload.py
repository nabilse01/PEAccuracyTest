from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class GetEP_Payload:
    data: str
    user_id: int
    fix_floor_id: int
    orientation: int
    barometer_reading: int
    session_id: str
    req_id: int
    steps_count: int
    heading: int
    orientation_status: int
    accelerometer_status: int
    is_wi_fi: bool
    reset_particles: bool
    device_id: str
    trigger_venue_detection: bool
    ############
    rssiCutOffLimitSettings: int
    minParticlesSettings: int
    maxParticlesSettings: int
    standardDeviationSettings: int

    @staticmethod
    def from_dict(obj: Any) -> 'GetEP_Payload':
        assert isinstance(obj, dict)
        data = from_str(obj.get("Data"))
        user_id = int(from_str(obj.get("UserID")))
        fix_floor_id = int(from_str(obj.get("FixFloorID")))
        orientation = int(from_str(obj.get("Orientation")))
        barometer_reading = int(from_str(obj.get("BarometerReading")))
        session_id = from_str(obj.get("SessionID"))
        req_id = int(from_str(obj.get("ReqID")))
        steps_count = int(from_str(obj.get("StepsCount")))
        heading = int(from_str(obj.get("Heading")))
        orientation_status = int(from_str(obj.get("OrientationStatus")))
        accelerometer_status = int(from_str(obj.get("AccelerometerStatus")))
        is_wi_fi = from_bool(obj.get("isWiFi"))
        reset_particles = from_bool(obj.get("ResetParticles"))
        device_id = from_str(obj.get("DeviceID"))
        trigger_venue_detection = from_bool(obj.get("TriggerVenueDetection"))
        #################
        rssiCutOffLimitSettings = int(
            from_str(obj.get("rssiCutOffLimitSettings")))
        maxParticlesSettings = int(from_str(obj.get("minParticlesSettings")))
        maxParticlesSettings = int(from_str(obj.get("maxParticlesSettings")))
        standardDeviationSettings = int(
            from_str(obj.get("standardDeviationSettings")))
        return GetEP_Payload(data, user_id, fix_floor_id, orientation, barometer_reading, session_id, req_id,
                             steps_count, heading, orientation_status, accelerometer_status, is_wi_fi, reset_particles,
                             device_id, trigger_venue_detection, rssiCutOffLimitSettings, minParticlesSettings, maxParticlesSettings, standardDeviationSettings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Data"] = from_str(self.data)
        result["UserID"] = from_str(str(self.user_id))
        result["FixFloorID"] = from_str(str(self.fix_floor_id))
        result["Orientation"] = from_str(str(self.orientation))
        result["BarometerReading"] = from_str(str(self.barometer_reading))
        result["SessionID"] = from_str(self.session_id)
        result["ReqID"] = from_str(str(self.req_id))
        result["StepsCount"] = from_str(str(self.steps_count))
        result["Heading"] = from_str(str(self.heading))
        result["OrientationStatus"] = from_str(str(self.orientation_status))
        result["AccelerometerStatus"] = from_str(
            str(self.accelerometer_status))
        result["isWiFi"] = from_bool(self.is_wi_fi)
        result["ResetParticles"] = from_bool(self.reset_particles)
        result["DeviceID"] = from_str(self.device_id)
        result["TriggerVenueDetection"] = from_bool(
            self.trigger_venue_detection)
        ############
        result["rssiCutOffLimitSettings"] = from_str(
            str(self.rssiCutOffLimitSettings))
        result["minParticlesSettings"] = from_str(
            str(self.minParticlesSettings))
        result["maxParticlesSettings"] = from_str(
            str(self.maxParticlesSettings))
        result["standardDeviationSettings"] = from_str(
            str(self.standardDeviationSettings))

        return result


def GetEP_Payload_from_dict(s: Any) -> GetEP_Payload:
    return GetEP_Payload.from_dict(s)


def GetEP_Payload_to_dict(x: GetEP_Payload) -> Any:
    return to_class(GetEP_Payload, x)


@dataclass
class EP:
    get_ep_result: str

    @staticmethod
    def from_dict(obj: Any) -> 'EP':
        assert isinstance(obj, dict)
        get_ep_result = from_str(obj.get("GetEPResult"))
        return EP(get_ep_result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["GetEPResult"] = from_str(self.get_ep_result)
        return result


def EP_from_dict(s: Any) -> EP:
    return EP.from_dict(s)


def EP_to_dict(x: EP) -> Any:
    return to_class(EP, x)
