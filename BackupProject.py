
# coding: utf-8

# In[1]:

from tracery import Grammar, modifiers
import random
import tracery_alterations
from Questions import question_set, questions, qg
import pycorpora
import uuid
import re
import unidecode
import inflect


# In[2]:

p = inflect.engine()


# In[3]:

def add_entry(entry, length_target=50000):
    global entries
    global wordcount
    entries.append(entry)
    delta_wc = len(entry.split())
    wordcount += delta_wc
    if wordcount >= length_target:
        return False
    return True


# In[4]:

def generate_entry(questionnaire):
    name = qg.flatten('#title_full_name#')
    name_simplified = unidecode.unidecode(name.lower())
    name_simplified = name_simplified.replace('.','')
    name_simplified = name_simplified.replace("'",'')
    splitname = re.split('[ -]',name_simplified)
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
    answers = tuple(q[1]() for q in questionnaire)
    data = """**userid**: `{0}`
**username**: `{1}`  
**name**: {2}  
**email**: `{3}`  
**password**: `{4}`  
""".format(uuid.uuid4(), username, name, email, password)
    data = data + '\n'.join("**{0}** {1}  ".format(q[0],a)
                            for (q,a) in zip(questionnaire, answers))+'  \n'
    answer_seed(answers, reset=True)
    data = data + "**Fortune**:  \n{0}\n\n".format(tell_fortune(answers))
    return data


# In[5]:

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
                  '#mail_adj##mail#.#tld#',
                  '#letter##mail#.#tld#',
                  '#mail_adj##mail#.#tld#',
                  '#mail##mail_adj#.#tld#'],
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


# In[6]:

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


# In[7]:

