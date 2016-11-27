
# coding: utf-8

# In[1]:

import random
from tracery import Grammar, modifiers
import tracery_alterations
from collections import namedtuple
import pycorpora


# In[2]:

class Question(namedtuple('Question',
                          ['id','questions','answers','additional_tags'])):
    def instantiate(self, n=2):
        if n=='lambda':
            return (self.questions(), self.answers)
        else:
            return (self.questions(), [self.answers() for i in range(n)])


# In[3]:

def question_set(questions, max_qs=10, answers=2, exclude=[]):
    r = []
    tags = set(exclude)
    for i in range(max_qs):
        valid = [q for q in questions
                 if q.id not in tags
                 and all(qt not in tags for qt in q.additional_tags)]
        if len(valid) == 0:
            break
        q = random.choice(valid)
        r.append(q.instantiate(answers))
        tags.add(q.id)
        for t in q.additional_tags:
            tags.add(t)
    return r


# In[4]:

saint_titles = ['Saint ', 'Pope ', 'King ', 'Mother ']


# In[5]:

qg = Grammar({
        'animal':pycorpora.animals.common['animals'],
        'first_name_en':pycorpora.humans.firstNames['firstNames'],
        'last_name_en':pycorpora.humans.lastNames['lastNames'],
        'first_name_no':(pycorpora.humans.norwayFirstNamesBoys['firstnames_boys_norwegian'] +
                         pycorpora.humans.norwayFirstNamesGirls['firstnames_girls_norwegian']),
        'last_name_no':pycorpora.humans.norwayLastNames['lastnames_norwegian'],
        'first_name_es':pycorpora.humans.spanishFirstNames['firstNames'],
        'last_name_es':pycorpora.humans.spanishLastNames['lastNames'],
        'any_title':pycorpora.humans.englishHonorifics['englishHonorifics'],
        'object':[x.strip() for x in pycorpora.objects.objects['objects']
                  if x.strip()[-1] != 's'],# and len(x.split()) < 2
        'cluedo_suspect':pycorpora.games.cluedo['suspects']['Cluedo'],
        'cluedo_weapon':pycorpora.games.cluedo['weapons']['Cluedo'],
        'cluedo_room':pycorpora.games.cluedo['rooms'],
        'clue_suspect':pycorpora.games.cluedo['suspects']['Clue'],
        'clue_weapon':pycorpora.games.cluedo['weapons']['Clue'],
        'clue_room':pycorpora.games.cluedo['rooms'],
        'room':pycorpora.architecture.rooms['rooms'],
        'appliance':pycorpora.technology.appliances['appliances'],
        'strange_word':pycorpora.words.strange_words['words'],
        'name_suffix':pycorpora.humans.suffixes['suffixes'],
        'greek_god':pycorpora.mythology.greek_gods['greek_gods'],
        'greek_monster':pycorpora.mythology.greek_monsters['greek_monsters'],
        'greek_titan':pycorpora.mythology.greek_titans['greek_titans'],
        'celebrity':pycorpora.humans.celebrities['celebrities'],
        'street_core':([x.split()[-1] for x in pycorpora.humans.celebrities['celebrities']] +
                       [x.split()[-1] for x in pycorpora.humans.britishActors['britishActors']] +
                       pycorpora.geography.english_towns_cities['towns'] +
                       pycorpora.geography.english_towns_cities['cities'] +
                       pycorpora.geography.countries['countries'] +
                       [x['name'] for x in pycorpora.geography.oceans['oceans']] +
                       [x['name'] for x in pycorpora.geography.rivers['rivers']]),
        'saint':[x['saint'] if any(x['saint'].startswith(t)
                                   for t in saint_titles)
                 else 'Saint '+x['saint']
                 for x in pycorpora.religion.christian_saints],
        'pet':['#animal.a.capitalize#','#animal.a.capitalize#',
               '#animal.a.capitalize#','#animal.a.capitalize#',
               '#animal.a.capitalize#','#animal.a.capitalize#',
               '#animal.a.capitalize#','#animal.a.capitalize#',
               '#celebrity#'],
        'street_noun':['street','road','street','road','street','road',
                       'street','road','street','road','street','road',
                       'lane','avenue','close','way',
                       'lane','avenue','close','way',
                       'boulevard','alley','drive','crescent','court',
                       'hill', 'strand','end','prospect','gate'],
        'street_adjective':['old','new','west','east','north','south'],
        'small_cardinal':['two','three','four'],
        'street':['#street_core# #street_noun#','#street_core# #street_noun#','#street_core# #street_noun#',
                  '#street_core# #street_noun#','#street_core# #street_noun#','#street_core# #street_noun#',
                  '#street_adjective# #street_core# #street_noun#','#street_adjective# #street_core# #street_noun#',
                  '#street_adjective# #street_noun#',
                  '#street_adjective# #street_noun#',
                  '#small_cardinal# #street_core.s# #street_noun#',
                  'the #street_adjective# #street_noun#',
                  'the #street_noun#',
                  '#rare_street#'],
        'rare_street':['#street#','#street#','#street#',
                       '#real_rare_street#'],
        'real_rare_street':['whipmawhopma#street_noun#',
                            'whip-ma-whop-ma-#street_noun#',
                            #'#[street_core:#rude_word#]street#',
                            '#[street_core:#strange_word#]street#'],
        'greek_whatever':['#greek_god#','#greek_monster#','#greek_titan#'],
        'cluedo':['#cluedo_suspect#, in the #cluedo_room#, with the #cluedo_weapon#',
                  '#clue_suspect#, in the #clue_room#, with the #clue_weapon#'],
        'any_pronouns':['{subject}/{object}/{dependentPossessive}/{independentPossessive}/{reflexive}'.format(**pronouns)
                        for pronouns in pycorpora.humans.thirdPersonPronouns['thirdPersonPronouns']],
        'simple_pronouns':['he/him/his/his/himself',
                           'she/her/her/hers/herself',
                           'they/them/their/theirs/themself'],
        'pronouns':['#simple_pronouns#','#simple_pronouns#','#simple_pronouns#','#any_pronouns#'],
        'simple_title':['Mr','Mr','Mr','Mrs','Ms','Miss','Mx','Mx','Mx'],
        'title':['#simple_title#','#simple_title#','#simple_title#','#any_title#'],
        'first_name':['#first_name_en#','#first_name_en#','#first_name_en#',
                      '#first_name_no#','#first_name_es#'],
        'single_last_name':['#last_name_en#','#last_name_en#','#last_name_en#',
                     '#last_name_no#','#last_name_es#'],
        'last_name':['#single_last_name#','#single_last_name#',
                     '#single_last_name#-#single_last_name#'],
        'full_name_no_suffix':['#first_name# #last_name#',
                               '#first_name# #first_name# #last_name#'],
        'full_name':['#full_name_no_suffix#','#full_name_no_suffix#','#full_name_no_suffix#',
                     '#full_name_no_suffix# #name_suffix#'],
        'title_last':'#title# #last_name#',
        'title_full_name':'#title# #full_name#',
        'first_name_noun':['first name',
                           'given name','given name','given name','given name','given name',
                           'personal name','personal name','personal name','personal name',
                           'forename',
                           'Christian name'],
        'last_name_noun':['surname','surname','surname','surname',
                          'family name','family name','family name','family name','family name',
                          'last name'],
        'title_noun':['honorific','title'],
        'low_ordinal_number':['first','second','third','fourth','fifth',
                               'sixth','seventh','eighth','ninth','tenth',
                               'eleventh','twelth','thirteenth','fourteenth','fifteenth'],
        'numerated_object':['#object.a#','two #object.s#','three #object.s#',
                            'four #object.s#','five #object.s#','six #object.s#',
                            'seven #object.s#','eight #object.s#','nine #object.s#'],
        'object_collection_head':['#numerated_object#',
                                  '#object_collection_head#, #numerated_object#'],
        'object_collection':['#object_collection_head#, #numerated_object#, and #numerated_object#'],
        'receive_verb':['receive','get'],
        'maybe_x':['#x#',''],
        'cheese_noun':['cheese','cheese','cheese','cheese',
                       'curd','fermented dairy product',
                       'cheese, curd, or #[x:other ]maybe_x#fermented dairy product',
                       'cheese or #[x:other ]maybe_x#fermented dairy product',
                       'curd or #[x:other ]maybe_x#fermented dairy product',
                       'cheese or curd'],
        'room_question_clause':['were you born','was your first kiss',
                                'do you usually eat','do you usually sleep',
                                'do you keep your #[x:best ]maybe_x##appliance#',
                                'were you born','was your first kiss',
                                'do you usually eat','do you usually sleep',
                                'do you keep your #[x:best ]maybe_x##appliance#',
                                'do you keep your life savings'],
        'room_question':['What kind of room #room_question_clause# in?',
                         'In what kind of room #room_question_clause#?',
                         'Where #room_question_clause#?'],
        'room_answer':['#room.a.capitalize#',
                       'The #room#'],
        'new_or_emerging':['new', 'emerging', 'new or emerging'],
        'fabric_item':['duvet cover','coat','skirt','pair of trousers','pair of pants',
                       'bandana'],
        'fabric_question':['What is your favourite fabric?',
                           'What is your favourite fabric?',
                           'What is your favourite fabric?',
                           'What was your first #fabric_item# made of?',
                           'What was your first #fabric_item# made out of?',
                           'Of what fabric was your first #fabric_item# made?']
    })
