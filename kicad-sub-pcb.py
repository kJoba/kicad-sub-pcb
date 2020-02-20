import os, re, sys

def main(argv):
	# check input
	if len(argv) < 1 or len(argv[0]) < 5 or argv[0][-4:] != ".sch":
		print("wrong or no input file")
		sys.exit(1)
	# make sure there is also a PCB file for this schematic
	try:
		with open(argv[0][:-4]+'.kicad_pcb', "r") as fobj:
			# read whole file for later clone and replacements
			pcb = fobj.read()
	except IOError:
		print("could not read pcb file: ", argv[0][:-4]+'.kicad_pcb')
		sys.exit(1)
	# open schematic
	try:
		with open(argv[0], "r") as fobj:
			schematic = fobj.read()
		# try to extract different sub-schematic paths
		uniquePaths = list(set(re.findall(r'AR Path="[^"]*\/([^"\/]*)\/[^"\/]*" Ref="[^"]*[^\?]"', schematic)))
		# get highest match counts of each path
		maxComps = 0
		for path in uniquePaths:
			l = len(re.findall(r'AR Path="[^"]*\/'+path+'\/[^"\/]*" Ref="[^"]*[^\?]"', schematic))
			if l > maxComps:
				maxComps = l
		#make the paths unique
		uniquePaths[:] = [path for path in uniquePaths if len(re.findall(r'AR Path="[^"]*\/'+path+'\/[^"\/]*" Ref="[^"]*[^\?]"', schematic)) == maxComps]
		replacements = {}
		# create search and replace array
		for path in uniquePaths:
			replacements[path] = re.findall(r'\$Comp\r?\n(?:(?:[^\$]|\$[^E]|\$E[^n]|\$En[^d]|\$End[^C]|\$EndC[^o]|\$EndCo[^m]|\$EndCom[^p]|\$EndComp[^\r\n]).*\r?\n)*AR Path="[^"]*\/'+path+'\/[^"\/]*" Ref="([^"]*[^\?])".*\r?\n(?:(?:[^F]|F[^ ]|F [^0]|F 0[^ ]).*\r?\n)*F 0 "([^"]+)"', schematic)
		# makedir for cloned pcbs
		try:
			os.makedirs(argv[0][:-4]+'.kicad_pcbs')
		except FileExistsError:
			pass
		# clone PCB for each extracted path
		for path in uniquePaths:
			try:
				with open(argv[0][:-4]+'.kicad_pcbs/'+path+'.kicad_pcb', "w") as fobj:
					# replace path and reference in cloned PCB
					newPcb = pcb.replace('    (path /', '    (path /'+path+'/')
					for repl in replacements[path]:
						newPcb = newPcb.replace('    (fp_text reference '+repl[1]+' ', '    (fp_text reference '+repl[0]+' ')
					fobj.write(newPcb)
			except IOError:
				print("failed to write pcb file: ", path+'.kicad_pcb')
				sys.exit(1)
		os.system("pause")
		sys.exit()
	except IOError:
		print("could not read schematic file: ", argv[0])
		sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])