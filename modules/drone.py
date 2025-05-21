import pymavlink
from pymavlink import mavutil

class Drone:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.mavlink_connection = pymavlink.mavutil.mavlink_connection(connection_string)
        self.mavlink_connection.wait_heartbeat()
        print("Connected to drone and received heartbeat.")
        
    def arm(self):
        print("Arming drone...")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,  # confirmation
            1,  # arm
            0, 0, 0, 0, 0, 0
        )
        
    def takeoff(self, altitude):
        print(f"Taking off to {altitude} meters.")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,  # confirmation
            0, 0, 0, 0, 0, 0, altitude
        )
        
    def land(self):
        print("Landing...")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0,
            0, 0, 0, 0, 0, 0, 0
        )
        
    def rtl(self):
        print("Returning to Launch (RTL)...")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
            0,
            0, 0, 0, 0, 0, 0, 0
        )

    def travel_relative(self, x, y, z):
        print(f"Traveling relative to ({x}, {y}, {z})")
        self.mavlink_connection.mav.set_position_target_local_ned_send(
            int(self.mavlink_connection.time_since("SYSTEM_TIME")),
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
            0b110111111000,
            x, y, -z,
            0, 0, 0,
            0, 0, 0,
            0, 0)
        
    def travel_absolute(self, lat, long, alt):
        print(f"Traveling to absolute coordinates ({lat}, {long}, {alt})")
        self.mavlink_connection.mav.set_position_target_global_int_send(
            int(self.mavlink_connection.time_since("SYSTEM_TIME")),
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            0b110111111000,
            int(lat * 1e7), int(long * 1e7), alt,
            0, 0, 0,
            0, 0, 0,
            0, 0)
        
    def yaw_relative(self, angle):
        print(f"Yawing relative to {angle} degrees.")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,  # confirmation
            abs(angle),  # yaw angle
            90, # yaw speed
            -1 if angle < 0 else 1, # direction
            1, # relative
            0, 0, 0,
        )
        
    def yaw_absolute(self, angle):
        print(f"Yawing to absolute {angle} degrees.")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,  # confirmation
            angle,  # yaw angle
            90, # yaw speed
            0, # direction
            0, # absolute
            0, 0, 0,
        )
        
    def circle(self):
        print("Circling...")
        self.mavlink_connection.mav.command_long_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,
            0,  # confirmation
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            7,  # Circle mode
            0, 0, 0, 0, 0
        )
