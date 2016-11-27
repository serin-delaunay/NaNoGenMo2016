
# coding: utf-8

# In[1]:

from tracery import Grammar, modifiers
import random
import tracery_alterations
from Questions import question_set, questions, qg
import pycorpora
import uuid


# In[2]:

def add_entry(entry, length_target=50000):
    global entries
    global wordcount
    entries.append(entry)
    delta_wc = len(entry.split())
    wordcount += delta_wc
    if wordcount >= length_target:
        return False
    return True


# In[3]:

g = Grammar({
        'address':'#nickname#@#domain#',
        'nickname_base':['#nick_noun_rev#',
                         '#nick_adjective_rev##nick_noun_rev#',
                         '#id_word_rev##nick_noun_rev#',
                         '#nick_adjective_rev##id_word_rev#',
                         '#nick_noun_rev##id_word_rev#',
                         '#nick_adjective_rev##nick_noun_rev##id_word_rev#'],
        'nickname':['#letter##nickname#',
                    '#nickname##letter#',
                    '#nickname##digit#',
                    '#nickname_base#',
                    '#nickname_base#',
                    '#nickname_base#'],
        'nick_noun':['#animal#',
                     '#person#'],
        'nick_noun_rev':['#nick_noun#','#nick_noun#','#nick_noun.reverse#'],
        'id_word_rev':['#id_word#','#id_word#','#id_word.reverse#'],
        'animal':[''.join(x.split()) for x in pycorpora.animals.common['animals']],
        #'animal_rev':['#animal#','#animal#','#animal.reverse#']
        'nick_adjective':['cool','super','superb','fantastic','fabulous',
                          'wonderful', 'wonder','cheeky','uber',
                          'incredible','incredi','geeky','geek',
                          'nerdy','nerd','sporty','smart','clever',
                          'northern','southern','western','eastern'],
        'nick_adjective_rev':['#nick_adjective#','#nick_adjective#','#nick_adjective.reverse#'],
        'person_aux':['boy','enbro','enby','fan','fanby','fenby',
                      'girl','guy','man','woman','person','jock','geek','nerd'],
        'person':['fan#person_aux#','cat#person_aux#','cow#person_aux#'],
        #'person_rev':['#person#','#person#','#person.reverse#'],
        'domain':['#letter##mail#.#tld#',
                  '#mail_adj##mail#.#tld#'],
        'tld':['com','org','net',
               'com','org','net',
               '#country_tld#',
               '#country_tld#',
               '#other_tld#'],
        'letter':[chr(ord('a')+i) for i in range(26)],
        'digit':[str(i) for i in range(10)],
        'mail':['mail','mail','mail',
                'post','crrl','box',
                'corr','poct','pocht',
                'past','mejl','dlvr'],
        'mail_adj':['fast','quick','kwk','speedy','rapid','rpd','vif','snel','snl',
               'hush','quiet','whisper','wspr','silent','slnt','tih','stil'],
        'country_tld':["ac","ad","ae","af","ag","ai","al","am","an","ao",
                       "aq","ar","as","at","au","aw","ax","az","ba","bb",
                       "bd","be","bf","bg","bh","bi","bj","bm","bn","bo",
                       "bq","br","bs","bt","bv","bw","by","bz","ca","cc",
                       "cd","cf","cg","ch","ci","ck","cl","cm","cn","co",
                       "cr","cu","cv","cw","cx","cy","cz","de","dj","dk",
                       "dm","do","dz","ec","ee","eg","eh","er","es","et",
                       "eu","fi","fj","fk","fm","fo","fr","ga","gb","gd",
                       "ge","gf","gg","gh","gi","gl","gm","gn","gp","gq",
                       "gr","gs","gt","gu","gw","gy","hk","hm","hn","hr",
                       "ht","hu","id","ie","il","im","in","io","iq","ir",
                       "is","it","je","jm","jo","jp","ke","kg","kh","ki",
                       "km","kn","kp","kr","kw","ky","kz","la","lb","lc",
                       "li","lk","lr","ls","lt","lu","lv","ly","ma","mc",
                       "md","me","mg","mh","mk","ml","mm","mn","mo","mp",
                       "mq","mr","ms","mt","mu","mv","mw","mx","my","mz",
                       "na","nc","ne","nf","ng","ni","nl","no","np","nr",
                       "nu","nz","om","pa","pe","pf","pg","ph","pk","pl",
                       "pm","pn","pr","ps","pt","pw","py","qa","re","ro",
                       "rs","ru","rw","sa","sb","sc","sd","se","sg","sh",
                       "si","sj","sk","sl","sm","sn","so","sr","ss","st",
                       "su","sv","sx","sy","sz","tc","td","tf","tg","th",
                       "tj","tk","tl","tm","tn","to","tp","tr","tt","tv",
                       "tw","tz","ua","ug","uk","us","uy","uz","va","vc",
                       "ve","vg","vi","vn","vu","wf","ws","ye","yt","za",
                       "zm","zw"],
        'other_tld':["academy","accountant","accountants","active","actor",
                     "adult","aero","agency","airforce","apartments","app",
                     "archi","army","associates","attorney","auction","audio",
                     "autos","band","bar","bargains","beer","best","bid",
                     "bike","bingo","bio","biz","black","blackfriday","blog",
                     "blue","boo","boutique","box","build","builders",
                     "business","buzz","cab","cafe","cam","camera","camp",
                     "cancerresearch","capital","cards","care","career",
                     "careers","cars","cash","casino","catering","center",
                     "ceo","channel","chat","cheap","christmas","church",
                     "city","claims","cleaning","click","clinic","clothing",
                     "cloud","club","coach","codes","coffee","college",
                     "community","company","computer","condos","construction",
                     "consulting","contractors","cooking","cool","coop",
                     "country","coupons","credit","creditcard","cricket",
                     "cruises","dad","dance","date","dating","day","deals",
                     "degree","delivery","democrat","dental","dentist",
                     "design","diamonds","diet","digital","direct","directory",
                     "discount","dog","domains","download","eat","education",
                     "email","energy","engineer","engineering","equipment",
                     "esq","estate","events","exchange","expert","exposed",
                     "express","fail","faith","family","fans","farm","fashion",
                     "feedback","finance","financial","fish","fishing","fit",
                     "fitness","flights","florist","flowers","fly","foo",
                     "football","forsale","foundation","fund","furniture",
                     "fyi","gallery","garden","gift","gifts","gives","glass",
                     "global","gold","golf","gop","graphics","green","gripe",
                     "guide","guitars","guru","healthcare","help","here",
                     "hiphop","hiv","hockey","holdings","holiday","homes",
                     "horse","host","hosting","house","how","info","ing","ink",
                     "institute","insure","international","investments",
                     "jewelry","jobs","kim","kitchen","land","lawyer","lease",
                     "legal","lgbt","life","lighting","limited","limo","link",
                     "loan","loans","lol","lotto","love","luxe","luxury",
                     "management","market","marketing","markets","mba","media",
                     "meet","meme","memorial","men","menu","mobi","moe",
                     "money","mortgage","motorcycles","mov","movie","museum",
                     "name","navy","network","new","news","ngo","ninja","one",
                     "ong","onl","online","ooo","organic","partners","parts",
                     "party","pharmacy","photo","photography","photos",
                     "physio","pics","pictures","pid","pink","pizza","place",
                     "plumbing","plus","poker","porn","post","press","pro",
                     "productions","prof","properties","property","qpon",
                     "racing","recipes","red","rehab","ren","rent","rentals",
                     "repair","report","republican","rest","review","reviews",
                     "rich","rip","rocks","rodeo","rsvp","run","sale","school",
                     "science","services","sex","sexy","shoes","show",
                     "singles","site","soccer","social","software","solar",
                     "solutions","space","studio","style","sucks","supplies",
                     "supply","support","surf","surgery","systems","tattoo",
                     "tax","taxi","team","store","tech","technology","tel",
                     "tennis","theater","tips","tires","today","tools","top",
                     "tours","town","toys","trade","training","travel",
                     "university","vacations","vet","video","villas","vision",
                     "vodka","vote","voting","voyage","wang","watch","webcam",
                     "website","wed","wedding","whoswho","wiki","win","wine",
                     "work","works","world","wtf","xxx","xyz","yoga","zone"],
        'bad_password':["123456","porsche","firebird","prince","rosebud",
                        "password","guitar","butter","beach","jaguar",
                        "12345678","chelsea","united","amateur","great","1234",
                        "black","turtle","7777777","cool","pussy","diamond",
                        "steelers","muffin","cooper","12345","nascar",
                        "tiffany","redsox","1313","dragon","jackson","zxcvbn",
                        "star","scorpio","qwerty","cameron","tomcat","testing",
                        "mountain","696969","654321","golf","shannon",
                        "madison","mustang","computer","bond007","murphy",
                        "987654","letmein","amanda","bear","frank","brazil",
                        "baseball","wizard","tiger","hannah","lauren","master",
                        "xxxxxxxx","doctor","dave","japan","michael","money",
                        "gateway","eagle1","naked","football","phoenix",
                        "gators","11111","squirt","shadow","mickey","angel",
                        "mother","stars","monkey","bailey","junior","nathan",
                        "apple","abc123","knight","thx1138","raiders","alexis",
                        "pass","iceman","porno","steve","aaaa","fuckme",
                        "tigers","badboy","forever","bonnie","6969","purple",
                        "debbie","angela","peaches","jordan","andrea","spider",
                        "viper","jasmine","harley","horny","melissa","ou812",
                        "kevin","ranger","dakota","booger","jake","matt",
                        "iwantu","aaaaaa","1212","lovers","qwertyui",
                        "jennifer","player","flyers","suckit","danielle",
                        "hunter","sunshine","fish","gregory","beaver","fuck",
                        "morgan","porn","buddy","4321","2000","starwars",
                        "matrix","whatever","4128","test","boomer","teens",
                        "young","runner","batman","cowboys","scooby",
                        "nicholas","swimming","trustno1","edward","jason",
                        "lucky","dolphin","thomas","charles","walter","helpme",
                        "gordon","tigger","girls","cumshot","jackie","casper",
                        "robert","booboo","boston","monica","stupid","access",
                        "coffee","braves","midnight","shit","love","xxxxxx",
                        "yankee","college","saturn","buster","bulldog","lover",
                        "baby","gemini","1234567","ncc1701","barney","cunt",
                        "apples","soccer","rabbit","victor","brian","august",
                        "hockey","peanut","tucker","mark","3333","killer",
                        "john","princess","startrek","canada","george",
                        "johnny","mercedes","sierra","blazer","sexy","gandalf",
                        "5150","leather","cumming","andrew","spanky","doggie",
                        "232323","hunting","charlie","winter","zzzzzz","4444",
                        "kitty","superman","brandy","gunner","beavis",
                        "rainbow","asshole","compaq","horney","bigcock",
                        "112233","fuckyou","carlos","bubba","happy","arthur",
                        "dallas","tennis","2112","sophie","cream","jessica",
                        "james","fred","ladies","calvin","panties","mike",
                        "johnson","naughty","shaved","pepper","brandon",
                        "xxxxx","giants","surfer","1111","fender","tits",
                        "booty","samson","austin","anthony","member","blonde",
                        "kelly","william","blowme","boobs","fucked","paul",
                        "daniel","ferrari","donald","golden","mine","golfer",
                        "cookie","bigdaddy","0","king","summer","chicken",
                        "bronco","fire","racing","heather","maverick","penis",
                        "sandra","5555","hammer","chicago","voyager","pookie",
                        "eagle","yankees","joseph","rangers","packers",
                        "hentai","joshua","diablo","birdie","einstein",
                        "newyork","maggie","sexsex","trouble","dolphins",
                        "little","biteme","hardcore","white","0","redwings",
                        "enter","666666","topgun","chevy","smith","ashley",
                        "willie","bigtits","winston","sticky","thunder",
                        "welcome","bitches","warrior","cocacola","cowboy",
                        "chris","green","sammy","animal","silver","panther",
                        "super","slut","broncos","richard","yamaha","qazwsx",
                        "8675309","private","fucker","justin","magic",
                        "zxcvbnm","skippy","orange","banana","lakers",
                        "nipples","marvin","merlin","driver","rachel","power",
                        "blondes","michelle","marine","slayer","victoria",
                        "enjoy","corvette","angels","scott","asdfgh","girl",
                        "bigdog","fishing","2222","vagina","apollo","cheese",
                        "david","asdf","toyota","parker","matthew","maddog",
                        "video","travis","qwert","121212","hooters","london",
                        "hotdog","time","patrick","wilson","7777","paris",
                        "sydney","martin","butthead","marlboro","rock","women",
                        "freedom","dennis","srinivas","xxxx","voodoo","ginger",
                        "fucking","internet","extreme","magnum","blowjob",
                        "captain","action","redskins","juice","nicole",
                        "bigdick","carter","erotic","abgrtyu","sparky",
                        "chester","jasper","dirty","777777","yellow","smokey",
                        "monster","ford","dreams","camaro","xavier","teresa",
                        "freddy","maxwell","secret","steven","jeremy",
                        "arsenal","music","dick","viking","11111111",
                        "access14","rush2112","falcon","snoopy","bill","wolf",
                        "russia","taylor","blue","crystal","nipple","scorpion",
                        "111111","eagles","peter","iloveyou","rebecca",
                        "131313","winner","pussies","alex","tester","123123",
                        "samantha","cock","florida","mistress","bitch","house",
                        "beer","eric","phantom","hello","miller","rocket",
                        "legend","billy","scooter","flower","theman","movie",
                        "6666","please","jack","oliver","success","albert"],
        'poor_password':['#bad_password#',
                         '#bad_password##id_word#',
                         '#id_word#',
                         '#id_word##bad_password#',
                         '#letter##poor_password#',
                         '#digit##poor_password#',
                         '#poor_password##letter#',
                         '#poor_password##digit#',
                         '#poor_password.reverse#',
                         '#poor_password.reverse#',
                         '#poor_password.reverse#']
    })
