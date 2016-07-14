
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
            # ))
from config import OVConfig
CF = OVConfig()
CF.run()
settings = CF.settings_dict

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


    def check(self):
        process = subprocess.Popen(
            settings['ffmpeg'], 
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
        # self.complete = self.check()

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


def main():
    FF = FFCompiler()
    FF.run()


if __name__ == '__main__':
    sys.exit(main())


