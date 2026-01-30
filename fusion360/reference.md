# Fusion 360 Bridge API Reference

Complete reference for all available commands.

## Connection Commands

### ping
Test the bridge connection.
```json
{"id": 1, "action": "ping", "params": {}}
```

### message
Display a message box in Fusion 360.
```json
{"id": 2, "action": "message", "params": {"text": "Hello!"}}
```

---

## Session Export (Design Data)

### export_session
**Export complete design data to a timestamped session folder.**

This single command replaces all individual query commands. It exports everything the AI needs to understand the current design state.

```json
{"id": 3, "action": "export_session", "params": {}}
```

Optional parameters:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| name | string | "" | Custom session name suffix |

**Returns:**
```json
{
  "session_path": "/path/to/ClaudeBridge/sessions/2024-01-15_14-30-22",
  "session_name": "2024-01-15_14-30-22",
  "files": ["manifest.json", "design_info.json", ...],
  "summary": {"components": 1, "bodies": 2, "sketches": 3, ...}
}
```

**Exported Files:**

| File | Contents |
|------|----------|
| `manifest.json` | Session metadata, file list, summary counts |
| `design_info.json` | Design overview: components, bodies, sketches, features, parameters |
| `bodies.json` | Detailed body info: volume, area, face types, bounding box, circular edges |
| `features.json` | Timeline features with suppression status; **hole features include detailed parameters** |
| `parameters.json` | User parameters + model parameters (d1, d2, etc.) with source info |
| `construction_planes.json` | All construction planes |
| `sketches/overview.json` | Summary of all sketches with curve counts |
| `sketches/sketch_N.json` | Full geometry for sketch N (circles, lines, arcs, ellipses with coordinates) |

**Example Session Folder:**
```
sessions/2024-01-15_14-30-22/
  manifest.json
  design_info.json
  bodies.json
  features.json
  parameters.json
  construction_planes.json
  sketches/
    overview.json
    sketch_0.json
    sketch_1.json
```

**Workflow:**
1. Call `export_session` once to export all design data
2. Read the JSON files you need directly from the session folder
3. No need for multiple round-trip commands

**Hole Feature Details (in features.json):**

For features with `"type": "Hole"`, a `hole_details` object is included:
```json
{
  "name": "Hole5",
  "type": "Hole",
  "hole_details": {
    "hole_type": "simple",           // "simple", "counterbore", or "countersink"
    "diameter_cm": 0.3,              // Hole diameter in cm
    "tip_angle_deg": 118.0,          // Tip angle in degrees
    "tap_type": "none",              // "none", "tapped", or "clearance"
    "position": {"x": 1.5, "y": 2.0, "z": 0.5},  // Hole center position
    "direction": {"x": 0, "y": 0, "z": -1},      // Hole direction vector
    "side_face_count": 1,
    "end_face_count": 1,
    // For counterbore holes:
    "counterbore": {"depth_cm": 0.2, "diameter_cm": 0.5},
    // For countersink holes:
    "countersink": {"angle_deg": 82.0, "diameter_cm": 0.6},
    // For tapped holes:
    "thread": {"designation": "M3x0.5", "class": "6H", "is_modeled": false}
  }
}
```

---

## Construction Geometry

