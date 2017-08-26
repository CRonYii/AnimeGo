import urllib.request as ws
import urllib
import re,os,sys

home_url = 'https://acg.rip'
dir = 'E:/Eclipse workspace/AnimeGo/animego/torrent/'

def acess(keyword="",page=1):
    all = False
    if page == 0:
        all = True
        page = 1
    print('searching keyword: \'%s\' at page [%s]'%(keyword, page))
    url = home_url+'/page/%s?term=%s'%(page,urllib.parse.quote(keyword))
    request = ws.Request(url)
    response = ws.urlopen(request)
    html = str(response.read(),encoding='utf-8')
    analysis(html)
    if all == True:
        for pnum in range(2,getTotalPageNumber(html)+1):
            acess(keyword, pnum)
    
def analysis(html):
    print('Analyzing data, fetching available resources')
    resources = getResources(html)
    for i,r in enumerate(resources):
        info = analysisSingleResource(r)
        print(i+1,info)
        #downloadFile(info[1], info[3])
        #print(i,r)
    
def analysisSingleResource(text):
    pattern = re.compile('<span class="label label-team"><a href=".*">(.*?)</a></span>',re.RegexFlag.S)
    team = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<span class="title">.*?">(.*?)</a>.*?</span>',re.RegexFlag.S)
    title = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<td class="size">(.*?)</td>',re.RegexFlag.S)
    size = fetchFromList(re.findall(pattern, text))
    pattern = re.compile('<td class="action"><a href="(.*?)"><i class="fa fa-download"></i></a></td>',re.RegexFlag.S)
    torrent = home_url + fetchFromList(re.findall(pattern, text))
    return [team,title,size,torrent]
    
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
    totalPage = re.findall(pattern, html)[0]
    pattern = re.compile('<li><a href="/page/.*?">(.*?)</a></li>', re.RegexFlag.S)
    totalPage = re.findall(pattern, totalPage)[-1]
    return int(totalPage)
    
def commandResolve(s):
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
        acess(params['k'], int(params['p']))
    elif excute == 'exit':
        print('Programm Exit')
        sys.exit()
    
if __name__ == '__main__':
    #print(commandResolve('s k=haikyuu'))
    while 1:
        commandResolve(input('Input Command: '))
    print('end of programm')