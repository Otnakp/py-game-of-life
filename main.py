import time
import random
import argparse
import imageio
import numpy as np
from PIL import Image, ImageDraw

def parse_arguments():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument('--width', type=int, default=100, help='Width of the board')
    parser.add_argument('--height', type=int, default=100, help='Height of the board')
    parser.add_argument('--steps', type=int, default=1000, help='Number of steps to simulate')
    parser.add_argument('--scale', type=int, default=5, help='Scaling factor for the output video')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for initial board state')
    return parser.parse_args()

def create_board(height, width, seed=None):
    if seed is not None:
        random.seed(seed)

    board = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
    return board

def get_neighbors_count(board, x, y):
    height, width = len(board), len(board[0])
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    
    count = 0
    for nx, ny in neighbors:
        if 0 <= nx < width and 0 <= ny < height:
            count += board[ny][nx]
    return count

def update_board(board):
    height, width = len(board), len(board[0])
    new_board = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            neighbors_count = get_neighbors_count(board, x, y)

            if board[y][x] and neighbors_count in (2, 3):
                new_board[y][x] = 1
            elif not board[y][x] and neighbors_count == 3:
                new_board[y][x] = 1
            else:
                new_board[y][x] = 0

    return new_board

def board_to_image(board, scale):
    height, width = len(board), len(board[0])
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)

    for y in range(height):
        for x in range(width):
            if board[y][x]:
                draw.point((x, y), fill='white')

    # Scale the image
    img = img.resize((width * scale, height * scale), Image.NEAREST)

    return img

def main_loop(width, height, steps, scale):
    board = create_board(height, width)
    frames = []

    for _ in range(steps):
        frames.append(board_to_image(board, scale))
        board = update_board(board)
    
    return frames

def save_frames_to_video(frames, output_filename, fps=20):
    with imageio.get_writer(output_filename, fps=fps, codec='libx264', ffmpeg_params=['-preset', 'ultrafast', '-crf', '0']) as writer:
        for frame in frames:
            writer.append_data(np.array(frame))

if __name__ == "__main__":
    args = parse_arguments()
    width, height, steps, scale, seed = args.width, args.height, args.steps, args.scale, args.seed

    # Run the simulation
    frames = main_loop(width, height, steps, scale)

    # Save frames as MP4
    save_frames_to_video(frames, 'game_of_life.mp4', fps=20)