fg = Grammar({
        'attribute_verb':['are','have always been','were once',
                          'are not', 'have never been','were'],
        'present_attribute_statement':['#they.capitalize# are #[x:sometimes ]maybe_x##attribute.a# person.',
                                       '#they.capitalize# are not #[x:always ]maybe_x##attribute.a# person.'],
        'past_attribute_statement':['#they.capitalize# were once #attribute_more_less.a# person.',
                                    '#they.capitalize# were never #attribute_more_less.a# person.',
                                    '#they.capitalize# have always been #attribute.a# person.',
                                    '#they.capitalize# have not always been #attribute.a# person.'],
        'future_attribute_statement':['#they.capitalize# will #[x:one day ]maybe_x#become #attribute_more_less.a# person#[x: again]maybe_x#.',
                                      '#they.capitalize# will #[a:never][b:not]ab# become #attribute.a# person#[x: again]maybe_x#.',
                                      '#they.capitalize# will always be #attribute.a# person.',
                                      '#they.capitalize# will #[a:not always][b:sometimes]ab# be #attribute.a# person.'],
        'attribute_statement':['#past_attribute_statement#',
                               '#present_attribute_statement#',
                               '#future_attribute_statement#'],
        'attribute':['#attribute_quantifier# #attribute_adjective#',
                     '#attribute_quantifier# #attribute_adjective#',
                     '#attribute_adjective#'],
        'attribute_more_less':['#attribute_quantifier_more_less# #attribute_adjective#',
                               '#attribute_quantifier_more_less# #attribute_adjective#',
                               '#attribute_adjective#'],
        'attribute_adjective':pycorpora.humans.descriptions['descriptions'],
        'attribute_quantifier':['not at all','slightly','somewhat','quite','very','extremely'],
        'attribute_quantifier_more_less':['more','less','#attribute_quantifier#'],
        'maybe_x':['#x#',''],
        'ab':['#a#','#b#'],
        'subject':'#they#',
        'set_pronouns_you':'[they:you][them:you][their:your][theirs:yours][themself:yourself]',
        'set_pronouns_they':'[they:they][them:them][their:their][theirs:theirs][themself:themself]',
        'today_advice_head':['It is a good day to',
                             'Today is as good a day as any to'],
        'today_advice':['#today_advice_head# #verb_phrase#, #conditional_if#.',
                        '#today_advice_head# #verb_phrase#.'],
        'anytime_advice':[
            '#they# #[a:should][b:may wish to]ab##[x: take the time to]maybe_x# #verb_phrase#'],
        'again':['again','once more',
                 'again','once more',
                 'for the umpteenth time'],
        'platitude_verb_phrase':[
            'take #[a:new][b:more]ab# opportunities',
            'fall in love#[x: #again#]maybe_x#', 'relish life#[x: #again#]maybe_x#',
            'start something new', 'break with the old#[x: #again#]maybe_x#',
            'count #their# blessings', 'make a#[x: new]maybe_x# friend',
            'rekindle an old #[a:relationship][b:friendship]ab#'],
        'verb_phrase':[
            '#platitude_verb_phrase#',
            'become #[x:#attribute_quantifier_more_less# ]maybe_x##attribute_adjective#'],
        'conditional_if':['if #they# are #[x:#attribute_quantifier# ]maybe_x##attribute_adjective#',
                          'if #they# #verb_phrase#'],
        'conditional_when':['when #they# #verb_phrase#',
                            'when #they# #conditional_verb_phrase#'],
        'sense_verb':['see','hear','smell','touch','taste','sense','become aware of'],
        'conditional_verb_phrase':['#sense_verb# #omen#'],
        'omen':['#omen_noun##[x: on #day_descriptor.a#]maybe_x#',],
        'omen_noun':['the #omen_animal##[x: #omen_animal_verb#]maybe_x#',
                     '#omen_animal.a##[x: #omen_animal_verb#]maybe_x#',
                     '#omen_abstract#',
                     '#omen_sky.a#'],
        'omen_abstract':['danger','love in the air',
                         'new opportunities',
                         '#their# dreams #[a:coming true][b:slipping away]ab#',
                         ],
        'omen_animal':['#omen_animal_aux#','#omen_animal_aux#','#omen_animal_aux#',
                       '#month# #omen_animal_aux#','#omen_animal_aux# of #attribute_adjective#ness'],
        'omen_animal_aux':['#[x:dusk-]maybe_x#black cat',
                         '#[x:giant ]maybe_x#moth',
                         '#[x:vampire ]maybe_x#bat',
                         'unicorn','panther','ghost'],
        'omen_animal_verb':['prowling','revealing itself','in #their# life','escaping','dozing'],
        'omen_sky':['rainbow','eclipse','new star','comet','shooting star'],
        'day_descriptor':['#[x:#weather# ]maybe_x##[x:#month# ]maybe_x##day#',
                          '#[x:#weather# ]maybe_x##day##[x: of #month#]maybe_x#'],
        'month':['January','February','March','April',
                 'May','June','July','August',
                 'September','October','November','December',
                 'January','February','March','April',
                 'May','June','July','August',
                 'September','October','November','December',
                 'January','February','March','April',
                 'May','June','July','August',
                 'September','October','November','December',
                 'January','February','March','April',
                 'May','June','July','August',
                 'September','October','November','December',
                 'Sektober'],
        'time_of_day':['day','morning','afternoon',
                       'evening','evening','night','night'],
        'day':['#time_of_day#','#day_of_week#'],
        'day_of_week':['Monday','Tuesday','Wednesday','Thursday',
                       'Friday','Saturday','Sunday',
                       'Monday','Tuesday','Wednesday','Thursday',
                       'Friday','Saturday','Sunday',
                       'Monday','Tuesday','Wednesday','Thursday',
                       'Friday','Saturday','Sunday',
                       'Grunday'],
        'weather':['stormy','stormy','stormy',
                   'cold','cold','chilly','frosty',
                   'warm','pleasant','temperate',
                   'rainy','wet','snowy','unpleasant',
                   'turbulent','busy','disastrous',
                   'ominous'],
        'conditional_advice':['#conditional_if.capitalize#, #anytime_advice#.',
                              '#conditional_when.capitalize#, #anytime_advice#.',
                              '#conditional_when.capitalize#, #conditional_if# then #anytime_advice#.',
                              '#conditional_when.capitalize#, #anytime_advice#, #conditional_if#.'],
        'realise_dreams_verb':['realise','achieve','reach'],
        'artist':['Picasso','van Gogh','Monet','Mondrian','Rembrandt',
                  'Caravaggio','Klimt','Michelangelo','Vermeer','Raphael',
                  'Cézanne', 'Renoir'],
        'composition_type':['sonata','symphony','concerto','opera'],
        'baroque_composition_type':['sonata','suite','concerto'],
        'composer':['Beethoven','Mozart','Tchaikovsky','Mussorgsky',
                    'Mahler','Schubert','Schumann',
                    'Backer-Grøndahl'],
        'baroque_composer':['Bach','Handel','Vivaldi','Royer'],
        'composition':['#composer# #composition_type#',
                       '#composer# #composition_type#',
                       '#baroque_composer# #baroque_composition_type#',
                       '#composer# #composition_type#',
                       '#composer# #composition_type#',
                       '#baroque_composer# #baroque_composition_type#',
                       '#[a:#baroque_composition_type][b:composition_type]ab#'],
        'discovery':['new planet','new element',
                     '#[a:lost][b:missing]ab# #artist#',
                     '#[a:lost][b:missing]ab# #composition#'],
        'invention':['time travel','faster-than-light travel', 'teleportation',
                     'faster-than-light communication'],
        'prediction_verb_phrase':['find true love',
                                  '#realise_dreams_verb# #their# dreams',
                                  'discover #discovery.a#',
                                  'invent #invention#',
                                  'die #die_condition#'],
        'die_verbing':['singing','laughing','weeping','crying'],
        'die_condition':['alone', 'surrounded by friends',
                         'surrounded by family', 'surrounded by friends and family',
                         'with only a stranger to comfort #them#',
                         'in #their# sleep','in a #[a:fire][b:robbery]ab#',
                         '#conditional_when#', '#die_verbing#',
                         'when #they# are at #their# #[a:best][b:worst]ab#',
                         'when #they# are at #their# #[a:most][b:least]ab# #attribute_adjective#'],
        'approximately':['approximately','around','about'],
        'children':'#[x:#attribute_adjective# ]maybe_x#children',
        'have_child_verb':['have','adopt','give birth to','parent'],
        'prediction_aux_verb':['will','might','may'],
        'prediction_adverb_1':['possibly','probably','likely','most likely',],
        'prediction_adverb_2_positive':['one day','finally','in time',],
        'prediction_adverb_2':['never','not',
                               'one day','finally','in time'],
        'prediction_core':'#they# #prediction_aux_verb#'
                          '#[x: #prediction_adverb_1#]maybe_x#'
                          '#[x: #prediction_adverb_2#]maybe_x#'
                          ' #prediction_verb_phrase#',
        'prediction':['#prediction_core.capitalize#.',
                      '#prediction_core.capitalize#.',
                      '#prediction_core.capitalize#.',
                      '#conditional_if.capitalize#, #prediction_core#.',
                      '#prediction_core.capitalize#, #conditional_if#.',
                      '#conditional_when.capitalize#, #prediction_core#.'],
        'children_prediction_common':['#core.capitalize#.',
                                      '#core.capitalize#.',
                                      '#core.capitalize#.',
                                      '#conditional_if.capitalize#, #core#.',
                                      '#core.capitalize#, #conditional_if#.'],
        'no_children_prediction_core':'#they# #prediction_aux_verb#'
                                      '#[x: #prediction_adverb_1#]maybe_x# '
                                      '#no_children_prediction_verb_phrase#',
        'one_child_prediction_core':'#they# #prediction_aux_verb#'
                                    '#[x: #prediction_adverb_1#]maybe_x#'
                                    '#[x: #prediction_adverb_2_positive#]maybe_x# '
                                    '#one_child_prediction_verb_phrase#',
        'children_prediction_core':'#they# #prediction_aux_verb#'
                                    '#[x: #prediction_adverb_1#]maybe_x# '
                                    '#children_prediction_verb_phrase#',
        'no_children_prediction_verb_phrase':['#have_child_verb# no children',
                                              'never #have_child_verb# children',
                                              'not #have_child_verb# children'],
        'one_child_prediction_verb_phrase':['#have_child_verb# a child',
                                            '#[children_number:one][children:child]children_prediction_verb_phrase#'],
        'children_prediction_verb_phrase':['#have_child_verb# #children_number# #children#',
                                           '#have_child_verb# #children_number# #children#',
                                           '#have_child_verb# #approximately# #children_number# #children#',
                                           '#have_child_verb# at #[a:least][b:most]ab# #children_number# #children#'],
        'no_children_prediction':'#[core:#no_children_prediction_core#]children_prediction_common#',
        'one_child_prediction':'#[core:#one_child_prediction_core#]children_prediction_common#',
        'children_prediction':'#[core:#children_prediction_core#]children_prediction_common#',
    })
