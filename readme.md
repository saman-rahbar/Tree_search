# N-K Problem

## Objectives
* To learn as much as you can about search.
* To work on a real practical problem.

## The N-K Problem
The problem is to get K packages delivered, using N vehicles.  Each package has a source and a destination.  The N vehicles start and end their routes at a garage.  A vehicle can carry 1 package at a time.

Underlying this problem is a map, i.e., a graph whose vertices are locations with unique labels (identification) and position in a Cartesian coordinate system.  This graph will have M locations.

The N-K problem has primary 3 parameters which can be set to adjust problem difficulty: N, K, and M.  Your preliminary work will use small values of N, K, and M, but you'll want to push these values up once you're beyond preliminary testing.  

**Note:** this is a hard search problem.  If you can't push N,K,M very far, don't stress.  Report on what you did.  Report on what the limitations are, and how you might address them.  At all times, your best attitude is to demonstrate how well you understand search as a result of working on this problem.  It's open ended, and "project-like" but keep in mind it is only 1 assignment out of 4.  

You may form groups within the class to write the implementation.  You must submit your own write-up.  Consulting and discussing the problem with any and everyone is completely acceptable.  You may make use of libraries and external implementations of various aspects of the problem, but you must cite them appropriately.  The key point of this assignment is that you learn something, and that you are able to describe what you've learned in your own words.  

## What to hand in:

* A PDF document with the following major headings:

* Group description.  Indicate the members of your group.
* Problem description.  Describe the problem, in your own words, and if you've made any variations.  This can be short; a paragraph or two will do.  This is simply to keep the document self-contained. 
* Solution description.  Discuss the aspects of the problem interpreted as search.  Include in your document any discussion of material found in AIMA that you feel a "client" would need to know to evaluate your approach, and decide whether to invest more money in your company.  Keep this to a page or so.  Most clients won't read long documents on background. 
* Implementation Description: This is the part of the report that explains your approach.  Don't explain anything that's common knowledge (e.g., don't talk about graphs, or BFS, or hash tables, or objects).  Talk about what your heuristics are, how you engineered the search to handle larger values of N,K,M.  Try to be concise, and refer to your implementation. The length depends on how much work you did, and how thoughtfully you tried to address some of the challenges.  3-5 pages at most.
* Results.  You'll want to solve a variety of initial set-ups of the problem to get a sense of how well your solution works.  Discuss the computation time to solve various values of N,K,M.  Show results as graphs or tables.  This section can be 1-2 pages, maybe a bit longer if you use a lot of graphs.  
* Conclusions.  Try to interpret your results, and project the viability of the approach beyond your prototype implementation.  Half a page or so will do.
* Appendix: Implementation.  Attach your implementation source code for review.  Don't worry about page length.  
