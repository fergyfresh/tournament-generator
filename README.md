# Tournament Generator
This project provides a Python module that uses a PostgreSQL database to keep
track of players and matches in a game tournament, using the Swiss pairing
system.

### How to run

This directory can be initiated with [Vagrant](https://www.vagrantup.com/)
by executing the command `vagrant up` within the `vagrant/` directory.  The
test cases can be run by executing the following commands:

`vagrant ssh`
`cd /vagrant/tournament`
`python tournament_test.py`
