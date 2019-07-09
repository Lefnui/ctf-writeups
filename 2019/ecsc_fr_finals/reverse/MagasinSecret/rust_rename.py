#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

import re
import subprocess

from ghidra.program.model.symbol import SourceType

def getDemangled(name):
  p = subprocess.Popen(["C:/Users/ida/Documents/demangler/target/release/demangler.exe", name], stdout=subprocess.PIPE)
  p.wait()
  return p.stdout.read().strip()
 
functions = currentProgram.getListing().getFunctions(False)
for func in functions:
  name = func.getName()
  demangled = getDemangled(name)
  if name != demangled: #Has been demangled
    demangled = re.sub("::h[0-9a-f]{16}$", "", demangled)
    func.setName(demangled.replace(" ", ""), SourceType.USER_DEFINED)
