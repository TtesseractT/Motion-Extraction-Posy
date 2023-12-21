""" Built by Tesseract: Sabian.H """
# MIT LICENCE 
'''
This script allows you to control various parameters of the motion trail effect:

input: Path to the input video file.
--blend_mode: Blend mode for the tblend filter (default is 'average').
--frame_step: Number of frames to skip for the motion trail (default is 2).
--pts_multiplier: Multiplier for adjusting the playback speed (default is 0.5).
--opacity: Opacity of the motion trail video (default is 0.5).

'''

import argparse
import subprocess
import os


""" USAGE:
python fstract.py input_video.mp4 --blend_mode average --frame_step 2 --pts_multiplier 0.5 --opacity 0.5

"""

def process_video(args):
    # Extract base name without extension
    base_name = os.path.splitext(os.path.basename(args.input))[0]

    # Construct output filename
    output_file = f'{base_name}_motion_trail.mp4'
    
    # Filename for the motion trail video
    motion_trail_video = "Temp_File_MT.mp4"

    # Apply motion trail effect and invert colors
    blend_filter = f"tblend={args.blend_mode},framestep={args.frame_step},setpts={args.pts_multiplier}*PTS,negate"
    subprocess.run([
        "ffmpeg", "-i", args.input, "-vf", blend_filter, motion_trail_video
    ], check=True)

    # Set opacity of the motion trail video to the specified value and overlay it with the original video
    overlay_filter = f"[1]format=rgba,colorchannelmixer=aa={args.opacity}[motion];[0][motion]overlay"
    subprocess.run([
        "ffmpeg", "-i", args.input, "-i", motion_trail_video, "-filter_complex", overlay_filter, output_file
    ], check=True)

    # Cleanup: Remove the motion trail video file
    os.remove(motion_trail_video)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Process video to create a motion trail effect.")
    parser.add_argument("input", help="Path to the input video file.")
    parser.add_argument("--blend_mode", default="average", help="Blend mode for tblend filter. Default is 'average'.")
    parser.add_argument("--frame_step", type=int, default=2, help="Frame step for creating motion trail. Default is 2.")
    parser.add_argument("--pts_multiplier", type=float, default=0.5, help="Multiplier for setpts filter. Default is 0.5.")
    parser.add_argument("--opacity", type=float, default=0.5, help="Opacity for the motion trail video. Default is 0.5.")

    args = parser.parse_args()

    try:
        output = process_video(args)
        print(f"Processed video saved as: {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
