
import os
import sys
import yaml
import subprocess
import platform
import shutil

"""
Download and compile ffmpeg if absent, including
dependencies

--optimized for edX VEDA instances/subsidiaries, but 
could be expanded to include other use cases

"""


class VideoCompile():

    def __init__(self, **kwargs):

        self.complete = False

        self.compile_dir = kwargs.get(
            'compile_dir', 
            os.path.join(
                os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__)
                    )),
                'ffmpeg'
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
            'apt-get install -y install autoconf automake \
            build-essential libass-dev libfreetype6-dev \
            libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev \
            libvorbis-dev libxcb1-dev libxcb-shm0-dev \
            libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev'
            )
        if x > 0:
            return False
        return True

    def centos_prep(self):
        x = os.system(
            'yum install -y autoconf automake cmake \
            freetype-devel gcc gcc-c++ git libtheora-dev libtool make \
            mercurial nasm pkgconfig zlib-devel libXext-devel \
            libXfixes-devel x264-devel zlib-devel'
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
        use that:

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
                'brew install -y  automake fdk-aac git lame\
                libass libtool libvorbis libvpx opus sdl shtool texi2html\
                theora wget x264 xvid yasm'
                )

        return True


    def buildout(self):
        
        if os.path.exists(self.compile_dir):
            shutil.rmtree(self.compile_dir)
            # os.mkdir(self.compile_dir)
        # else:
        os.mkdir(self.compile_dir)

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
                os.system('%s %s' % ('git clone', entry['url']))

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
                self._EXEC(command=c)


    def _EXEC(self, command):
        """
        submerged/oneline output
        """
        if platform.system() == 'Linux':
            command = 'sudo ' + command

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
            print line.replace('\n', '')

            # sys.stdout.write('\r')
            # sys.stdout.flush()
            # sys.stdout.write("%s : %s" % ('Buildout', wheel[x]))
            # x += 1
            # if x == 4:
            #     x = 0

        sys.stdout.write('\n')


def main():
    pass

if __name__ == '__main__':
    sys.exit(main())


