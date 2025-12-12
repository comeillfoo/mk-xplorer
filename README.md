# mk-xplorer

Try to make Makefile parser for the it subsequent processing using other tools.

Based on the manual [Parsing Makefiles (GNU make)](https://www.gnu.org/software/make/manual/html_node/Parsing-Makefiles.html).

## Implementation goals

- [x] [Splitting long lines](https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html) ([ignoring recipe lines](https://www.gnu.org/software/make/manual/html_node/Splitting-Recipe-Lines.html))
- [x] [Comments](https://www.gnu.org/software/make/manual/html_node/Makefile-Contents.html)
- [x] Explicit rules - [Rule Syntax](https://www.gnu.org/software/make/manual/html_node/Rule-Syntax.html)
