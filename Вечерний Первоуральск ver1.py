import urllib.request as ur, re, os, time, html.parser

def download_page(pageUrl):
    time.sleep(2)
    try:
        page = ur.urlopen(pageUrl)
        text = page.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
        text = ''
    return text

def neat_text(text):
    text=re.findall('<div class="b-block-text__text">(.+?)</div>', text, flags=re.DOTALL)
    text=''.join(text)
    return text
    

def author(text):
    try:
        author_name=re.search('<span class="b-object__detail__author__name">(.+?)</span>', text, flags=re.DOTALL)
        author_name=author_name.group(1)
    except:
        author_name='NoName'      
    return author_name

def article(text):
    try:
        article_name =re.search('<meta name="title" content="(.+?)"/>', text, flags=re.DOTALL)
        article_name=article_name.group(1)
    except:
        article_name='NoArticleName'
    return article_name

def date(text):
    try:
        date_name =re.search('<span class="date">(\d{2}\.\d{2}\.\d{4})</span>', text, flags=re.DOTALL)
        date_name=date_name.group(1)
    except:
        date_name='NoDate'
    return date_name

def category(text):
    category_name = re.findall('<a href="/article/\?category=.+?">(.+?)</a>', text, flags=re.DOTALL)
    category_name = ' '.join(category_name)
    if category_name == ' ':
      category_name='NoCategory'
    return category_name

def cleaning(text):
    regTag = re.compile('<.*?>',flags = re.U|re.DOTALL)
    regScript = re.compile('<script>.*?</script>',flags = re.U|re.DOTALL) 
    regComment = re.compile('<!--.*?-->', flags = re.U|re.DOTALL)
    regAd = re.compile('http://.+?/', flags = re.U|re.DOTALL) 
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t=regAd.sub("", clean_t)
    clean_t=html.parser.HTMLParser().unescape(clean_t)
    return clean_t

def files(i):
    if not os.path.exists("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\plain\\" + year + "\\" + month):
        os.makedirs("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\plain\\"+ year + "\\" + month )
    file = open("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\plain\\"+ year + "\\" + month + "\\"+ str(i) + ".txt", "w", encoding="utf-8")
    file.write("@au " + author_name + "\n" + "@ti " + article_name + "\n"  + "@da " +date_name +"\n" + "@topic " + category_name +"\n" + "@url " + pageUrl + "\n" +final)
    file.close()

def meta_data():
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tгородская\t%s\t"Вечерний Первоуральск"\t\t%s\tгазета\tРоссия\tСвердловская Область\tru'
    string = (row % (path, author_name, article_name, date_name, category_name, pageUrl, year))
    file = open("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\meta_data.сsv", "a", encoding="utf-8")
    file.write(string + "\n")
    file.close()
    
def mystem1():
     if not os.path.exists ("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-xml\\" + year + "\\" + month):
        os.makedirs("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-xml\\" + year + "\\" + month)

def mystem2():
     if not os.path.exists ("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-plain\\" + year + "\\" + month):
        os.makedirs("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-plain\\" + year + "\\" + month)
     os.system("C:\\mystem.exe -cdi " + path + " C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-plain\\" +  year + "\\" + month +"\\" + str(i) + ".txt")

def cleaning_mystem_head(path2):
    file = open(path2, "r", encoding = "utf-8")
    array = file.readlines()
    file.close()
    array_head= array[0:5]
    body = ''.join(array[5:])
    array_ready=[]
    for string in array_head:
        stem = re.compile('({.+?})')
        string = stem.sub ('', string)
        array_ready.append(string)
    head_ready = ''.join(array_ready)
    final = head_ready + body 
    file = open (path2, "w", encoding = "utf-8")
    file.write(final)
    file.close

def txt_into_xml(path2, path3):
    file = open (path2, "r", encoding = "utf-8")
    final = file.read()
    file2 = open (path3, "w", encoding = "utf-8")
    file2.write(final)
    file.close()
    file2.close()
    
commonUrl = 'http://xn----8sbebnabwjokrslkgcu8a9d9f.xn--p1ai/article/'

for i in range(114658,114659):
        pageUrl = commonUrl + str(i)
        page=download_page(pageUrl)
        final=cleaning(neat_text(page))
        if final!= '':
            author_name = cleaning(author(page))
            article_name = cleaning(article(page))
            date_name = cleaning(date(page))
            category_name = cleaning(category(page))
            source = pageUrl
            year = ''.join(re.findall('\d{4}', date_name))
            month = ''.join(re.findall('\d{2}\.(\d{2})\.\d{4}', date_name))
            files(i)
            path = ("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\plain\\"+ year + "\\" + month + "\\"+ str(i) + ".txt")
            path2 = ("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-plain\\" +  year + "\\" + month +"\\" + str(i) + ".txt")
            path3 = ("C:\\Users\\Tanya\\Documents\\2term\\kili\\corpus\\mystem-xml\\" +  year + "\\" + month +"\\" + str(i) + ".xml")
            print(path, author_name, article_name, date_name, category_name, pageUrl, year)
            meta_data()
            mystem1()
            mystem2()
            cleaning_mystem_head(path2)
            txt_into_xml(path2, path3)
            


      
        

        
        

    
  
    
