import os
import time
import subprocess

if __name__ == '__main__':
    from build import build
    build()

class build:
    def __init__(self):
        self._pwd = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + '/..')
        self.build()

    def build(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+============================+")
        print("|          LICENSER          |")
        print("+============================+")
        start_time = time.time()
        self.__clean()
        os.makedirs('{}/dist'.format(self._pwd), exist_ok=True)
        subprocess.call("docker pull nginx:alpine", shell=True)
        subprocess.call("cd {} ; docker build -t meteor2-license:latest -f build/Dockerfile .".format(self._pwd), shell=True)
        subprocess.call("docker rmi nginx:alpine", shell=True)
        subprocess.call("docker save meteor2-license | gzip > {}/dist/meteor2-license.tar.gz".format(self._pwd), shell=True)
        self.__clean()

        print("\n- Build Path: {}/dist/meteor2-license.tar.gz".format(self._pwd))
        print("- Overall Time: {}".format(time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))))

    ####################
    # Internal Methods #
    ####################
    def __clean(self):
        subprocess.call("docker kill $(docker ps -a -q --filter ancestor=meteor2-license) >/dev/null 2>&1", shell=True)
        subprocess.call("docker rm $(docker ps -a -q --filter ancestor=meteor2-license) >/dev/null 2>&1", shell=True)
        subprocess.call("docker rmi meteor2-license:latest >/dev/null 2>&1", shell=True)
