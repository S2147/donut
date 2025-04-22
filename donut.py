import math
import os
import time

A, B = 0, 0  # Rotation angles

def render_frame():
    global A, B
    screen_width = 80
    screen_height = 40
    screen = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]  # Screen buffer
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]  # Depth buffer
    R1 = 1  # Inner radius of the donut
    R2 = 2  # Outer radius of the donut
    K1 = 5  # Distance between the viewer and the donut
    K2 = 15  # Projection scale factor

    # Loop through theta and phi (angles that describe the surface of the torus)
    for theta in range(0, 628, 7):  # Theta from 0 to 2*pi, step size ~0.01 radians
        costheta = math.cos(theta / 100)
        sintheta = math.sin(theta / 100)
        for phi in range(0, 628, 2):  # Phi from 0 to 2*pi, step size ~0.02 radians
            cosphi = math.cos(phi / 100)
            sinphi = math.sin(phi / 100)

            # 3D coordinates of the donut surface before rotation
            circlex = R2 + R1 * costheta  # X coordinate of the circle in 3D space
            circley = R1 * sintheta       # Y coordinate of the circle in 3D space

            # 3D rotation of the point around the X and Z axes
            x = circlex * (math.cos(B) * cosphi + math.sin(A) * math.sin(B) * sinphi) - circley * math.cos(A) * math.sin(B)
            y = circlex * (math.sin(B) * cosphi - math.sin(A) * math.cos(B) * sinphi) + circley * math.cos(A) * math.cos(B)
            z = K1 + math.cos(A) * circlex * sinphi + math.sin(A) * circley  # Add K1 to avoid negative depth

            ooz = 1 / z  # Perspective scaling factor

            # 2D projection of the 3D point
            xp = int(screen_width / 2 + K2 * ooz * x)
            yp = int(screen_height / 2 - K2 * ooz * y)

            # Calculate luminance (brightness) based on the surface normal
            luminance_index = int(8 * (cosphi * costheta - sinphi * sintheta))

            # Ensure the projected point is within the screen boundaries
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if ooz > zbuffer[yp][xp]:  # Only draw if this point is closer to the viewer
                    zbuffer[yp][xp] = ooz
                    screen[yp][xp] = '.,-~:;=!*#$@'[luminance_index % 12]  # ASCII shading

    # Clear the screen and print the frame
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal
    for line in screen:
        print(''.join(line))

    A += 0.04  # Slowly rotate around X-axis
    B += 0.02  # Slowly rotate around Z-axis

if __name__ == '__main__':
    while True:
        render_frame()
        time.sleep(0.03)  # Control the rotation speed
