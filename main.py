import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from skimage.metrics import mean_squared_error, structural_similarity
import random
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

# Load the target grayscale image
target_image = Image.open('image/portrait1.jpg').convert('L')
target_array = np.array(target_image)

# Create a white canvas of the same dimensions
canvas = Image.new('L', target_image.size, color=255)
canvas_array = np.array(canvas)

def create_star(size):
    star = Image.new('L', (size, size), color=0)
    draw = ImageDraw.Draw(star)
    # Coordinates for a 5-pointed star
    points = [
        (size * 0.5, size * 0),
        (size * 0.61, size * 0.35),
        (size * 1, size * 0.35),
        (size * 0.68, size * 0.57),
        (size * 0.79, size * 0.91),
        (size * 0.5, size * 0.7),
        (size * 0.21, size * 0.91),
        (size * 0.32, size * 0.57),
        (size * 0, size * 0.35),
        (size * 0.39, size * 0.35)
    ]
    draw.polygon(points, fill=255)
    return star

def compute_mse(image1, image2):
    return mean_squared_error(image1, image2)

def compute_ssim(image1, image2):
    score, _ = structural_similarity(image1, image2, full=True)
    return score


def place_shape(canvas, shape, position, scale, rotation):
    shape_resized = shape.resize((int(shape.size[0]*scale), int(shape.size[1]*scale)), resample=Image.LANCZOS)
    shape_rotated = shape_resized.rotate(rotation, expand=True)
    shape_array = np.array(shape_rotated)

    # Calculate position to paste the shape
    x, y = position
    x -= shape_rotated.size[0] // 2
    y -= shape_rotated.size[1] // 2

    # Create a mask for the shape
    mask = shape_array > 0

    # Copy the canvas to avoid modifying the original
    new_canvas = canvas.copy()
    canvas_array = np.array(new_canvas)

    # Paste the shape onto the canvas
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(canvas_array.shape[1], x + shape_rotated.size[0]), min(canvas_array.shape[0], y + shape_rotated.size[1])

    shape_x1 = max(0, -x)
    shape_y1 = max(0, -y)
    shape_x2 = shape_x1 + x2 - x1
    shape_y2 = shape_y1 + y2 - y1

    canvas_array[y1:y2, x1:x2][mask[shape_y1:shape_y2, shape_x1:shape_x2]] = 0  # Black color

    return Image.fromarray(canvas_array)

def optimize_shape_placement(target_array, canvas, shape, max_shapes):
    placements = []
    current_canvas = canvas.copy()
    current_canvas_array = np.array(current_canvas)

    for i in tqdm(range(max_shapes)):
        best_score = float('inf')
        best_params = None

        # Smart initial placement strategy
        for _ in range(100):
            # Randomly choose parameters around the areas of highest difference
            diff = target_array - current_canvas_array
            y_indices, x_indices = np.where(diff > np.percentile(diff, 95))
            if len(x_indices) == 0 or len(y_indices) == 0:
                continue
            idx = random.randint(0, len(x_indices) - 1)
            x = x_indices[idx]
            y = y_indices[idx]
            scale = random.uniform(0.5, 1.5)
            rotation = random.uniform(0, 360)

            new_canvas = place_shape(current_canvas, shape, (x, y), scale, rotation)
            new_canvas_array = np.array(new_canvas)
            score = compute_mse(target_array, new_canvas_array)

            if score < best_score:
                best_score = score
                best_params = (x, y, scale, rotation)
                best_canvas = new_canvas

        if best_params:
            placements.append(best_params)
            current_canvas = best_canvas
            current_canvas_array = np.array(current_canvas)
        else:
            break  # No improvement found

    return current_canvas, placements

# Parameters
max_shapes = 100  # Adjust as needed
star_size = 50  # Initial size of the star

# Create the star shape
star_shape = create_star(star_size)

# Optimize
final_canvas, placements = optimize_shape_placement(target_array, canvas, star_shape, max_shapes)

fig, ax = plt.subplots()
images = []

current_canvas = canvas.copy()
for params in placements:
    x, y, scale, rotation = params
    current_canvas = place_shape(current_canvas, star_shape, (x, y), scale, rotation)
    img = plt.imshow(current_canvas, animated=True, cmap='gray')
    images.append([img])

ani = FuncAnimation(fig, lambda i: images[i], frames=len(images), interval=200, blit=True)
ani.save('recreation_animation.gif', writer='pillow')
plt.close()

# Display the Final Image
plt.imshow(final_canvas, cmap='gray')
plt.title('Recreated Image')
plt.axis('off')
plt.show()
