# gifify
Python script for creating .gifs from video files using ffmpeg

## Requirements
- python >= 3.6
- ffmpeg

## How to use
- Download
- (Optional) `chmod +x gifify.py`
- (Optional) Move the script to a location that is in your PATH variable
- Run the .py file or run `gifify --file <path>` if you did the optional steps

## Flags
- `--file --f <path>` Select the file to operate on
- `--mode --m <auto|mp4|cut|crop|resize|gif>` Select the mode. Default `auto`

###### Optional flags for the non-auto modes
- `--timestamp --time --t <hh:mm:ss.ds>` The starting timestamp for mode `cut` in ffmpeg format
- `--duration --dur --d <hh:mm:ss.ds>` The duration for mode `cut` in ffmpeg format
- `--startx --x <number>` The starting x coordinate for mode `crop` in pixels
- `--starty --y <number>` The starting y coordinate for mode `crop` in pixels
- `--resolution --res --r <number>` The length of the side of the square for modes `crop` and `resize`. Support for non-square rectangles planned.