qg.add_modifiers(modifiers.base_english)


# In[6]:

def add_religion(grammar, name, data):
    decorated_name = 'religion_{0}'.format(name)
    if isinstance(data, str):
        return data
    elif isinstance(data, list):
        rule = [add_religion(grammar, '{0}_{1}'.format(name,i), x)
                for (i, x) in enumerate(data)]
        grammar.push_rules(decorated_name, rule)
        return decorated_name
    elif isinstance(data, dict):
        rule = [k if len(v) == 0 else
                '#{0}#'.format(add_religion(grammar, k, v))
                for (k,v) in data.items()]
        grammar.push_rules(decorated_name, rule)
        return decorated_name
rg = Grammar({})
add_religion(rg, 'all',
             {'Atheism':{},
              'Agnosticism':{},
              'Theism':{'all_other':pycorpora.religion.religions,
                        'Christianity':{},
                        'Islam':{},
                        'Hinduism':{},
                        'Buddhism':{},
                        'Sikhism':{},
                        'Judaism':{}}})


# In[7]:

mg = Grammar({})
for planetish in pycorpora.science.planets['planets']:
    if len(planetish['moons']) > 0:
        mg.push_rules('{0}_moon'.format(planetish['name']),planetish['moons'])
mg.push_rules('moon',['#{0}_moon#'.format(planetish['name'])
                      for planetish in pycorpora.science.planets['planets']
                      if len(planetish['moons']) > 0])


