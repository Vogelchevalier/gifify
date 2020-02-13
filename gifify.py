#!/usr/bin/python

# TODO: non-square rectangle support
#   better gif quality
#   https://github.com/ImageOptim/gifski
#   https://ffmpeg.org/ffmpeg-filters.html#paletteuse

import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="A script for making .gif avatars from video files")

# File
parser.add_argument("--file", "--f",
                    required=True, type=str, help='The file you want to operate on.')

# Mode
parser.add_argument("--mode", "--m",
                    choices=["auto", "mp4", "cut", "crop", "resize", "gif"],
                    default="auto", type=str, help="Choose the mode.")

# Cut timestamp and duration
parser.add_argument("--timestamp", "--time", "--t",
                    default="00:00:00.0", type=str, help='The starting timestamp for mode "cut". hh:mm:ss.ds')
parser.add_argument("--duration", "--dur", "--d",
                    default="00:00:00.0", type=str, help='The duration for mode "crop". hh:mm:ss.ds')

# Crop coordinates and resolution
parser.add_argument("--startx", "--x",
                    default=0, type=int, help='The starting x coordinate for mode "crop".')
parser.add_argument("--starty", "--y",
                    default=0, type=int, help='The starting y coordinate for mode "crop".')
parser.add_argument("--resolution", "--res", "--r",
                    default=1, type=int, help='''The resolution for modes "crop" and "resize".
                                            It\'s a square, so 1 number is enough''')

args = parser.parse_args()

file = args.file
mode = args.mode
timestamp = args.timestamp
duration = args.duration
startx = args.startx
starty = args.starty
res = args.resolution

filename, filetype = os.path.splitext(file)


# Functions
def commandLine(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()
    print(process.returncode)


def askConfirmation():
    answer = input("##### File not .mp4, continue anyways? [y/N]: ")
    if answer == 'y' or answer == 'Y':
        return True
    else:
        return False


def makemp4(fname, ftype):
    if ftype != ".mkv" and ftype != ".mp4":
        answer = input("##### File not .mkv, continue anyways? [y/N]: ")
        if answer != 'y' and answer != 'Y':
            return
        else:
            ffmpeg = ['ffmpeg', '-i', f'{fname}{ftype}', '-an', f'{fname}.mp4']
            commandLine(ffmpeg)
            print(f"##### {fname}{ftype} ready")
            return

    if ftype != ".mp4":
        ffmpeg = ['ffmpeg', '-i', f'{fname}{ftype}', '-c', 'copy', '-an', f'{fname}.mp4']
        commandLine(ffmpeg)
        print(f"##### {fname}{ftype} ready")
    elif ftype == ".mp4":
        print("##### Input file already .mp4, exiting...")
        return


def cutVideo(fname, ftype, start, dur):
    if ftype != ".mp4":
        if not askConfirmation():
            return

    ffmpeg = ['ffmpeg', '-ss', start, '-i', f'{fname}{ftype}', '-c', 'copy', '-t', dur, f'{fname}-cut{ftype}']
    commandLine(ffmpeg)
    print("##### Video cut")


def cropVideo(fname, ftype, x, y, reso):
    if ftype != ".mp4":
        if not askConfirmation():
            return

    ffmpeg = ['ffmpeg', '-i', f'{fname}{ftype}', '-filter:v', f'crop={reso}:{reso}:{x}:{y}',
              f'{fname}-crop{ftype}']
    commandLine(ffmpeg)
    print("##### Video cropped")


def resizeVideo(fname, ftype, reso):
    if ftype != ".mp4":
        if not askConfirmation():
            return

    ffmpeg = ['ffmpeg', '-i', f'{fname}{ftype}', '-vf', f'scale={reso}x{reso}:flags=lanczos',
              f'{fname}-resize{ftype}']
    commandLine(ffmpeg)
    print("##### Video resized")


def makeGif(fname, ftype):
    if ftype == ".gif":
        print("##### Input file already .gif, exiting...")
        return
    elif ftype != ".mp4":
        if not askConfirmation():
            return

    ffmpeg = ['ffmpeg', '-i', f'{fname}{ftype}', '-lavfi',
              'palettegen=stats_mode=single[pal],[0:v][pal]paletteuse=new=1',
              '-loop', '0', f'{fname}.gif']
    commandLine(ffmpeg)
    print(f"##### {fname}{ftype} ready")


def autoMode(fname, ftype):
    files_to_cleanup = []

    begin = input(f'##### File {fname}{ftype} selected. Continue? [Y/n]: ')

    if begin == "n" or begin == "N":
        return

    if ftype != ".mp4":
        print("##### Creating an .mp4 [ctrl + c to quit]")
        makemp4(fname, ftype)
        ftype = ".mp4"
        files_to_cleanup.append(f'{fname}{ftype}')

    print("##### Cutting [ctrl + c to quit]")
    print(f'##### File {fname}{ftype} selected')

    start_time = input("##### At what timestamp do you want to start the gif [hh:mm:ss.ds]: ")
    clip_duration = input("##### How long do you want the gif to be [hh:mm:ss.ds]: ")

    cutVideo(fname, ftype, start_time, clip_duration)
    fname = f'{fname}-cut'
    files_to_cleanup.append(f'{fname}{ftype}')

    print("##### Cropping [ctrl + c to quit]")
    print(f'##### File {fname}{ftype} selected')

    x = input("##### X coordinate you want the area to start from: ")
    y = input("##### Y coordinate you want the area to start from: ")
    reso = input("##### Length of the side of the square in pixels: ")

    cropVideo(fname, ftype, x, y, reso)
    fname = f'{fname}-crop'
    files_to_cleanup.append(f'{fname}{ftype}')

    print("##### Resizing [ctrl + c to quit]")
    print(f'##### File {fname}{ftype} selected')

    print("##### Length of the resized side of the square in pixels.")
    resized_reso = input("##### Leave empty (press enter) for no resizing: ")

    if resized_reso:
        resizeVideo(fname, ftype, resized_reso)
        fname = f'{fname}-resize'
        files_to_cleanup.append(f'{fname}{ftype}')
    else:
        print("##### No resizing done!")

    print("##### Creating a .gif [ctrl + c to quit]")
    print(f'##### File {fname}{ftype} selected')

    makeGif(fname, ftype)
    ftype = ".gif"
    print(f'##### Created {fname}{ftype}')

    cleanup = input("##### Clean up extra files? Leaves the original video and the gif. [y/N]: ")

    if cleanup == "y" or cleanup == "Y":
        for i in range(len(files_to_cleanup)):
            os.remove(files_to_cleanup[i])
            print(f'##### Removed {files_to_cleanup[i]}')
    else:
        print("##### No files removed")


# if elif else to choose the right function for the mode
if mode == 'mp4':
    makemp4(filename, filetype)
elif mode == 'cut':
    cutVideo(filename, filetype, timestamp, duration)
elif mode == 'crop':
    cropVideo(filename, filetype, startx, starty, res)
elif mode == 'resize':
    resizeVideo(filename, filetype, res)
elif mode == 'gif':
    makeGif(filename, filetype)
else:
    autoMode(filename, filetype)