g.add_modifiers({'reverse':lambda text, *params: text[::-1]})


# In[4]:

possible_translations = {
    "A":["@","4","^","/\\","/-\\","aye"],
    "B":["8","6","13","|3","/3","ß","P>","|:"],
    "C":["©","¢","<","[","(","{"],
    "D":[")","|)","[)","?","|>","|o"],
    "E":["3","&","€","ë","[-"],
    "F":["ƒ","|=","/=","|#","ph"],
    "G":["6","9","&","C-","(_+","gee"],
    "H":["#","}{","|-|","]-[","[-]",")-(","(-)","/-/"],
    "I":["1","!","¡","|","]","eye"],
    "J":["]","¿","_|","_/","</","(/"],
    "K":["X","|<","|{","|("],
    "L":["|","1","£","|_","1_","¬"],
    "M":["|v|","|\\/|","/\\/\\","(v)","/|\\","//.","^^","em"],
    "N":["|\\|","/\\/","[\\]","<\\>","/V","^/"],
    "O":["0","()","[]","°","oh"],
    "P":["¶","|*","|o","|°","|\"","|>","9","|7","|^(o)"],
    "Q":["9","0_","()_","(_,)","<|"],
    "R":["2","®","/2","12","I2","l2","|^","|?","lz"],
    "S":["5","$","§","z","es"],
    "T":["7","+","†","-|-","']['"],
    "U":["µ","|_|","(_)","L|","v"],
    "V":["\\/","^"],
    "W":["VV","\\/\\/","\\\\'","'//","\\|/","\\^/","(n)"],
    "X":["%","*","><","}{",")(","ecks"],
    "Y":["¥","J","'/","j"],
    "Z":["2","7_","~/_",">_","%"]
}
obvious_translations = {
    "A":['@','4','/\\','/-\\'],
    "B":['8','6','|3'],
    "C":['<','[','('],
    "E":['3'],
    "H":['|-|','/-/','\\-\\'],
    "K":['|<'],
    "L":['1'],
    "M":["|v|","|\\/|","/\\/\\"],
    "N":["|\\|","/\\/"],
    "O":["0","()"],
    "S":["5","$","z"],
    "T":["7","+"],
    "U":["|_|"],
    "V":["\\/"],
    "W":["VV","\\/\\/"],
    "X":["%","><"],
    "Z":["2"]
}


