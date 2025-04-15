# 3D Cube Generator

A Python script that generates and rotates a 3D cube using PyVista.

## Setup

1. Create and activate a virtual environment:

For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

For Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust the parameters:
- `ROTATION_SPEED`: Speed of rotation in degrees per second (default: 30)
- `ROTATION_AXIS`: Axis of rotation ('x', 'y', or 'z') (default: 'x')
- `INITIAL_ANGLE`: Starting angle in degrees (default: 0)
- `CUBE_SIZE`: Size of the cube (default: 1.0)

## Usage

Run the script:
```bash
python cube_generator.py
```

The script will display a 3D cube that rotates continuously. You can:
- Rotate the view by dragging with the left mouse button
- Zoom in/out with the right mouse button
- Pan by dragging with the middle mouse button
- Close the window to stop the animation

## Deactivating Virtual Environment

When you're done, you can deactivate the virtual environment:
```bash
deactivate
```