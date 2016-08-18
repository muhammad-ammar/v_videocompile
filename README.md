# ff_compiler
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

#### NOTE: Does not compile on Windows machines (poss. a later release)

This will check for an extant ffmpeg install, and install if the generalized shell command `ffmpeg` returns something that doesn't look like ffmpeg.

### Use

    from ffmpeg_compiler import FFInstall

    F = FFInstall(
        compile_dir=${optional directory}
        )
    F.run()

