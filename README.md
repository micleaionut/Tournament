This project contains the code to generate, run and test a Swiss-style[1] tournament results database. It is intended for educational purposes only in fulfillment of the "Project 2: Tournament Results" for the Udacity Full Stack Web Developer Nanodegree program.
 - VirtualBox installation
 - Vagrant installation
 - Get Vagrant VM from udacity fulstack-nanodegree-vm
 
 From a GitHub shell:
 1. cd Desktop\FSND-Virtual-Machine\vagrant
 2. vagrant up
 3. vagrant ssh
 4. cd /vagrant/tournament
 5. psql -f tournament.sql 
 6. python tournament_results.py (Success!  All tests pass!)