fg.add_modifiers(modifiers.base_english)


# In[8]:

def answer_seed(answers, reset=False, count=[0]):
    if reset:
        count[0] = 0
    random.seed(answers[count[0]%len(answers)])
    count[0] += 1


# In[9]:

def tell_fortune(answers, pronouns='set_pronouns_you',future_only=False,
                 identifier_subject='you', identifier_possessive='your',
                 max_child_fortunes=3):
    fortune = []
    answer_seed(answers)
    if not future_only:
        fortune.append(fg.flatten('#[#{0}#][they:{1}]attribute_statement#'.format(
                    pronouns,identifier_subject)))
    else:
        fortune.append(fg.flatten('#[#{0}#][they:{1}]future_attribute_statement#'.format(
                    pronouns,identifier_subject)))
    attribute_statement_count = random.randint(0,2)
    for i in range(attribute_statement_count):
        answer_seed(answers)
        if not future_only:
            fortune.append(fg.flatten('#[#{0}#]attribute_statement#'.format(pronouns)))
        else:
            fortune.append(fg.flatten('#[#{0}#]future_attribute_statement#'.format(pronouns)))
    if not future_only:
        answer_seed(answers)
        fortune.append(fg.flatten('#[#{0}#]today_advice#'.format(pronouns)))
    
    answer_seed(answers)
    conditional_advice_count = random.randint(0,3)
    for i in range(conditional_advice_count):
        answer_seed(answers)
        fortune.append(fg.flatten('#[#{0}#]conditional_advice#'.format(pronouns)))
    
    answer_seed(answers)
    personal_prediction_count = random.randint(0,3)
    for i in range(personal_prediction_count):
        answer_seed(answers)
        fortune.append(fg.flatten('#[#{0}#]prediction#'.format(pronouns)))
    
    answer_seed(answers)
    r = random.random()
    if r > 0.7:
        child_count = 0
    if r > 0.25:
        child_count = random.randint(0,1)
    if r > 0.1:
        child_count = random.randint(0,3)
    elif r > 0.003:
        child_count = random.randint(2,8)
    else:
        child_count = random.randint(4,20)
    child_prediction_count = random.randint(0,child_count)
    child_prediction_count = min(child_prediction_count,max_child_fortunes)
    
    answer_seed(answers)
    if child_count == 0:
        fortune.append(fg.flatten('#[#{0}#]no_children_prediction#'.format(pronouns)))
    elif child_count == 1:
        fortune.append(fg.flatten('#[#{0}#]one_child_prediction#'.format(pronouns)))
    else:
        fortune.append(fg.flatten(
                '#[#{0}#][children_number:{1}][children:children]children_prediction#'.format(
                    pronouns,
                    p.number_to_words(child_count))))
    fortunes = [' '.join(fortune)]
    answer_seed(answers)
    child_fortune_numbers = random.sample(list(range(child_count)),child_prediction_count)
    for child_number in child_fortune_numbers:
        fortunes.append(tell_fortune(
                answers,
                pronouns='set_pronouns_they',
                future_only=True,
                identifier_subject='{0} {1} child'.format(
                    identifier_possessive,
                    p.number_to_words(str(child_number+1)+'th')),
                identifier_possessive='{0} {1} child\'s'.format(
                    identifier_possessive,
                    p.number_to_words(str(child_number+1)+'th')),
                max_child_fortunes=max(0,max_child_fortunes-1)))
    fortune_text = '\n\n'.join(fortunes)
    return fortune_text


# In[10]:

entries = []
wordcount = 0
random.seed()
questionnaire = sorted(question_set(questions,
                                    max_qs=100,
                                    answers='lambda',
                                    exclude=['first_name','last_name','title']))
while add_entry(generate_entry(questionnaire),50000):
    random.seed()
print(wordcount)
print(len(entries))
story = '\n'.join(entries)
f = open('data_leak.md','w',encoding='utf-8')
f.write(story)
f.close()

