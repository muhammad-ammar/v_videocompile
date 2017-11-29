
import os
import sys
import yaml
import subprocess
import platform
import shutil

from os.path import expanduser
home = expanduser("~")

"""
Download and compile ffmpeg if absent, including
dependencies

--optimized for edX VEDA instances/subsidiaries, but 
could be expanded to include other use cases

"""

class InstallError(Exception):
    """
    An error that occurs during ffmpeg install.
    """
    pass


class VideoCompile():

    def __init__(self, **kwargs):

        self.debug = kwargs.get('debug', True)
        self.compile_dir = kwargs.get(
            'compile_dir', 
                os.path.join(
                home,
                'ffmpeg_sources'
                )
            )

        self.build_repos = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)
                )),
            'build_repos.yaml'
            )
        self.build_list = None


    def run(self):
        """
        NOTE:
        I was unable to get this to work politely with a variety of 
        systems with any reliability, so I might back off

        old run (manual compile) is 'run()'
        new run (less good, more polite) is drun()
        """
        if os.path.exists(self.compile_dir):
            shutil.rmtree(self.compile_dir)

        os.mkdir(self.compile_dir)

        if self.check() is True:
            return None

        """
        Run through compilation steps
        """
        if self.prepare() is False:
            print '[ERROR] : FFmpeg install...\
                Visit https://ffmpeg.org for instructions'
            return None

        self.buildout()
        print '%s : %s' % (
            'ffmpeg/ffprobe installed', self.check()
            )
        if self.check() is True:
            print '%s : %s' % (
                'ffmpeg/ffprobe installed', self.check()
                )
            return None

        """
        failover to polite compile
        """
        self.polite_buildout()
        print '%s : %s' % (
            'ffmpeg/ffprobe installed', self.check()
            )


    def drun(self):
        if self.check() is True:
            print '%s : %s' % (
                'ffmpeg/ffprobe installed', self.check()
                )
            return None

        """
        Run through compilation steps
        """
        if self.prepare() is False:
            print '[ERROR] : FFmpeg install...\
                Visit https://ffmpeg.org for instructions'
            raise InstallError('ffmpeg installation failed')

        self.polite_buildout()
        print '%s : %s' % ('ffmpeg/ffprobe installed', self.check())


    def check(self):
        """
        is ffmpeg already installed?
        (submerged process)
        """
        process = subprocess.Popen(
            'ffmpeg', 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            shell=True, 
            universal_newlines=True
            )

        for line in iter(process.stdout.readline, b''):
            if 'ffmpeg version' in line:
                return True
            if 'ffmpeg: command not found' in line:
                return False
        return False


    def prepare(self):

        if not os.path.exists(self.build_repos):
            print '[ERROR] : no build yaml'
            return None

        """
        This should cascade down until it gets a hit 
        through ubuntu, centos, and finally osx
        """
        if platform.system() == 'Linux':
            if platform.linux_distribution()[0] == 'Ubuntu':
                return self.ubuntu_prep()
            else:
                return self.centos_prep()
        elif platform.system() == 'Darwin':
            return self.darwin_prep()
        else:
            """
            Build out further platform extensability
            """
            return False

    def ubuntu_prep(self):
        x = os.system(
            'sudo apt-get install -y yasm autoconf automake \
            build-essential libass-dev libfreetype6-dev \
            libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev \
            libvorbis-dev libxcb1-dev libxcb-shm0-dev \
            libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev \
            libvpx3 libvpx-dev' #libvorbis libogg'
            )

        if x > 0:
            return False
        return True

    def centos_prep(self):
        x = os.system(
            'sudo yum -y install yasm autoconf automake cmake \
            freetype-devel gcc gcc-c++ git libtool make \
            mercurial nasm pkgconfig zlib-devel \
            libvpx' # libvorbis libogg'
            )
        if x > 0:
            return False
        return True

    def darwin_prep(self):
        """
        NOTE: I couldn't get this to work with anything other
        than brew -- in the interests of getting to done, and as 
        one probably shouldn't be running this on a darwin machine
        in production, I left it.

        ALSO NOTE:
        there's a brew command to install ffmpeg -- so feel free to 
        use that (it's in polite_buildout()):

            '''
            brew install ffmpeg --with-fdk-aac --with-ffplay \
            --with-freetype --with-libass --with-libquvi \
            --with-libvorbis --with-libvpx --with-opus --with-x265
            '''
        """
        x = os.system('brew info')
        if x > 0:
            x = os.system(
                'ruby -e \"$(curl -fsSL \
                https://raw.githubusercontent.com/Homebrew/install/master/install)\"'
            )
                
        if x == 0:
            x = os.system(
                'brew install -y automake yasm fdk-aac git lame\
                libass libtool opus sdl shtool texi2html\
                theora wget x264 xvid  \
                libvpx' # libvorbis libogg'
                )

        return True


    def buildout(self):
        with open(self.build_repos, 'r') as stream:
            try:
                self.build_list = yaml.load(stream)
            except yaml.YAMLError as exc:
                print 'YAML Build error'
                return None
        # run through and compile
        for library in self.build_list:
            self.run_compile(library=library)


    def run_compile(self, library):
        """
        reset to start
        """
        os.chdir(self.compile_dir)

        """
        run dependency builds
        """
        for key, entry in library.iteritems():
            print key
            '''
            clone 
            -or- 
            curl & expand
            '''
            if 'curl' in entry['url']:
                os.system(entry['url'])
                self._EXEC(command=entry['unpack'])

            else:
                # if platform.system() != 'Linux':
                os.system('%s %s' % ('git clone', entry['url']))
                # else:
                    # os.system('%s %s' % ('sudo git clone', entry['url']))

            if not os.path.exists(
                os.path.join(self.compile_dir, entry['dir'])
                ):
                print '[ERROR] : expansion problem'
                return None

            """
            compile dependency
            """
            os.chdir(entry['dir'])
            for c in entry['commands']:
                print '***********'
                print c
                print '***********'
                self._EXEC(command=c)


    def _EXEC(self, command):
        if self.debug is True:
            os.system(command)
        else:
            """
            submerged/oneline output
            """
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True, 
                universal_newlines=True
                )

            """
            show process wheel
            """
            wheel = {0: '|', 1: '/', 2: '-', 3: '\\'}
            x = 0
            for line in iter(process.stdout.readline, b''):
                sys.stdout.write('\r')
                sys.stdout.flush()
                sys.stdout.write("%s : %s" % ('Buildout', wheel[x]))
                x += 1
                if x == 4:
                    x = 0

            sys.stdout.write('\n')


    def polite_buildout(self):
        """
        This should act as a temporary failsafe. 
        I don't love the dependencies here, but this will get the node up
        :::
        """

        if platform.system() == 'Linux':
            if not os.path.exists(self.compile_dir):
                os.mkdir(self.compile_dir)
            os.chdir(self.compile_dir)
            os.system(
                'wget \
                    http://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz'
                )
            os.system('tar -xf ffmpeg-release-64bit-static.tar.xz')

            for f in os.listdir(self.compile_dir):
                if os.path.isdir(os.path.join(self.compile_dir, f)):
                    ff_build = os.path.join(self.compile_dir, f, 'ffmpeg')
                    probe_build = os.path.join(self.compile_dir, f, 'ffprobe')
                else:
                    os.remove(f)

            os.system(' '.join((
                'sudo ln -s',
                ff_build,
                '/usr/bin/ffmpeg'
                )))
            os.system(' '.join((
                'sudo ln -s',
                probe_build,
                '/usr/bin/ffprobe'
                )))

        elif platform.system() == 'Darwin':
            os.system(
                'brew install ffmpeg --with-fdk-aac --with-ffplay \
                    --with-freetype --with-libass --with-libquvi \
                    --with-libvorbis --with-libvpx --with-opus --with-x265'
                )
            os.system('brew link --overwrite ffmpeg')


def main():
    pass


if __name__ == '__main__':
    sys.exit(main())


