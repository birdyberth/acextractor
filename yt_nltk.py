from nltk import word_tokenize
import subprocess

f = open('ytcomments/ytcomments1nov2017.xml','r')
rawdata = f.readlines()
f.close()
longueur = len(rawdata)
f = open('commentaires_tries.html','w')
f.write('<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8">\n<style>\ntable, th, td {\n    border: 1px solid black;\n}\n</style>\n</head>\n<body>\n\n<table>\n  <tr>\n    <th>Nom</th>\n    <th>Commentaire</th>\n  </tr>\n')

nb_com = 0
for i in range(0, longueur):
    line = rawdata[i]
    if line[0:7] == "<video>":
        videourl = line[12:55]
        
    if line[0:6] == "<name>":
        [b, reste] = line.split("<name>")
        [name, reste] = reste.split("</name>")
        [b, reste] = reste.split("<userurl>")
        [userurl, reste] = reste.split("</userurl>")
        [b, reste] = reste.split("<comment>")
        try:
            [comment, b] = reste.split("</comment>")
        except:
            j=1
            while True:
                try:
                    [lastpart, b] = rawdata[i+j].split("</comment>")
                    break
                except:
                    j=j+1
            comment = reste
            for k in range(1,j-1):
                comment = comment + rawdata[i+k]
            comment = comment + lastpart
            
        q = comment.find("?")
        if q >= 0:
            if len(comment) >= 50:
                #print comment.decode('utf-8')
                #print "-------------------------------------"
                f.write('  <tr>\n    <td><a href=')
                f.write(userurl)
                f.write(' target=_blank>')
                f.write(name)
                f.write('</a>\n<a href=')
                f.write(videourl)
                f.write(' target=_blank>')
                f.write(videourl)
                f.write('</a></td>\n    <td>')
                f.write(comment)
                f.write('</td>\n  </tr>')
                nb_com = nb_com + 1
            
f.write('</table>\n\n</body>\n</html>')
f.close()

if nb_com:
    subprocess.run(["firefox","commentaires_tries.html"])



