# NaNoGenMo2016 Entry

This is a project to generate a 50,000+ word work of fiction.
It will take the form of sci-fi neurosurgery studies presented as scientific journal articles.
I plan to do this using:
* [STRIPS planning](https://en.wikipedia.org/wiki/STRIPS) with random preconditions and goals to generate experiment/operation plans.
I'm using [PyDDL](https://github.com/garydoranjr/pyddl) with a few wrapper classes to do the planning.
* [Context-free grammars](https://en.wikipedia.org/wiki/Context-free_grammar) to translate the studies to text.
I've made yet another clone of Tracery for that purpose. 
* Probably TeX to generate the end result.
