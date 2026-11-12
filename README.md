# SOREPY

A web application for tracking soreness when working out. I made this because I kept forgetting when was the last time I worked out a certain muscle and how long the muscle was sore after.

The app is entirely human made. No AI was used during any stage of development. Sorepy is a lightweight python app available trough any device that has an internet browser.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Installation

You can install the app using docker (recommended) or with pip.

### Installation using docker (recommended)

> [!NOTE]
> Prerequisites:
> - docker
> - docker compose

- Create a directory for storing the compose file and data (can be a separate directory if wanted)

`sudo mkdir /opt/docker/sorepy && cd /opt/docker/sorepy` 
- Download the compose.yaml to the sorepy directory

`sudo wget https://raw.githubusercontent.com/Phaenos/sorepy/refs/heads/main/compose.yaml` 
- Run with docker compose

`sudo docker compose up` 
- App available on {local ip}:5000

The docker container starts up and exposes port 5000 (you can change the port in the compose.yaml file if conflicting).

### Installation as a python app

> [!NOTE]
> Prerequisites:
> - python3
> - pip
> - venv

- Create a directory for the virtual environment

`mkdir $HOME/.sorepy && cd $HOME/.sorepy` 
- Create a python virtual environment

`python3 -m venv .venv` 
- Enter the venv (you can exit with `deactivate` when finished)

`source .venv/bin/activate` 
- Install using pip

`pip install sorepy` 
- While in the .venv environment start up the server (check the [gunicorn docs](https://gunicorn.org/) for further settings)

`gunicorn -w 1 -b 0.0.0.0:5000 sorepy:app` 
- Server is now available at {local ip}:5000 (stop with CTRL+c)

If you want to to autostart server check your init system docs. If you use Systemd, you can use included sorepy.service file. Change {username} to your username and put it in '$HOME/.config/systemd/user' Then run:

`systemctl --user daemon-reload` - to find the new service file

`systmectl --user start sorepy.service` - to start the server

`systmectl --user enable sorepy.service` - to automatically start server on startup

`systmectl --user status sorepy.service` - see the status of the service

`systmectl --user stop sorepy.service` - if you want to stop the server

## Usage

The UI is simple, everything is on the screen. The first screen shows a preview of todays and yesterdays workout and soreness with a textual description.

|Description|Days since last sore|
|---|---|
|never got sore|-|
|healed a while ago|>1|
|healed just on time|1|
|still sore|0|

With the *input* button you can input which muscle did you work out and which is sore for a selected date (today is automatically selected).

With the *history* button you can view data for each month.

## TODO

- [x] View history
- [ ] Authentication
- [ ] Multiple users
- [ ] Customizable muscles
- [ ] Customizable soreness descriptions
- [ ] Customizable soreness length

## Support

Please [open an issue](https://github.com/fraction/readme-boilerplate/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/fraction/readme-boilerplate/compare/).

## Buy me a coffee

[Buy me a coffee](https://buymeacoffee.com/phaenos) 
