# V_Videocompile
Master repo to compile ffmpeg for veda & veda subsidiaries

## Intro
There wasn't a good, universal *nix solution to compiling ffmpeg on various
node, ingest, and worker machines, so I made this. It's simple, ugly, and should
work for most local and AWS instances, assuming you're running a *nix machine.

This won't get you a full-flavored version of ffmpeg, this is just for what we use 
(and might use later) at edX. You'll get mp3, mp4, and theora, as well as the 
basic HLS encoder. 

If you're interested in ffmpeg, and want something that's a little more functional
for general and workaday use, allow me to recommend:  https://trac.ffmpeg.org/wiki/CompilationGuide

#### NOTE: 'Impolite' full compilation isn't currently working with terraform - though the script will run if run manually (go figure). 
#### So I've backed off into a 'polite' build, using a (known, tested) static build for EC2 instances and a brew-based install for Darwin machines

This will check for an extant ffmpeg install, and install if the global command `ffmpeg` returns something that doesn't look like ffmpeg.

### Use (for compile) <--currently in bin

    from v_videocompile import VideoCompile

    F = VideoCompile(
        compile_dir=${optional directory}
        )
    F.drun()


### Use (for impolite compile)

    from v_videocompile import VideoCompile

    F = VideoCompile(
        compile_dir=${optional directory}
        )
    F.run()


This software uses code of FFmpeg licensed under the LGPLv2.1 and its source can be
downloaded here:
    http://ffmpeg.org/releases/ffmpeg-3.1.1.tar.bz2

#### NOTE: Does not compile on Windows machines (poss. a later release)

08.2016/@yro