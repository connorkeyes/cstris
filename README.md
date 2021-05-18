# cstris
CStris is a stacker game that you can use to challenge your friends. Play solo, or send and receive challenges over email.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](https://github.com/connorkeyes/cstris) under your own control, then clone your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd cstris
```

Use Anaconda to create and activate a new virtual environment, perhaps called "tetris-env":

```sh
conda create -n tetris-env python=3.8
conda activate tetris-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
pip install sendgrid
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)
> ALSO: Pygame apparently can have problems displaying on Macs. If this application fails to work on your Mac, try installing this specific version of Pygame: pip install pygame==2.0.0.dev4

## Setup

First, you must [acquire an API Key from Sendgrid.](https://sendgrid.com/docs/ui/account-and-settings/api-keys/)

Once you have done this, in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to specify your API Key and the email address you would like to send through:

    export SENDGRID_API_KEY = "API_KEY_HERE"
    export SENDER_ADDRESS = "example@gmail.com"

## Usage

Run the CStris script:

```py
python app/cstris.py
```

All other instructions, including how to play the game, are within the app itself.