# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 19:28:11 2022

@author: viter

This is a converter that receives as input a ".bbl" file (produced by a Overleaf or other 
Latex tool) and produces as output an ".html" file, in which the references of a paper are
represented in html format, ready to be included in the OJS system.

"""


def limpa_latex(linha):
    linha = linha.replace('{\\c{c}}', 'ç')
    linha = linha.replace('{\\~\\a}', 'ã')
    linha = linha.replace('{\\~\\o}', 'õ')
    linha = linha.replace('{\\~\\n}', 'ñ')
    linha = linha.replace('{\\\'\\a}', 'á')
    linha = linha.replace('{\\\'\\e}', 'é')
    linha = linha.replace('{\\\'\\i}', 'í')
    linha = linha.replace('{\\\'\\o}', 'ó')
    linha = linha.replace('{\\\'\\u}', 'ú')
    linha = linha.replace('{\\^\\a}', 'â')
    linha = linha.replace('{\\^\\e}', 'ê')
    linha = linha.replace('{\\`\\a}', 'à')
    linha = linha.replace('{\\~a}', 'ã')
    linha = linha.replace('{\\~o}', 'õ')
    linha = linha.replace('{\\~n}', 'ñ')
    linha = linha.replace('{\\\'a}', 'á')
    linha = linha.replace('{\\\'e}', 'é')
    linha = linha.replace('{\\\'i}', 'í')
    linha = linha.replace('{\\\'o}', 'ó')
    linha = linha.replace('{\\\'u}', 'ú')
    linha = linha.replace('{\\\'n}', 'ń')
    linha = linha.replace('{\\^a}', 'â')
    linha = linha.replace('{\\^e}', 'ê')
    linha = linha.replace('{\\`a}', 'à')
    linha = linha.replace('{\\\"a}', 'ä')
    linha = linha.replace('{\\\"o}', 'ö')
    linha = linha.replace('{\\\"u}', 'ü')
    linha = linha.replace('~', ' ')
    linha = linha.replace('--', '-')
    linha = linha.replace('{\\_}', '_')
    linha = linha.replace('\\_', '_')
    linha = linha.replace('\&', '&')
    return linha

def limpa_href(linha):
    if '\\href' in linha:
        novalinha = ''
        k = linha.rfind("\\href")
        achou = False
        for i in range(len(linha)):
            if i < k or achou == True:
                novalinha = novalinha + linha[i]
            else:
                if linha[i] == '}':
                    achou = True
        return novalinha
    else:
        return linha

def limpa_url(linha):
    if '\\url' in linha:
        link = ''
        novalinha = ''
        k = linha.rfind("\\url")
        achou = False
        for i in range(len(linha)):
            if i < k:
                novalinha = novalinha + linha[i]
            elif i > k+4:
                if linha[i] == '}' and achou == False:
                    novalinha = novalinha + '[<a href=\"' + link + '\">link</a>]'
                    achou = True
                elif achou == False:
                    link = link + linha[i]
                else:
                    novalinha = novalinha + linha[i]
        novalinha = novalinha.replace('Available at:{[', 'Available online {[')
        novalinha = novalinha.replace('Available at: {[', 'Available online {[')
        return novalinha
    else:
        return linha

def formata_latex(linha):
    novalinha = ''
    pilha = 0
    skip = 0
    for i in range(len(linha)):
        if skip > 0:
            skip = skip - 1
        elif linha[i] =='{':
            if linha[i+1:].startswith('\\em '):
                novalinha = novalinha + '<i>'
                skip = 4
            else:
                pilha = pilha + 1
        elif linha[i] == '}':
            if pilha == 0:
                novalinha = novalinha + '</i>'
            else:
                pilha = pilha - 1
        else:
            novalinha = novalinha + linha[i]
    return novalinha

def linka_doi(linha):
    if 'DOI' in linha:
        novalinha = ''
        skip = 0
        achou = False
        for i in range(len(linha)):
            if skip > 0:
                skip = skip - 1
            elif linha[i+1:].startswith('DOI: '): 
                achou = True
                skip = 5
            elif skip == 0 and achou == True:
                doistr = linha[i:-2] 
                novalinha = novalinha + '<a href=\"https://doi.org/' + doistr + '\">'
                achou = False
            novalinha = novalinha + linha[i]
        novalinha = novalinha[:-2] + '</a>.\n'
        return novalinha
    else:
        return linha

refs_vet = []


infile = input("Type input file name: ")

if not infile.endswith(".bbl"):
    print("File type should be \".bbl\"")
    raise SystemExit
    
outfile = 'output-' + infile[:-4] + '.html'

fin = open(infile, "r", encoding = "utf-8")

fout = open(outfile, "w", encoding = "utf-8")

if fin != None:
    print("Loaded file "+ infile)  
else:
    print("\nInput file not found\n\n")
    raise SystemExit

k = 0
newit = 0
newitem = ''
for linha in fin:
    if linha =='\n':
        newitem = limpa_latex(newitem)
        newitem = limpa_href(newitem)
        newitem = limpa_url(newitem)
        newitem = formata_latex(newitem)
        newitem = linka_doi(newitem)
        refs_vet.append(newitem)
        newit = 0
    elif linha.startswith('\\bibitem'):
        newit = 1
        k = k + 1
        newitem = ''
    elif newit == 1:
        if linha.startswith('\\newblock'):
            newitem = newitem.replace('\n', '') + ' ' + linha.replace('\\newblock ', '')
        elif linha.startswith('  '):
            newitem = newitem.replace('\n', '') + ' ' + linha.lstrip()
        else:
            newitem = linha
            
for ref in refs_vet:
    #print(ref)
    fout.write(ref)
            
fout.close

print("Output written to " + outfile)