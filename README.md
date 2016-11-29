# NaNoGenMo2016 Entry

This is a project to generate a 50,000+ word work of fiction, as part of NaNoGenMo 2016.
It's [#9](https://github.com/NaNoGenMo/2016/issues/9) on the main repo.
It will take the form of sci-fi neurosurgery studies presented as scientific journal articles.
I plan to do this using:
* [STRIPS planning](https://en.wikipedia.org/wiki/STRIPS) with random preconditions and goals to generate experiment/operation plans.
I'm using [PyDDL](https://github.com/garydoranjr/pyddl) with a few wrapper classes to do the planning.
* [Context-free grammars](https://en.wikipedia.org/wiki/Context-free_grammar) to translate the studies to text. I'm using [Tracery for Python](https://github.com/aparrish/pytracery) for this.
* [corpora](https://github.com/dariusk/corpora) (via [pycorpora](https://github.com/aparrish/pycorpora)) as a source of details about experimental subjects.
* Probably TeX to generate the end result.

There's also a backup project: leaked user data from my defunct website, *The Greatest Personality Test And Fortune Telling Website In The World... Ever!*
The text can be found [here](https://github.com/serin-delaunay/NaNoGenMo2016/blob/master/output/data_leak_v2.md).
It's [#125](https://github.com/NaNoGenMo/2016/issues/125) on the main repo.

All output text ([output/](https://github.com/serin-delaunay/NaNoGenMo2016/blob/master/output)) is provided under the CC0 license.

<a href="http://creativecommons.org/publicdomain/zero/1.0/"><img src="http://i.creativecommons.org/p/zero/1.0/88x31.png"></a>

To the extent possible under law, [Serin Delaunay](https://github.com/serin-delaunay/NaNoGenMo2016) has waived all copyright and related or neighboring rights to NaNoGenMo 2016 entry text. This work is published from: United Kingdom.
