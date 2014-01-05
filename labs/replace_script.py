import sys

if (len(sys.argv) > 1):
    for i in range(len(sys.argv) - 1):
        doc_arg = sys.argv[i+1]
        f=open(doc_arg,'r+')
        doc = ""
        for line in f.readlines():
            doc = doc + "\n" + line.replace('src="/bjc-r','src="http://bjc.berkeley.edu/bjc-r')
        g=open("new_" + doc_arg,'w')
        g.write(doc)

else:
    print("Error: script must take in at least one argument file")



