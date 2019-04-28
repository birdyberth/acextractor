from nltk import word_tokenize
import subprocess
from collections import Counter
from operator import itemgetter

def parsexml(filename):
    print("Extraction des commentaires du fichier xml...")
    f = open(filename,'r')
    rawdata = f.readlines()
    f.close()
    longueur = len(rawdata)
    #longueur = 100
    listcom=[]
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
            
            entry = {'name':name,'userurl':userurl,'videourl':videourl,'comment':comment}
            listcom.append(entry)
        if i % 100e3 == 0:
            print(i,"commentaires ouverts")
    
    return(listcom)

def wordalizer(entry):
    comment = entry['comment'] #Va chercher le texte du commentaire
    acfound = False
    ACindex = 0
    #Mettre aussi un détecteur de caps pour les émotions
    #Trouver une façon de retirer les doublons
    #Trouver une façon de cliquer sur la vidéo et que ça retrouve le commentaire
    tkcom = word_tokenize(comment.lower()) #Prend les commentaires, les mets en lowercase, sort des tokens de mots 
    n = len(tkcom)
    if n > 0:    
        wc = Counter(tkcom) #compte le nombre de chaque mot du dictionnaire dans le commentaire
        nbofI = wc['i']+wc['me']+wc['my']+wc['mine']+wc['myself']+wc['im']+wc['ive']
        nbofIT = wc['it']+wc['itself']+wc['its']+wc['this']+wc['these']+wc['that']+wc['those']
        nbofWE = wc['we']+wc['us']+wc['our']+wc['ourselves']
        nbofTHEY = wc['you']+wc['your']+wc['yours']+wc['yourself']+wc['yourselves']+wc['he']+wc['him']+wc['his']+wc['himself']+wc['she']+wc['her']+wc['hers']+wc['herself']+wc['they']+wc['them']+wc['their']+wc['theirs']+wc['themselves']
        nbofpunc = wc['.']+wc[',']
        nbofexc = wc['!']+wc['?']
        nbofIFTHEN = wc['if']+wc['then']
        spectrum = [nbofI/n,nbofIT/n,nbofWE/n,nbofTHEY/n,nbofpunc/n,nbofexc/n,nbofIFTHEN/n]
        if spectrum[0] > 0 :
            ACindex = (spectrum[1]+spectrum[2]+spectrum[3]+spectrum[6])/spectrum[0]
            if ACindex >= 1:
                acfound = True
    return(ACindex)

def htmlout(filtcom):
    f = open('commentaires_tries.html','w')
    f.write('<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8">\n<style>\ntable, th, td {\n    border: 1px solid black;\n}\n</style>\n</head>\n<body>\n\n<table>\n  <tr>\n    <th>Nom</th>\n    <th>Commentaire</th>\n  </tr>\n')
    for entry in filtcom:
        f.write('  <tr>\n    <td><a href=')
        f.write(entry['userurl'])
        f.write(' target=_blank>')
        f.write(entry['name'])
        f.write('</a>\n')
        f.write(str(round(entry['acindex'])))
        f.write('\n<a href=')
        f.write(entry['videourl'])
        f.write(' target=_blank>vidéo</a></td>\n    <td>')
        f.write(entry['comment'])
        f.write('</td>\n  </tr>')
    
    f.write('</table>\n\n</body>\n</html>')
    f.close()

    subprocess.run(["firefox","commentaires_tries.html"]) #Part firefox automatiquement pour afficher les commentaires trouvés
            
            
if __name__ == "__main__":
    listcom = parsexml('ytcomments/ytcomments1nov2017.xml')
    print("Calcul de l'indice AC pour chaque commentaire...")
    filtcom=[]
    i = 1
    for entry in listcom:
        acindex = wordalizer(entry)
        if acindex >= 10:
            entry['acindex']=acindex
            filtcom.append(entry)
        if i % 1e3 == 0:
            print(i,"commentaires analysés")
        i = i + 1
    print("Tri des commenatires selon l'indice AC...")
    sortedcom = sorted(filtcom, key=itemgetter('acindex'), reverse=True) #Filtre les commentaires dans l'ordre du plus "AC" au moins
    out=[]
    lentry = {}
    llentry = {}
    lllentry = {}
    for entry in sortedcom: #Retire les doublons
        if (entry != lentry) and (entry != llentry) and (entry != lllentry):
          out.append(entry)
        lllentry = llentry
        llentry = lentry
        lentry = entry
        
    htmlout(out)



