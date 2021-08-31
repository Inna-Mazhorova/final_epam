# Python code executor
## Epam final project

This is a simple web form for Python-code executing.
There are 2 input fields:
- code-field (must-have);
- stdin field (optional)

After pressing the "Launch"-button code is executed and stdout and stderr fields are filled in.
For security reasons import of os module and executing of exac and eval functions are prohibited.
Default timeout for execution is 10 seconds.

The program could be run:
- in a docker container;
- via cloning this repository

Shinx documentation can be seen here:
- https://final-epam.readthedocs.io/en/latest/main_launch.html#main_launch.compile
or here
- http://localhost:8000/docs  
  
