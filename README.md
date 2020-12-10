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

#### The `key-pos` condition
#### The `key-name` condition
#### The `layout-file-name` condition

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
