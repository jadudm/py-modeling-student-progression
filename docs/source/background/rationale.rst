Background and Rationale
=========

.. _msp_racket_bitbucket: 

There has been significant growth in CS departments over the past decade. And, as a department chair -- in particular, chair of a department that did not *yet* have a fixed curriculum -- that the course sequencing would matter. What do I mean by this?

A student wants to graduate, preferably in four years. They might have general requirements as well as requirements in a major (or minor, or whatever the unit of currency for the degree is). The question I had was this: **what course offering sequence maximized the number of students who could complete the requirements**?

This `led to an exploration in Racket <https://bitbucket.org/jadudm/modeling-student-progression/src/master/>`_, where I built a genetic algorithm to evolve optimized four-year course sequences. Each "semester" of the simulation, student agents (it was an agent-based-genetic-algorithm, I suppose) would enroll in classes, and then the fitness of each four-year window of time was assessed. More students graduated with better course sequences. 

Why?
----

When you have a finite number of faculty, and those faculty have different teaching strengths, you need to think about how to optimize your course offerings along many dimensions. That is not a problem people can do well in their heads. It is, however, something computers can do.

This project is a reworking of the original code from Racket to Python. This will make the project more accessible to more people, and sets up for the subsequent authoring of a paper on the project (to be written/to appear).