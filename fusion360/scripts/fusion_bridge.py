#!/usr/bin/env python3
"""
Fusion 360 Bridge Helper
========================
Python helper for sending commands to the Fusion 360 ClaudeBridge add-in.

Usage:
    from fusion_bridge import FusionBridge

    bridge = FusionBridge()
    bridge.ping()
    bridge.create_sketch("xy")
    bridge.draw_circle(0, 0, 2.5)
    bridge.extrude(height=5)
"""

import json
import os

BASE_DIR = os.path.expanduser("~/Documents/scripts/fusion_360/ClaudeBridge")
COMMANDS_FILE = os.path.join(BASE_DIR, "commands.json")
RESULTS_FILE = os.path.join(BASE_DIR, "results.json")


class FusionBridge:
    """Helper class for interacting with Fusion 360 via ClaudeBridge."""

    def __init__(self):
        self.command_id = self._get_last_command_id()

    def _get_last_command_id(self):
        """Get the last processed command ID."""
        try:
            with open(RESULTS_FILE, 'r') as f:
                data = json.load(f)
                return data.get('command_id', 0)
        except:
            return 0

    def _send_command(self, action, params=None):
        """Send a command and read result."""
        self.command_id += 1
        cmd = {
            "id": self.command_id,
            "action": action,
            "params": params or {}
        }

        with open(COMMANDS_FILE, 'w') as f:
            json.dump(cmd, f, indent=2)

        try:
            with open(RESULTS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Connection commands
    def ping(self):
        """Test the bridge connection."""
        return self._send_command("ping")

    def message(self, text):
        """Display a message in Fusion 360."""
        return self._send_command("message", {"text": text})

    # Information commands
    def get_info(self):
        """Get design information."""
        return self._send_command("get_info")

    def list_profiles(self, sketch_index=None):
        """List profiles in a sketch."""
        params = {}
        if sketch_index is not None:
            params["sketch_index"] = sketch_index
        return self._send_command("list_profiles", params)

    # Sketch commands
    def create_sketch(self, plane="xy"):
        """Create a new sketch on a plane (xy, xz, or yz)."""
        return self._send_command("create_sketch", {"plane": plane})

    def draw_circle(self, x=0, y=0, radius=1, sketch_index=None):
        """Draw a circle."""
        params = {"x": x, "y": y, "radius": radius}
        if sketch_index is not None:
            params["sketch_index"] = sketch_index
        return self._send_command("draw_circle", params)

    def draw_rectangle(self, x=0, y=0, width=1, height=1, sketch_index=None):
        """Draw a rectangle."""
        params = {"x": x, "y": y, "width": width, "height": height}
        if sketch_index is not None:
            params["sketch_index"] = sketch_index
        return self._send_command("draw_rectangle", params)

    def draw_line(self, x1=0, y1=0, x2=1, y2=1, sketch_index=None):
        """Draw a line."""
        params = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        if sketch_index is not None:
            params["sketch_index"] = sketch_index
        return self._send_command("draw_line", params)

    # 3D commands
    def extrude(self, height=1, sketch_index=None, profile_index=0, operation="new"):
        """Extrude a profile. operation: 'new', 'join', or 'cut'."""
        params = {"height": height, "profile_index": profile_index, "operation": operation}
        if sketch_index is not None:
            params["sketch_index"] = sketch_index
        return self._send_command("extrude", params)


# Convenience functions for direct use
_bridge = None

def get_bridge():
    """Get or create a bridge instance."""
    global _bridge
    if _bridge is None:
        _bridge = FusionBridge()
    return _bridge

def ping():
    return get_bridge().ping()

def create_sketch(plane="xy"):
    return get_bridge().create_sketch(plane)

def draw_circle(x=0, y=0, radius=1):
    return get_bridge().draw_circle(x, y, radius)

def draw_rectangle(x=0, y=0, width=1, height=1):
    return get_bridge().draw_rectangle(x, y, width, height)

def draw_line(x1=0, y1=0, x2=1, y2=1):
    return get_bridge().draw_line(x1, y1, x2, y2)

def extrude(height=1, profile_index=0, operation="new"):
    return get_bridge().extrude(height, profile_index=profile_index, operation=operation)

def get_info():
    return get_bridge().get_info()

def list_profiles(sketch_index=None):
    return get_bridge().list_profiles(sketch_index)


if __name__ == "__main__":
    # Example usage
    bridge = FusionBridge()

    print("Testing connection...")
    result = bridge.ping()
    print(f"Ping: {result}")

    if result.get("success"):
        print("\nCreating a box...")
        bridge.create_sketch("xy")
        bridge.draw_rectangle(0, 0, 4, 3)
        bridge.extrude(height=2)
        print("Done!")