# In[5]:

def generate_entry(questionnaire):
    name = qg.flatten('#title_full_name#')
    splitname = name.lower().split(' -')[1:-1]
    initials = ''.join(w[0] for w in splitname)
    id_words = [initials]+splitname
    g.push_rules('id_word',id_words)
    email = g.flatten('#address#')
    password = g.flatten('#poor_password#')
    username = g.flatten('#nickname#')
    g.pop_rules('id_word')
    password_rules = {
        ord(k.lower()):random.choice(v[:random.randint(1,len(v))])
        for (k,v) in random.sample(obvious_translations.items(),random.randint(3,10))
    }
    password = password.translate(password_rules)
    answers = [q[1]() for q in questionnaire]
    data = """userid: {0}.
username: "{1}".
name: {2}.
email: {3}.
password: "{4}".
""".format(uuid.uuid4(), username, name, email, password)
    data = data + '\n'.join("{0}\n    {1}".format(q[0],a)
                            for (q,a) in zip(questionnaire, answers))+'\n'
    data = data + "Fortune:\n{0}\n".format(tell_fortune(tuple(answers)))
    return data


# In[6]:

fg = Grammar({
        'attribute_verb':['are','have always been','were once',
                          'are not', 'have never been','were'],
        'attribute_statement':['You are #[x:sometimes ]maybe_x##attribute.a# person.','You are not #[x:always ]maybe_x##attribute.a# person.',
                               'You were once #attribute.a# person.','You were never #attribute.a# person.',
                               'You have always been #attribute.a# person.','You have not always been #attribute.a# person.',
                               'You will #[x:one day ]maybe_x#become #attribute.a# person#[x: again]maybe_x#.','You will #[a:never][b:not]ab# become #attribute.a# person#[x: again]maybe_x#.',
                               'You will always be #attribute.a# person.','You will #[a:not always][b:sometimes]ab# be #attribute.a# person.'],
        'attribute':['#attribute_quantifier# #attribute_adjective#',
                     '#attribute_quantifier# #attribute_adjective#',
                     '#attribute_adjective#'],
        'attribute_adjective':pycorpora.humans.descriptions['descriptions'],
        'attribute_quantifier':['not at all','slightly','somewhat','quite','very','extremely'],
        'maybe_x':['#x#',''],
        'ab':['#a#','#b#'],
    })
fg.add_modifiers(modifiers.base_english)


# In[7]:

def tell_fortune(answers):
    random.seed(answers)
    return fg.flatten('#attribute_statement#')


# In[8]:

entries = []
wordcount = 0
random.seed()
questionnaire = sorted(question_set(questions,
                                    max_qs=100,
                                    answers='lambda',
                                    exclude=['first_name','last_name','title']))
while add_entry(generate_entry(questionnaire),50000):
    pass
print(wordcount)
story = '\n'.join(entries)
f = open('data_leak.txt','w',encoding='utf-8')
f.write(story)
f.close()