# In[8]:

questions = [
    Question('first_name',
             lambda:qg.flatten('What is your #first_name_noun#?'),
             lambda:qg.flatten('#first_name#'),
             ()),
    Question('last_name',
             lambda:qg.flatten('What is your #last_name_noun#?'),
             lambda:qg.flatten('#last_name#'),
             ()),
    Question('title',
             lambda:qg.flatten('What is your #title_noun#?'),
             lambda:qg.flatten('#title#'),
             ()),
    Question('first_last_name',
             lambda:qg.flatten('What is your #first_name_noun# and #last_name_noun#?'),
             lambda:qg.flatten('#first_name# #last_name#'),
             ('first_name', 'last_name')),
    Question('full_name',
             lambda:qg.flatten('What is your full name?'),
             lambda:qg.flatten('#full_name#'),
             ('first_name','last_name')),
    Question('title_last_name',
             lambda:qg.flatten('What is your #title_noun# and #last_name_noun#?'),
             lambda:qg.flatten('#title# #last_name#'),
             ('title','last_name')),
    Question('title_full_name',
             lambda:qg.flatten('What is your #title_noun# and full name?'),
             lambda:qg.flatten('#title# #full_name#'),
             ('title', 'first_name', 'last_name')),
    Question('pronouns',
             lambda:qg.flatten('What are your pronouns?'),
             lambda:qg.flatten('#pronouns#'),
             ()),
    Question('birthday_presents',
             lambda:qg.flatten('What did you #receive_verb# for your #low_ordinal_number# birthday?'),
             lambda:qg.flatten('#object_collection.capitalize#'),
             ()),
    Question('cheese',
             lambda:qg.flatten('What is your favourite #cheese_noun#?'),
             lambda:random.choice(pycorpora.foods.curds['curds']).capitalize(),
             ()),
    Question('fruit',
             lambda:qg.flatten('What is your favourite fruit?'),
             lambda:random.choice(pycorpora.foods.fruits['fruits']).capitalize(),
             ('vegetable',)),
    Question('vegetable',
             lambda:qg.flatten('What is your favourite vegetable?'),
             lambda:random.choice(pycorpora.foods.vegetables['vegetables']).capitalize(),
             ()),
    Question('sandwich',
             lambda:qg.flatten('What is your favourite type of sandwich?'),
             lambda:random.choice(pycorpora.foods.sandwiches['sandwiches'])['name'].capitalize(),
             ('bread',)),
    Question('bread',
             lambda:qg.flatten('What is your favourite type of bread?'),
             lambda:random.choice(pycorpora.foods.breads_and_pastries['breads']).capitalize(),
             ()),
    Question('pastry',
             lambda:qg.flatten('What is your favourite type of pastry?'),
             lambda:random.choice(pycorpora.foods.breads_and_pastries['pastries']).capitalize(),
             ('bread',)),
    Question('pokemon',
             lambda:qg.flatten('What was the first Pokémon you caught?'),
             lambda:random.choice(pycorpora.games.pokemon['pokemon'])['name'],
             ('game',)),
    Question('wrestling',
             lambda:qg.flatten('What is your favourite professional wrestling move?'),
             lambda:random.choice(pycorpora.games.wrestling_moves['moves']).capitalize(),
             ('game',)),
    Question('cluedo',
             lambda:qg.flatten('What is your favourite Clue#[x:do]maybe_x# murder?'),
             lambda:qg.flatten('#cluedo#'),
             ('game',)),
    Question('pet',
             lambda:qg.flatten('What was your first pet?'),
             lambda:qg.flatten('#pet#'),
             ()),
    Question('dinosaur',
             lambda:qg.flatten('What is your favourite dinosaur?'),
             lambda:random.choice(pycorpora.animals.dinosaurs['dinosaurs']),
             ('pet',)),
    Question('room',
             lambda:qg.flatten('#room_question#'),
             lambda:qg.flatten('#room_answer#'),
             ()),
    Question('ism',
             lambda:"What is your favourite style of modern art?",
             lambda:random.choice(pycorpora.art.isms['isms']).title(),
             ('art',)),
    Question('colour',
             lambda:"What is your favourite colour?",
             lambda:random.choice(pycorpora.colors.xkcd['colors'])['color'].capitalize(),
             ('art',)),
    Question('firework',
             lambda:"What is your favourite firework?",
             lambda:random.choice(pycorpora.technology.fireworks['effects']).capitalize(),
             ('art',)),
    Question('knot',
             lambda:"What is your favourite knot?",
             lambda:random.choice(pycorpora.technology.knots['knots']).capitalize(),
             ('art',)),
    Question('car',
             lambda:"Who was the manufacturer of your first car?",
             lambda:random.choice(pycorpora.corporations.cars['cars']),
             ('technology',)),
    Question('lisp',
             lambda:"What is your favourite dialect of LISP?",
             lambda:random.choice(pycorpora.technology.lisp['lisps']),
             ('technology','geek')),
    Question('technology',
             lambda:qg.flatten("What is your favourite #new_or_emerging# technology?"),
             lambda:random.choice(pycorpora.technology.new_technologies['technologies']).capitalize(),
             ('technology','geek',)),
    Question('programming',
             lambda:'What was the first programming language you learned?',
             lambda:random.choice(pycorpora.technology.programming_languages),
             ('technology','geek')),
    Question('fabric',
             lambda:qg.flatten('#fabric_question#'),
             lambda:random.choice(pycorpora.materials.fabrics['fabrics']).capitalize(),
             ()),
    Question('gem',
             lambda:"What is your favourite gemstone?",
             lambda:random.choice(pycorpora.materials.gemstones['gemstones']).capitalize(),
             ()),
    Question('fluid',
             lambda:"What was the first bodily fluid you had to flush down the toilet?",
             lambda:random.choice(pycorpora.materials.get_file('abridged-body-fluids')['abridged body fluids']).capitalize(),
             ()),
    Question('building',
             lambda:"What material was the house you grew up in built from?",
             lambda:random.choice(pycorpora.materials.get_file('building-materials')['building materials']).capitalize(),
             ()),
    Question('prime',
             lambda:'What is your favourite prime number?',
             lambda:str(random.choice(pycorpora.mathematics.primes['primes'][:random.randint(1,999)])),
             ('maths','geek')),
    Question('author',
             lambda:'Who is your favourite author?',
             lambda:random.choice(pycorpora.humans.authors['authors']),
             ()),
    Question('job',
             lambda:'What is your current occupation?',
             lambda:random.choice(pycorpora.humans.occupations['occupations']).capitalize(),
             ()),
    Question('tv',
             lambda:'What is your favourite TV show?',
             lambda:random.choice(getattr(pycorpora,'film-tv').tv_shows['tv_shows']),
             ()),
    Question('music',
             lambda:'What is your favourite style of music?',
             lambda:random.choice(pycorpora.music.genres['genres']),
             ()),
    Question('greek',
             lambda:'Which figure in Greek mythology do you most identify with?',
             lambda:qg.flatten('#greek_whatever#'),
             ()),
    Question('flower',
             lambda:'What is your favourite flower?',
             lambda:random.choice(pycorpora.plants.flowers['flowers']).capitalize(),
             ()),
    Question('religion',
             lambda:'What is your religion?',
             lambda:rg.flatten('#religion_all#'),
             ()),
    Question('saint',
             lambda:'Who is your favourite Christian saint?',
             lambda:qg.flatten('#saint#'),
             ()),
    Question('element',
             lambda:'What is your favourite chemical element?',
             lambda:random.choice(pycorpora.science.elements['elements'])['name'],
             ('geek',)),
    Question('minor_planet',
             lambda:'What is your favourite minor planet?',
             lambda:random.choice(pycorpora.science.minor_planets['minor_planets']),
             ('geek','astronomy')),
    Question('planet',
             lambda:'What is your favourite planet?',
             lambda:random.choice(['Mercury','Venus','Earth','Mars',
                                   'Jupiter','Saturn','Uranus','Neptune']),
             ('astronomy')),
    Question('moon',
             lambda:'What is your favourite moon?',
             lambda:mg.flatten('#moon#'),
             ('astronomy','geek')),
    Question('headline',
             lambda:'What was the front page headline on the day you were born?',
             lambda:random.choice(pycorpora.words.crash_blossoms['crash_blossoms']),
             ('birth',)),
    Question('street',
             lambda:'What was the name of the street you grew up on?',
             lambda:qg.flatten('#street#').title(),
             ()),
]

