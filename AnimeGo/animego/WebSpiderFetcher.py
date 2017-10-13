# -*- coding: utf-8 -*-

import urllib.request as ws
import urllib
import re,os,sys

home_url = 'https://acg.rip'
dir = 'E:/Python/AnimeGo/Animego/animego/torrent/'

def acess(keyword="",page=1):
    '''
     - params - 
    keyword: str
    page: int
     - return -

    '''
    #print('searching keyword: \'%s\' at page [%s]'%(keyword, page))
    url = home_url+'/page/%s?term=%s'%(page,urllib.parse.quote(keyword))
    request = ws.Request(url)
    response = ws.urlopen(request)
    html = str(response.read(),encoding='utf-8')
    return analyze(html), getTotalPageNumber(html)

def analyze(html):
    itemList = []
    resources = getResources(html)
    for i,r in enumerate(resources):
        info = analyzeSingleResource(r)
        #info.insert(0,i+1)
        itemList.append(info)
        #print(i+1,info)
        #downloadFile(info[2], info[4])
        #print(i,r)
    return itemList
    
def analyzeSingleResource(text):
    pattern = re.compile('<span class="label label-team"><a href=".*">(.*?)</a></span>',re.RegexFlag.S)
    team = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<span class="title">.*?">(.*?)</a>.*?</span>',re.RegexFlag.S)
    title = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<td class="size">(.*?)</td>',re.RegexFlag.S)
    size = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<div class="done"><span class=".*?">(.*?)</span>',re.RegexFlag.S)
    peers = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<td class="action"><a href="(.*?)"><i class="fa fa-download"></i></a></td>',re.RegexFlag.S)
    torrent = home_url + fetchFromList(re.findall(pattern, text))
    return [peers,team,title,size,torrent]
    
def getResources(html):
    pattern = re.compile('</thead>\n(.*)</table>',re.RegexFlag.S)
    result = re.findall(pattern, html)[0]
    pattern = re.compile('<tr>(.*?)</tr>',re.RegexFlag.S)
    result = re.findall(pattern, result)
    return result
        
def downloadFile(name,url):
    f = ws.urlopen(url)
    data = f.read()
    with open(dir+name+'.torrent', "wb") as code:
        code.write(data)
        code.close()
    
def fetchFromList(o):
    if len(o) == 0:
        o = "None"
    else:
        o = o[0]
    return o

def getTotalPageNumber(html):
    pattern = re.compile('<a rel="next" href="(.*?)</a></li> <li class="next">', re.RegexFlag.S)
    result = re.findall(pattern, html)

    if len(result) == 0: #Return 1 if Page bar is not Found
        return -1; 
    ''' some bugs occur and I use another tricky way to do this, but still keep the original code just in case some problem occur
    totalPage = result[0]
    print(totalPage)
    pattern = re.compile('<li><a href="/page/.*?">(.*?)</a></li>', re.RegexFlag.S)
    totalPage = re.findall(pattern, totalPage)[-1]
    '''
    totalPage = result[0].split('>')[-1]
    return int(totalPage)
    
def commandResolve(s):
    '''
    use ',' to serperate commands
    s,k='death note',p=0
    s: search - k: keyword - p: page number
    dl: download
    exit: exit the programm
    '''
    cmds = s.split(',')
    excute = cmds[0]
    if excute not in ['s','dl','exit']:
        print('invalid command')
        return
    params = {'k':'','p':1}
    for param in cmds[1:]:
        p = param.split('=')
        if len(p) != 2: return
        var = p[0]
        value = p[1]
        params[var] = value
    if excute == 's':
        print(acess(params['k'], int(params['p'])))
    elif excute == 'exit':
        print('Programm Exit')
        sys.exit()
    
if __name__ == '__main__':
    while 1:
        commandResolve(input('Input Command: '))
    print('end of programm')