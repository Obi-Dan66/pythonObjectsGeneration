import pyvista as pv
import numpy as np
from dotenv import load_dotenv
import os
import time
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cube_animation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_environment():
    """Load environment variables from .env file"""
    logging.info("Loading environment variables...")
    load_dotenv()
    env_vars = {
        'rotation_speed': float(os.getenv('ROTATION_SPEED', 45)),
        'rotation_axis': os.getenv('ROTATION_AXIS', 'y').lower(),
        'initial_angle': float(os.getenv('INITIAL_ANGLE', 0)),
        'target_angle': float(os.getenv('TARGET_ANGLE', 90)),
        'cube_size': float(os.getenv('CUBE_SIZE', 1.0)),
        'stop_at_target': os.getenv('STOP_AT_TARGET', 'true').lower() == 'true',
        'rotation_direction': float(os.getenv('ROTATION_DIRECTION', 1))
    }
    logging.info(f"Loaded environment variables: {env_vars}")
    return env_vars

def create_cube(size):
    """Create a cube with the specified size"""
    logging.info(f"Creating cube with size {size}")
    try:
        cube = pv.Box(bounds=(-size/2, size/2, -size/2, size/2, -size/2, size/2))
        logging.info("Cube created successfully")
        return cube
    except Exception as e:
        logging.error(f"Error creating cube: {e}")
        raise

def get_rotation_matrix(angle, axis):
    """Get rotation matrix for the specified angle and axis"""
    logging.debug(f"Calculating rotation matrix for angle {angle} around {axis} axis")
    rad_angle = np.radians(angle)
    if axis == 'x':
        return np.array([
            [1, 0, 0],
            [0, np.cos(rad_angle), -np.sin(rad_angle)],
            [0, np.sin(rad_angle), np.cos(rad_angle)]
        ])
    elif axis == 'y':
        return np.array([
            [np.cos(rad_angle), 0, np.sin(rad_angle)],
            [0, 1, 0],
            [-np.sin(rad_angle), 0, np.cos(rad_angle)]
        ])
    else:  # z-axis
        return np.array([
            [np.cos(rad_angle), -np.sin(rad_angle), 0],
            [np.sin(rad_angle), np.cos(rad_angle), 0],
            [0, 0, 1]
        ])

def main():
    try:
        logging.info("Starting cube animation program")
        
        # Load environment variables
        env = load_environment()
        
        logging.info("Setting up PyVista configuration")
        pv.OFF_SCREEN = False
        logging.info(f"PyVista version: {pv.__version__}")
        logging.info(f"Off-screen rendering: {pv.OFF_SCREEN}")
        
        # Create a plotter
        logging.info("Creating plotter")
        p = pv.Plotter()
        
        # Create the cube
        logging.info("Setting up cube")
        cube = create_cube(env['cube_size'])
        original_points = cube.points.copy()
        
        # Add the cube to plotter
        logging.info("Adding cube to plotter")
        actor = p.add_mesh(cube, color='blue', show_edges=True)
        
        # Set up the camera
        logging.info("Setting up camera")
        p.camera_position = 'iso'
        
        # Initialize rotation variables
        current_angle = env['initial_angle']
        rotation_step = (env['rotation_speed'] / 60.0) * env['rotation_direction']
        logging.info(f"Rotation step: {rotation_step} degrees per frame")

        # Start the plotter in non-blocking mode
        p.show(interactive=False, auto_close=False)
        
        logging.info("Starting animation")
        try:
            while True:
                # Update the rotation angle
                current_angle += rotation_step
                
                # Check if we've reached the target angle
                if env['stop_at_target']:
                    if (env['rotation_direction'] > 0 and current_angle >= env['target_angle']) or \
                       (env['rotation_direction'] < 0 and current_angle <= env['target_angle']):
                        current_angle = env['target_angle']
                        # Final update
                        rotation_matrix = get_rotation_matrix(current_angle, env['rotation_axis'])
                        cube.points = np.dot(original_points, rotation_matrix)
                        p.render()
                        break
                
                # Calculate rotation matrix and update cube
                rotation_matrix = get_rotation_matrix(rotation_step, env['rotation_axis'])
                cube.points = np.dot(cube.points, rotation_matrix)
                
                # Update the display
                p.render()
                
                # Control frame rate
                time.sleep(0.016)  # approximately 60 FPS
                
            # Keep the window open after animation
            logging.info("Animation complete, switching to interactive mode")
            p.show(interactive=True)
            
        except KeyboardInterrupt:
            logging.info("Animation interrupted by user")
            
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        logging.info("Cleaning up...")
        if 'p' in locals():
            p.close()
        logging.info("Program finished")

if __name__ == "__main__":
    main() 