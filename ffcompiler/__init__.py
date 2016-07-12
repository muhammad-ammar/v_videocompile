
import os
import sys
import urllib2
import yaml
import subprocess

"""
This will read a default yaml file and output to a instance-specific file, 
to be read by processes as needed

"""


class FFInstall():
    """
    I couldn't get this to run reliably in testing, so I bruted it
    """
    """
    Should drop a compiled version of ffmpeg into this without too much hassle *
    * Ha, I've been having some issues getting this to work reliably, 
    so I've hopped through some hoops to get this to work.
    
    Will download and build ffmpeg, latest version (as of 07.2016)
    and run as a binary

    """
    def __init__(self, pkg_url):
        self.pkg_url = pkg_url

        self.FFM = None
        self.FFP = None
        #----
        self.FF_DIR = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'ENCODE_LIB'
            )
        self.ff_yaml = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'ffmpeg_binary.yaml'
            )


    def run(self):
        if not os.path.exists(self.FF_DIR):
            os.mkdir(self.FF_DIR)
        
        self._PREP()
        self._EXEC("""cd %s/ffmpeg-3.1.1
            ./configure \
                --enable-gpl --enable-nonfree \
                --disable-ffserver \
                --disable-shared --enable-static \
                --enable-libx264 --enable-libmp3lame --enable-pthreads
            make
        """ % (self.FF_DIR))
        self._CONNECT()
        self._GLOBALIZE()


    def check(self):
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
            return False


    def _PREP(self):
        pkg_name = os.path.basename(urllib2.urlparse.urlparse(self.pkg_url).path)
        pkg_fpath = os.path.join(self.FF_DIR, pkg_name)
        tmp_fpath = os.path.join(self.FF_DIR, pkg_name + ".downloading")

        with open(tmp_fpath, "wb") as f:
            print "downloading %s from %s" % (pkg_name, self.pkg_url)
            f.write(urllib2.urlopen(self.pkg_url).read())
            os.rename(tmp_fpath, pkg_fpath)

        if pkg_name.endswith(".tar.bz2"):
            print "extracting %s" % pkg_name
            self._EXEC("cd '%s' ; tar xjf %s" % (self.FF_DIR, pkg_name))

        if pkg_name.endswith(".tar.gz"):
            print "extracting %s" % pkg_name
            self._EXEC("cd '%s' ; tar xzf %s" % (self.FF_DIR, pkg_name))


    def _EXEC(self, command):
        print "[cmd] %s" % command
        os.system(command)


    def _CONNECT(self):
        """
        walk through dirs
        """
        for f in os.listdir(self.FF_DIR):
            if os.path.isfile(os.path.join(self.FF_DIR, f)):
                os.remove(os.path.join(self.FF_DIR, f))
            if os.path.isdir(os.path.join(self.FF_DIR, f)):
                self.FFM = os.path.join(self.FF_DIR, f, 'ffmpeg')
                self.FFP = os.path.join(self.FF_DIR, f, 'ffprobe')

    def _GLOBALIZE(self):
        ffdict = {
            'ffmpeg' : self.FFM,
            'ffprobe' : self.FFP
            }
        with open(self.ff_yaml, 'w') as outfile:
            outfile.write(
                yaml.dump(
                    ffdict, 
                    default_flow_style=False
                    )
                )



def main():
    # TODO: move to yaml, change to class activate
    install_dict = {
        "http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz": 'yasm-1.2.0',
        "ftp://ftp.videolan.org/pub/x264/snapshots/x264-snapshot-20120302-2245-stable.tar.bz2" : 'x264-snapshot-20120302-2245-stable',
        "http://downloads.sourceforge.net/lame/lame-3.99.5.tar.gz" : 'lame-3.99.5',
        }

    for key, entry in install_dict.iteritems():
        F1 = FFInstall(
            pkg_url=key
            )
        if F1.check() False:
            F1._PREP()
            F1._EXEC("""cd %s/%s
                ./configure
            """ % (F1.FF_DIR, entry))

    F4 = FFInstall(
        pkg_url="http://ffmpeg.org/releases/ffmpeg-3.1.1.tar.bz2"
        )

    if F4.check() is False:
        F4.run()


if __name__ == '__main__':
    sys.exit(main())