### create_offset_plane
Create a construction plane offset from a base plane. Essential for creating geometry at different Z heights.
```json
{"id": 10, "action": "create_offset_plane", "params": {
  "plane": "xy",
  "offset": 5.0
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane (`"xy"`, `"xz"`, `"yz"`) |
| offset | float | 1.0 | Distance in cm (positive = along normal) |
| name | string | auto | Optional custom name |

**Returns:** `plane_index` for use with `create_sketch`

### create_plane_at_angle
Create a construction plane at an angle from a base plane.
```json
{"id": 11, "action": "create_plane_at_angle", "params": {
  "plane": "xy",
  "axis": "x",
  "angle": 45
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane |
| axis | string | "x" | Rotation axis (`"x"`, `"y"`, `"z"`) |
| angle | float | 45 | Angle in degrees |
| name | string | auto | Optional custom name |

---

## Sketch Commands

### create_sketch
Create a new sketch on a construction plane or offset plane.
```json
{"id": 10, "action": "create_sketch", "params": {"plane": "xy"}}
```
**Or on an offset plane:**
```json
{"id": 11, "action": "create_sketch", "params": {"plane_index": 0}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| plane | string | "xy" | Base plane (`"xy"`, `"xz"`, `"yz"`) - used if plane_index not set |
| plane_index | int | null | Index of construction plane (from `create_offset_plane`) |

### create_sketch_on_face
Create a sketch on an existing body face. Useful for adding cuts or features to existing geometry.
```json
{"id": 12, "action": "create_sketch_on_face", "params": {
  "body_index": 0,
  "use_top_face": true
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| face_index | int | 0 | Which face (if use_top_face is false) |
| use_top_face | bool | false | Auto-find topmost planar face |

**Example workflow for cutting into top of a body:**
```json
// 1. Create sketch on top face
{"id": 1, "action": "create_sketch_on_face", "params": {"body_index": 0, "use_top_face": true}}
// 2. Draw shape to cut
{"id": 2, "action": "draw_circle", "params": {"x": 0, "y": 0, "radius": 1}}
// 3. Cut through body
{"id": 3, "action": "extrude", "params": {"height": -2, "operation": "cut"}}
```

### draw_circle
```json
{"id": 11, "action": "draw_circle", "params": {
  "sketch_index": 0, "x": 0, "y": 0, "radius": 2.5
}}
```

### draw_rectangle
```json
{"id": 12, "action": "draw_rectangle", "params": {
  "sketch_index": 0, "x": 0, "y": 0, "width": 4, "height": 3
}}
```

### draw_line
```json
{"id": 13, "action": "draw_line", "params": {
  "sketch_index": 0, "x1": 0, "y1": 0, "x2": 5, "y2": 3
}}
```

### draw_arc
Draw an arc defined by center, start point, and end point. Arc is drawn counter-clockwise from start to end.
```json
{"id": 14, "action": "draw_arc", "params": {
  "sketch_index": 0,
  "center_x": 0, "center_y": 0,
  "start_x": 2, "start_y": 0,
  "end_x": 0, "end_y": 2
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| center_x, center_y | float | 0, 0 | Center point |
| start_x, start_y | float | 1, 0 | Start point (defines radius) |
| end_x, end_y | float | 0, 1 | End point |

### draw_arc_three_points
Draw an arc passing through three points.
```json
{"id": 15, "action": "draw_arc_three_points", "params": {
  "sketch_index": 0,
  "start_x": 0, "start_y": 0,
  "mid_x": 1, "mid_y": 1,
  "end_x": 2, "end_y": 0
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| start_x, start_y | float | 0, 0 | Start point of arc |
| mid_x, mid_y | float | 0.5, 0.5 | Point along the arc (determines curvature) |
| end_x, end_y | float | 1, 0 | End point of arc |

### draw_arc_sweep
Draw an arc defined by center, start point, and sweep angle.
```json
{"id": 16, "action": "draw_arc_sweep", "params": {
  "sketch_index": 0,
  "center_x": 0, "center_y": 0,
  "start_x": 2, "start_y": 0,
  "sweep_angle": 90
}}
```

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| center_x, center_y | float | 0, 0 | Center point |
| start_x, start_y | float | 1, 0 | Start point (defines radius) |
| sweep_angle | float | 90 | Sweep angle in degrees (positive = counter-clockwise) |

**Arc Examples:**
```json
// Quarter circle (90°) - use draw_arc_sweep
{"id": 1, "action": "draw_arc_sweep", "params": {
  "center_x": 0, "center_y": 0, "start_x": 3, "start_y": 0, "sweep_angle": 90
}}

// Semicircle (180°)
{"id": 2, "action": "draw_arc_sweep", "params": {
  "center_x": 0, "center_y": 0, "start_x": 3, "start_y": 0, "sweep_angle": 180
}}

// Arc connecting two points with specific curvature - use draw_arc_three_points
{"id": 3, "action": "draw_arc_three_points", "params": {
  "start_x": -2, "start_y": 0, "mid_x": 0, "mid_y": 1.5, "end_x": 2, "end_y": 0
}}
```

### list_profiles
List profiles in a sketch (for extrusion).
```json
{"id": 10, "action": "list_profiles", "params": {"sketch_index": 0}}
```

---

## Text Commands

### draw_text
Draw text on a sketch. The text creates sketch curves that can be extruded.
```json
{"id": 30, "action": "draw_text", "params": {
  "sketch_index": 0,
  "text": "Hello",
  "x": 0,
  "y": 0,
  "height": 1.0,
  "font_name": "Arial"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Which sketch |
| text | string | required | Text string to draw |
| x | float | 0 | X position of text anchor |
| y | float | 0 | Y position of text anchor |
| height | float | 1.0 | Text height in cm |
| angle | float | 0 | Rotation angle in degrees |
| font_name | string | "Arial" | Font name |

### emboss_text
Emboss (raised) or deboss (cut) text on a body face. This convenience command creates a sketch on the face, adds text, and extrudes it.
```json
{"id": 31, "action": "emboss_text", "params": {
  "body_index": 0,
  "use_top_face": true,
  "text": "67 in",
  "height": 0.5,
  "depth": 0.05,
  "emboss": false
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| face_index | int | 0 | Which face (if use_top_face is false) |
| use_top_face | bool | false | Auto-find topmost planar face |
| text | string | required | Text string to emboss |
| x | float | 0 | X position relative to face |
| y | float | 0 | Y position relative to face |
| height | float | 1.0 | Text height in cm |
| depth | float | 0.1 | Extrusion depth in cm |
| emboss | bool | false | True for raised (emboss), False for cut (deboss) |
| font_name | string | "Arial" | Font name |

**Example: Label a board with its dimension**
```json
// Deboss "67 in" on top of body 1
{"id": 1, "action": "emboss_text", "params": {
  "body_index": 1,
  "use_top_face": true,
  "text": "67 in",
  "x": 2,
  "y": 0.5,
  "height": 0.8,
  "depth": 0.05,
  "emboss": false
}}
```

---

## Sketch Constraints

### add_constraint_midpoint
Constrain a point to the midpoint of a line. Commonly used to center geometry on the origin.
```json
{"id": 20, "action": "add_constraint_midpoint", "params": {
  "sketch_index": -1,
  "line_index": 0,
  "point": "origin"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | -1 (last) | Which sketch |
| line_index | int | 0 | Index of the line |
| point | string | "origin" | Currently only "origin" supported |

### add_constraint_coincident
Constrain a point to lie on a curve (line or circle).
```json
{"id": 21, "action": "add_constraint_coincident", "params": {
  "point_type": "line_endpoint",
  "point_source": {"line_index": 0, "endpoint": "end"},
  "target_type": "circle",
  "target_index": 0
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| point_type | string | "line_endpoint" | `"line_endpoint"` or `"circle_center"` |
| point_source | object | {} | `{line_index, endpoint}` or `{circle_index}` |
| target_type | string | "circle" | `"circle"` or `"line"` |
| target_index | int | 0 | Index of target curve |

### add_constraint_coincident_points
Constrain two line endpoints together (point-to-point).
```json
{"id": 22, "action": "add_constraint_coincident_points", "params": {
  "line1_index": 0, "line1_endpoint": "end",
  "line2_index": 1, "line2_endpoint": "start"
}}
```

### add_constraint_vertical
Make a line vertical.
```json
{"id": 23, "action": "add_constraint_vertical", "params": {"line_index": 0}}
```

### add_constraint_horizontal
Make a line horizontal.
```json
{"id": 24, "action": "add_constraint_horizontal", "params": {"line_index": 0}}
```

### get_sketch_constraints
List all geometric constraints in a sketch.
```json
{"id": 25, "action": "get_sketch_constraints", "params": {"sketch_index": -1}}
```

### delete_constraint
Delete a constraint by index.
```json
{"id": 26, "action": "delete_constraint", "params": {"constraint_index": 5}}
```

---

## 3D Operations

### extrude
Extrude a sketch profile.
```json
{"id": 14, "action": "extrude", "params": {
  "sketch_index": 0,
  "profile_index": 0,
  "height": 5,
  "operation": "new"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Sketch containing profile |
| profile_index | int | 0 | Which profile (use `list_profiles`) |
| height | float | 1 | Height in cm |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |

### revolve
Revolve a sketch profile around an axis to create rotational geometry.
```json
{"id": 15, "action": "revolve", "params": {
  "sketch_index": 0,
  "profile_index": 0,
  "axis": "x",
  "angle": 360,
  "operation": "new"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sketch_index | int | last | Sketch containing profile |
| profile_index | int | 0 | Which profile (use `list_profiles`) |
| axis | string | "x" | `"x"`, `"y"`, `"z"` for construction axes, or `"line"` for sketch line |
| axis_line_index | int | 0 | Index of sketch line to use as axis (when axis="line") |
| angle | float | 360 | Degrees to revolve (360 = full revolution) |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |

**Example: Create a sphere by revolving a semicircle**
```json
// 1. Create sketch on XZ plane
{"id": 1, "action": "create_sketch", "params": {"plane": "xz"}}
// 2. Draw a semicircle profile (half circle + line for axis)
// 3. Revolve around the line
{"id": 3, "action": "revolve", "params": {"axis": "line", "axis_line_index": 0}}
```

### loft
Create a smooth transition between two or more profiles (sketches at different positions).
```json
{"id": 16, "action": "loft", "params": {
  "sections": [
    {"sketch_index": 0, "profile_index": 0},
    {"sketch_index": 1, "profile_index": 0}
  ],
  "operation": "join"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sections | array | required | List of {sketch_index, profile_index} objects |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |
| is_solid | bool | true | Create solid (true) or surface (false) |
| is_closed | bool | false | Connect last section back to first |

**Example: Create curved transition between two shapes**
```json
// 1. Create sketch on bottom plane with shape A
{"id": 1, "action": "create_sketch", "params": {"plane": "xy"}}
{"id": 2, "action": "draw_rectangle", "params": {"width": 4, "height": 4}}
// 2. Create offset plane and sketch with shape B
{"id": 3, "action": "create_offset_plane", "params": {"plane": "xy", "offset": 5}}
{"id": 4, "action": "create_sketch", "params": {"plane_index": 0}}
{"id": 5, "action": "draw_circle", "params": {"radius": 2}}
// 3. Loft between them
{"id": 6, "action": "loft", "params": {
  "sections": [
    {"sketch_index": 0, "profile_index": 0},
    {"sketch_index": 1, "profile_index": 0}
  ]
}}
```

### loft_rails
Loft with guide rails for more controlled shape transitions.
```json
{"id": 17, "action": "loft_rails", "params": {
  "sections": [
    {"sketch_index": 0, "profile_index": 0},
    {"sketch_index": 1, "profile_index": 0}
  ],
  "rails": [
    {"sketch_index": 2, "curve_index": 0}
  ],
  "operation": "new"
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| sections | array | required | Same as loft |
| rails | array | [] | List of {sketch_index, curve_index} for guide curves |
| operation | string | "new" | `"new"`, `"join"`, `"cut"` |
| is_solid | bool | true | Create solid or surface |

### fillet
Round edges of a body.
```json
{"id": 15, "action": "fillet", "params": {
  "body_index": 0,
  "radius": 0.2,
  "edge_indices": [0, 1, 2]
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| radius | float | 0.1 | Fillet radius (cm) |
| edge_indices | array | all | Specific edges (or omit for all) |

### chamfer
Bevel edges of a body.
```json
{"id": 16, "action": "chamfer", "params": {
  "body_index": 0,
  "distance": 0.1,
  "edge_indices": [0, 1]
}}
```

### shell
Hollow out a body.
```json
{"id": 17, "action": "shell", "params": {
  "body_index": 0,
  "thickness": 0.2,
  "remove_top": true
}}
```
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| body_index | int | 0 | Which body |
| thickness | float | 0.1 | Wall thickness (cm) |
| face_index | int | null | Specific face to remove |
| remove_top | bool | true | Auto-find top face if face_index not set |

---

## Parameters

### set_parameter
Create or update a user parameter.
```json
{"id": 18, "action": "set_parameter", "params": {
  "name": "WallThickness",
  "value": 2,
  "unit": "mm"
}}
```

---

## Units

All dimensions are in **centimeters** (Fusion 360's internal unit):
- 1 cm = 10 mm
- For 50mm, use `5` (cm)
- For 2mm, use `0.2` (cm)

---

## Workflow: Understanding and Modifying a Design

1. **Export session data:**
   ```json
   {"id": 1, "action": "export_session", "params": {}}
   ```

2. **Read the exported files** from the session folder:
   - `design_info.json` for overview
   - `bodies.json` for detailed body geometry
   - `sketches/sketch_N.json` for specific sketch coordinates

3. **Make modifications:**
   - Add fillet/chamfer to existing bodies
   - Create new sketch and cut holes
   - Shell to hollow out
   - Add new features

4. **Export again** to verify changes:
   ```json
   {"id": 99, "action": "export_session", "params": {"name": "after_changes"}}
   ```

---

## File Paths

| File | Purpose |
|------|---------|
| `~/Documents/scripts/fusion_360/ClaudeBridge/commands.json` | Write commands |
| `~/Documents/scripts/fusion_360/ClaudeBridge/results.json` | Read results |
| `~/Documents/scripts/fusion_360/ClaudeBridge/sessions/` | Exported session data |
