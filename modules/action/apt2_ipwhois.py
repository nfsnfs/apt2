import re
import sys
try:
    import ipwhois
except ImportError:
    raise ImportError('Missing ipwhois library. To install run: pip install ipwhois')

from core.actionModule import actionModule
from core.keystore import KeyStore as kb
from core.utils import Utils

class apt2_ipwhois(actionModule):
    def __init__(self, config, display, lock):
        super(apt2_ipwhois, self).__init__(config, display, lock)
        self.title = "run ipwhois"
        self.shortName = "IpWhois"
        self.description = "execute [ipwhois] on each target"

        self.types = ["osint"]

        self.requirements = []
        self.triggers = ["newHost"]

        self.safeLevel = 5

    def getTargets(self):
        self.targets = kb.get(['osint/host'])

    def process(self):
        # load any targets we are interested in
        self.getTargets()

        # loop over each target
        for t in self.targets:
            # verify we have not tested this host before
            if not self.seentarget(t):
                # add the to the already seen list
                self.addseentarget(t)
                # make outfile
                temp_file = self.config["proofsDir"] + self.shortName + "_" + t + "_" + Utils.getRandStr(10)
                obj=ipwhois.IPWhois(t)
                result = obj.lookup_rdap()
                Utils.writeFile(str(result), temp_file)
        return
