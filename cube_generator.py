import pyvista as pv
import numpy as np
from dotenv import load_dotenv
import os
import time

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        'rotation_speed': float(os.getenv('ROTATION_SPEED', 30)),
        'rotation_axis': os.getenv('ROTATION_AXIS', 'x').lower(),
        'initial_angle': float(os.getenv('INITIAL_ANGLE', 0)),
        'cube_size': float(os.getenv('CUBE_SIZE', 1.0))
    }

def create_cube(size):
    """Create a cube with the specified size"""
    # Create a simple cube using Box instead of Cube
    return pv.Box(bounds=(-size/2, size/2, -size/2, size/2, -size/2, size/2))

def main():
    # Load environment variables
    env = load_environment()
    
    # Create a plotter
    plotter = pv.Plotter(off_screen=False)
    
    # Create the cube
    cube = create_cube(env['cube_size'])
    
    # Add the cube to the plotter
    plotter.add_mesh(cube, color='blue', show_edges=True)
    
    # Set up the camera
    plotter.camera_position = 'iso'
    
    # Initial angle
    angle = env['initial_angle']
    
    # Show the plotter in interactive mode
    plotter.show(interactive=True)
    
    # Rotation loop
    while True:
        # Update the rotation angle
        angle += env['rotation_speed'] * 0.016  # 0.016 is approximately 1/60 second
        
        # Create rotation matrix based on the specified axis
        if env['rotation_axis'] == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))]
            ])
        elif env['rotation_axis'] == 'y':
            rotation_matrix = np.array([
                [np.cos(np.radians(angle)), 0, np.sin(np.radians(angle))],
                [0, 1, 0],
                [-np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))]
            ])
        else:  # z-axis
            rotation_matrix = np.array([
                [np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0],
                [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0],
                [0, 0, 1]
            ])
        
        # Apply rotation to the cube
        cube.points = np.dot(cube.points, rotation_matrix)
        
        # Update the plotter
        plotter.render()
        time.sleep(0.016)  # Approximately 60 FPS

if __name__ == "__main__":
    main() 