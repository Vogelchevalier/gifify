# gifify
Python script for creating .gifs from video files using ffmpeg

## Requirements
- python >= 3.6
- ffmpeg

## How to use
- Download
- Run the .py file

## Flags
- `--file <path>` Select the file to operate on
- `--mode <auto|mp4|cut|crop|resize|gif>` Select the mode. Default `auto`

###### Optional flags for the non-auto modes
- `--timestamp <hh:mm:ss.ds>` The starting timestamp for mode `cut` in ffmpeg format
- `--duration <hh:mm:ss.ds>` The duration for mode `cut` in ffmpeg format
- `--startx <number>` The starting x coordinate for mode `crop` in pixels
- `--starty <number>` The starting y coordinate for mode `crop` in pixels
- `--resolution <number>` The length of the side of the square for modes `crop` and `resize`. Alias `--res`. Support for non-square rectangles planned.
