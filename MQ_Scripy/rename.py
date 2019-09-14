import os
# path=os.getcwd()+'\\github\\logExtract\\data\\log'
path = r"C:\Users\xinhuizx\logExtract\data\log"
for parent, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename.find('.log')!=-1:
            newName =parent.split('\\')[-1]+filename
            #print(newName)
            os.rename(os.path.join(parent, filename), os.path.join(parent, newName))
print("rename ok!")
