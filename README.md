# Infinite Crosswords
The most powerful AI the world has yet seen: ...<br/>
Me: I'd like some crosswords please.

Generates crosswords on any topic given as an input. Mostly done through brute force rather than brains, so key constraint is number of iterations. Set to ~1000 for a great crossword and a 20 minute wait, or ~20 for a good crossword right now. Outputs to a printable HTML file.

You'll need to create your own config.py file and add your API key to use the tool. See comments in app.py.

Run app.py to launch the program.

# Features not yet added:
- Identifying in the clue where multiple words are given. eg 'hot-dog' currently lists as (6) letters, but (3,3) would be better.

# Known bugs
- Short words that share the same letters with the start of long words, eg 'cat' into 'catapult' can appear in the clue list at the same location as the longer word.
