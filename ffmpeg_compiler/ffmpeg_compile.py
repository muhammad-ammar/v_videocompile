
import os
import sys
import yaml
import subprocess

"""
Download and compile ffmpeg if absent / can run as part of test suite
or as part of setup. Will eventually live in separate repo.

"""
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'openveda'
    ))
from config import OVConfig
from reporting import ErrorObject



class FFCompiler():

    def __init__(self):

        self.complete = False

        self.FF_DIR = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'ffmpeg_build'
            )
        self.ff_repos = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'ffmpeg_repos.yaml'
            )
        self.repo_list = None
        self.ff_yaml = os.path.join(
            os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)
                )
            ), 
            'ffmpeg_binary.yaml'
            )
        CF = OVConfig()
        CF.run()
        self.settings = CF.settings_dict



    def check(self):
        """
        an attempt to submerge some of the process
        """
        try:
            self.settings['ffmpeg']
        except:
            return False
        process = subprocess.Popen(
            self.settings['ffmpeg'], 
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


    def run(self):
        if not os.path.exists(self.FF_DIR):
            os.mkdir(self.FF_DIR)

        # get info from yaml
        with open(self.ff_repos, 'r') as stream:
            try:
                self.repo_list = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise ErrorObject().print_error(
                    message='Invalid Config YAML'
                    )

        # run through and compile
        for library in self.repo_list:
            os.chdir(self.FF_DIR)
            for key, entry in library.iteritems():
                # clone
                os.system('%s %s' % ('git clone', entry['url']))
                os.chdir(entry['dir'])
                # config, make
                for c in entry['commands']:
                    self._EXEC(command=c)

                if key == 'ffmpeg':
                    self.FFM = os.path.join(
                        self.FF_DIR,
                        entry['dir'],
                        'ffmpeg'
                        )
                    self.FFP = os.path.join(
                        self.FF_DIR,
                        entry['dir'],
                        'ffprobe'
                        )

        self._GLOBALIZE()


    def _EXEC(self, command):
        """
        submerged output
        """
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            shell=True, 
            universal_newlines=True
            )
        while True:
            line = process.stdout.readline().strip()
            if line == '' and process.poll() is not None:
                break
            sys.stdout.write('\r')
            sys.stdout.write("%s" % (line.strip()))
            sys.stdout.flush()
        sys.stdout.write('')


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
    FF = FFCompiler()
    FF.check()
    print FF.check()

if __name__ == '__main__':
    sys.exit(main())


