# KLE-Colouriser

A small shell script for applying colouring rules to KLE files.
When paired with [`keycov`][keycov], it makes it much easier to produce any insane colourway-pattern compatible with a diverse range of keyboards.

This script can also be used to create a single source of truth for colourising information.

## Table of Contents


<!-- vim-markdown-toc GFM -->

* [Setup](#setup)
* [Usage](#usage)
	* [Running the thing](#running-the-thing)
	* [Configuring colour-maps](#configuring-colour-maps)
		* [The `key-pos` condition](#the-key-pos-condition)
		* [The `key-name` condition](#the-key-name-condition)
		* [The `layout-file-name` condition](#the-layout-file-name-condition)
		* [The `all` condition](#the-all-condition)
		* [The `any` condition](#the-any-condition)
		* [The `not-all` condition](#the-not-all-condition)
		* [The `not-any` condition](#the-not-any-condition)
* [Caveats](#caveats)

<!-- vim-markdown-toc -->

## Setup

You’ll need a working installation of [python3][python3] and its package manager [pip3][pip3].
Download and unzip the [latest release][latest-release] then open up a terminal and type the following commands.
(These assume that the archive was unzipped in `~/Downloads/kle-colouriser/`.)

```bash
cd ~/Downloads/kle-colouriser/
pip3 install -r requirements.txt
python3 kle-colouriser.py --help
```

This last step should print out the usage information for `kle-colouriser`.

## Usage

### Running the thing

Before running, `kle-colouriser` will require two things:

1. A colour-map file to apply (this guide assumes `examples/colour-map.yml`)
2. A folderful of kle files to generate (we’ll call this `keebs/`)

To run `kle-colouriser`, open a terminal and type the following (assuming that the [latest release][latest-release] was unzipped to `~/Downloads/kle-colouriser/`.

```bash
cd ~/Downloads/kle-colouriser/
python3 kle-colouriser.py examples/colour-map.yml keebs/ colourised-keebs/
```

This will apply the example colour-map to the example layouts and output the results in the (new) `colourised-keebs/` directory.

### Configuring colour-maps

Colour-maps are just a list of simple condition-action rules written in the quite specific (and fairly common) markup language, [yaml][yaml].
Each colour-map rule specifies: its name, a colour to apply to caps, a colour to apply to legends and a set of conditions which must be satisfied in order to apply the rule.
Each keycap in a [KLE][kle] layout is then checked against the colour-map rules and the first with all conditions satisfied is then applied to that cap.
(That is, if two rules have satisfied conditions, that which appears higher in the colour-map file is used.)

A detailed account of `kle-colouriser`’s decisions can be found by increasing the verbosity level.
Passing `--verbosity=1` will show the rule chosen for each key in each layout.
Passing `--verbosity=2` will show the results of evaluating each condition within each rule for each key in each layout (there’s a lot of output).

The following is an example colour-map.

```yaml
- name: specials
  cap-colour: 'ffff00'
  glyph-style: '#ff8000'
  key-name:
  - Esc
  - Enter
- name: alphas
  cap-colour: '00ff00'
  glyph-style: '#ff0000;'
  key-pos: x + y <= 15
  key-name:
  - .-.+
  - '[^+/*-]'
  - ''
  - F[1-49][0-2]?
- name: something-else
  cap-colour: '123456'
  glyph-style: '123456'
  key-pos: 2 * x + 3 * y >= 10
- name: mods
  cap-colour: 'ff0000'
  glyph-style: '00ff00'
  key-name:
  - .*
```

#### The `key-pos` condition

It is possible to make the colour of the key depend on its position in a given layout.
For this, a mathematical condition may be specified.
Note that as per the [KLE][kle] standard, the value of `x` increases to the right, and the value of `y` _downwards._

Conditions are constructed as follows, closely following Python+C syntax.

- Numbers and the variables `x` and `y` are valid expressions
- The negation of an expression is also an expression
- A pair of expressions can be compared by any of the following binary operations.
	- `^^` power
    - `*`, multiplication
    - `/`, division, e.g. `3 / 2 = 1.5`
    - `//`, integer division, e.g. `3 // 2 = 1`
    - `%`, modulo, remainder of d, e.g. `3 % 2 = 1`
    - `+`, addition
    - `-`, subtraction
- A pair of expressions may be compared to form a condition
    - `<` less-than
    - `<=`, less-than-or-equal
    - `>`, greater-than
    - `>=`, greater-than-or-equal
    - `=`, equal
    - `==`, equal
    - `!=`, not equal
- A pair of conditions may be used in logical operations; this is also a condition:
	- `!` logical negation (`true` iff either but not both inputs are `true`)
	- `&` logical conjunction (`true` iff both inputs are `true`)
	- `|` logical disjunction (`true` iff either input is `true`)
	- `^` exclusive or (`true` iff either but not both inputs is `true`)

If a conditional operator is omitted, a value of `true` is returned _if and only if_ the numerical value resolved is not equal to zero.

Note that as only binary operations are considered, multiple comparisons can have unexpected results, such as the following.

```python
0.3 < 0.1 < 0.2
= 0.3 < (0.1 < 0.2)
= 0.3 < True
= 0.3 < 1
= True
```

Use the `&` operator instead: `a < b < c <=> a < b & b < c`.

#### The `key-name` condition

It is possible for the legend text of a key to be used to constrain colour-application.
The contents of the `key-name` field is either a string, or a list of strings, each of which represents a regular expression.
If the keycap legend matches any of the regular expressions specified, then the condition is `true`.
Any new-line characters present in the keycap legend are replaced by dashes, for example `!\n1` becomes `!-1`.

It’s not essential to know regular expressions, but a few basics such as those outlined below can make things a little more streamlined.
The cheatsheet and playground on [regexr][regex-playground] may be helpful.

Consider the example regular expression `.*`.
This comprises of `.`, which means match any _one_ character, and `*` which means repeat _zero or more_ of the regular expression to its left.
Hence `.*` just means that _anything,_ including the empty string, is matched.

Similarly, the regex `[0-9]` specifies a character class which means match any _one_ of the characters specified inside it.
Here a range from `0` to `9` is specified, hence this will match any single digit.
In the example colour-map, this concept is used in conjunction with the `?` operator which matches either _zero or one__ of the regular expression to its left.
This was used in the expression `F[1-49][0-2]?`, which when applied to a 100% keyboard will match keys F1 to F4 and F9 to F12.

#### The `layout-file-name` condition

It is possible to apply the same rule differently depending on the layout file to which it is applied.
This is done using regular expressions in the same way as the [`key-name`](#the-key-name-condition) condition.
If this is required, some diligent naming if input files may be useful.
For example, orthogonal layouts might have the word `ortho` as a part of their name, which would be matched by `.*ortho.*`.

#### The `all` condition

Takes a set of conditions as specified in this readme.
Returns `true` iff _every single one_ of its sub-conditions are `true`.

#### The `any` condition

Takes a set of conditions as specified in this readme.
Returns `true` iff _at least one_ of its sub-conditions are `true`.

#### The `not-all` condition

Takes a set of conditions as specified in this readme.
Negation of the `all` condition, returns `true` iff _at least one_ of its sub-conditions is `false`.

#### The `not-any` condition

Takes a set of conditions as specified in this readme.
Negation of the `any` condition, returns `true` iff _none_ of its sub-conditions is `true`.

## Caveats

Please note that given the quite organic nature of many keyboard layouts, some colour-map rules may be applicable to some but not others, and as such a human touch may occasionally be required.
For example, a 1u-wide stripe of colour at a 30° angle may work well for a 100% keyboard, but for an orthogonal one, a 45° angle may be required for the same visual effect due to aliasing (`kle-colouriser` will not support anti-aliasing).
To some extent it may be possible to adapt the colour-map rules slightly e.g. by using different rules with [`layout-file-name`](#the-layout-file-name-condition) conditions to react differently to problematic layout files.

The decision of whether to perfect already-good colour-map files or to simply amend problems by hand will entirely depend on the user’s workflow.
In the latter case, assuming reasonable colour-maps, the amount of work to fix these issues is likely less than that required to colourise the inputted layouts entirely manually.

[keycov]: https://github.com/TheSignPainter98/keycov
[kle]: http://www.keyboard-layout-editor.com "Keyboard layout editor"
[latest-release]: https://github.com/TheSignPainter98/kle-colouriser/releases/latest
[pip3]: https://pip.pypa.io/en/stable/
[python3]: https://www.python.org
[yaml]: https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html
