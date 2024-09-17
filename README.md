# Grayscale Photo Recreation Using Shapes

This Python project recreates a given grayscale photo using simple black shapes on a white canvas. The goal is to place and adjust these shapes (scaling, rotating, and positioning) to achieve maximum similarity to the original photo while minimizing the number of shapes used. This project demonstrates an iterative approach to gradually improve the resemblance between the canvas and the target photo.

## Features

- Recreate grayscale images using a single type of shape (star) on a white canvas.
- Shapes can be scaled, rotated, and positioned to fit the image.
- Smart initial placement of shapes to enhance optimization.
- Modular design for easy replacement of similarity metrics and optimization methods.
- Outputs a recreated image and an animation showing the iterative shape placement process.

## Requirements

- Python 3.x
- Required libraries (see [Installation](#installation))

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/grayscale-photo-recreation.git
cd grayscale-photo-recreation
pip install -r requirements.txt
```

## Usage

Prepare Input: Provide a grayscale image as the target photo.

Run the Program:

```bash
python recreate_photo.py --input path/to/your/grayscale_image.png --max_shapes 100
```

--input: Path to the grayscale image.
--max_shapes: The maximum number of shapes allowed for recreating the photo.
Output:

The recreated grayscale image saved to the output directory.
An animation showing the shapes being added one by one to the canvas.
Example
Here's an example of how to run the program:

```bash
python recreate_photo.py --input images/sample.png --max_shapes 100
```

The program will output:

A recreated image as output/recreated_image.png.
An animation as output/shape_animation.gif.

## How It Works

Input Handling: The program takes a grayscale image and initializes a white canvas of the same dimensions.
Shape Placement: It uses an optimization method (e.g., genetic algorithm, simulated annealing) to iteratively place shapes on the canvas. The shapes are adjusted in scale, rotation, and position to best match the target image.
Optimization: The similarity between the recreated image and the target photo is maximized using a chosen similarity metric (e.g., Mean Squared Error, Structural Similarity Index). The modular design allows for easy swapping of both the metric and the optimization method.
Output: The program generates the final recreated image and an animation showing the iterative process.

## Configuration

Similarity Metric: The similarity metric can be changed by modifying the evaluate_similarity function in utils.py.
Optimization Method: To use a different optimization method, adjust the optimize_shapes function in optimizer.py.

## Future Improvements

Support for multiple shape types (e.g., circles, squares).
Improved performance for high-resolution images.
Addition of a GUI for easier interaction.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or feedback, please contact me.
