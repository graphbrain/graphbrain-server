# graphbrain-server

*NOTE:* This is highly experimental stuff, only meant for the core team at the moment.

## Installation

### Prerequisites (macOS)

Naturally, you can ignore the prerequisites that are already installed in your machine.

* XCode and the "Command Line Tools":

    $ xcode-select --install

* The [Homebrew package manager](http://brew.sh/).

* Python 3:

    $ brew install python3

* pip (Python package manager):

    $ sudo easy_install pip

* virtualenv (Virtual Python Environment builder):

    $ sudo -H pip install virtualenv


* LevelDB (database engine):

    $ brew install leveldb

### Installing from github

Start by cloning the source code to your current local directory.

    $ git clone https://github.com/graphbrain/graphbrain-server.git
    $ cd graphbrain-server

It is advisable to work with virtual environments. This avoids conflicts with the system-wide installed packages and creates a nice self-contained environment for you to work on.

To create a virtual environment in the current directory, do this (macOS):

    $ python3 -m venv venv

Then to switch to the virtual environment and install graphbrain-server:

    $ source venv/bin/activate
    $ pip install .


## Running a server

    $ gbserver run
