# Fusion 360 Bridge Examples

Complete workflow examples for common tasks.

## Example 1: Create a Simple Box

A 4cm × 3cm × 2cm box.

### Step 1: Create sketch on XY plane

```json
{"id": 1, "action": "create_sketch", "params": {"plane": "xy"}}
```

### Step 2: Draw rectangle

```json
{"id": 2, "action": "draw_rectangle", "params": {"x": 0, "y": 0, "width": 4, "height": 3}}
```

### Step 3: Extrude to 2cm height

```json
{"id": 3, "action": "extrude", "params": {"sketch_index": 0, "profile_index": 0, "height": 2}}
```

---

## Example 2: Create a Cylinder with Hole

A cylinder with a center hole (like a washer).

### Step 1: Create sketch

```json
{"id": 1, "action": "create_sketch", "params": {"plane": "xy"}}
```

### Step 2: Draw outer circle (radius 3cm)

```json
{"id": 2, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 3}}
```

### Step 3: Draw inner circle (radius 1cm)

```json
{"id": 3, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 1}}
```

### Step 4: Check profiles

```json
{"id": 4, "action": "list_profiles", "params": {"sketch_index": 0}}
```

Response will show 2 profiles:
- Profile 0: The inner circle (smaller area)
- Profile 1: The ring between circles (larger area)

### Step 5: Extrude the ring (profile 1)

```json
{"id": 5, "action": "extrude", "params": {"sketch_index": 0, "profile_index": 1, "height": 1}}
```

---

## Example 3: Create an L-Bracket

An L-shaped bracket using two rectangles.

### Step 1: Create sketch

```json
{"id": 1, "action": "create_sketch", "params": {"plane": "xy"}}
```

### Step 2: Draw vertical part

```json
{"id": 2, "action": "draw_rectangle", "params": {"x": 0, "y": 0, "width": 1, "height": 5}}
```

### Step 3: Draw horizontal part (overlapping)

```json
{"id": 3, "action": "draw_rectangle", "params": {"x": 0, "y": 0, "width": 4, "height": 1}}
```

### Step 4: Check profiles (the L-shape should be one profile)

```json
{"id": 4, "action": "list_profiles", "params": {"sketch_index": 0}}
```

### Step 5: Extrude

```json
{"id": 5, "action": "extrude", "params": {"sketch_index": 0, "profile_index": 0, "height": 1}}
```

---

## Example 4: Stacked Objects (Multiple Extrudes)

Create a stepped cylinder.

### Step 1: Create first sketch and circle

```json
{"id": 1, "action": "create_sketch", "params": {"plane": "xy"}}
```

```json
{"id": 2, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 3}}
```

### Step 2: Extrude base (5cm)

```json
{"id": 3, "action": "extrude", "params": {"sketch_index": 0, "profile_index": 0, "height": 5}}
```

### Step 3: Get design info to find top face

```json
{"id": 4, "action": "get_info", "params": {}}
```

### Step 4: Create new sketch (on XY plane, but offset would need scripting)

For stacking, create a new sketch with a smaller circle:

```json
{"id": 5, "action": "create_sketch", "params": {"plane": "xy"}}
```

```json
{"id": 6, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 2}}
```

### Step 5: Extrude with join operation

```json
{"id": 7, "action": "extrude", "params": {"sketch_index": 1, "profile_index": 0, "height": 8, "operation": "join"}}
```

---

## Example 5: Cut a Hole

Cut a circular hole through an existing body.

### Assuming a box already exists from Example 1...

### Step 1: Create sketch on XY plane

```json
{"id": 10, "action": "create_sketch", "params": {"plane": "xy"}}
```

### Step 2: Draw circle for hole

```json
{"id": 11, "action": "draw_circle", "params": {"x": 2, "y": 1.5, "radius": 0.5}}
```

### Step 3: Extrude with cut operation

```json
{"id": 12, "action": "extrude", "params": {"sketch_index": 1, "profile_index": 0, "height": 5, "operation": "cut"}}
```

---

## Command Sequence Template

Use this pattern for reliable command execution:

```python
import json

BRIDGE_DIR = "<ClaudeBridge-directory>"  # Set to your ClaudeBridge add-in path

def send_command(cmd_id, action, params={}):
    cmd = {"id": cmd_id, "action": action, "params": params}
    with open(f"{BRIDGE_DIR}/commands.json", "w") as f:
        json.dump(cmd, f)
    with open(f"{BRIDGE_DIR}/results.json", "r") as f:
        return json.load(f)
```

---

## Tips for Complex Models

1. **Plan your sketches** - Each closed shape becomes a profile
2. **Use overlapping rectangles** for complex 2D shapes
3. **Check profiles** with `list_profiles` before extruding
4. **Use "join"** to add to existing bodies
5. **Use "cut"** to subtract from existing bodies
6. **Work in centimeters** - multiply mm by 0.1
