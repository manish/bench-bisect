### Overview

Ever wanted to understand which git commit caused a performance regression for a specific code path? The process can be tedious if you do not have the right tools. You have to write a benchmark function and run it for every commit, capture the data, compare them and come to a conclusion.

What if it all happens for you? You provide a benchmark file with `main` as the entry method. Then you specify the start commit and optionally end commit.

Sit back and relax and you will get the results saved as json to your disk and additionally a chart generated for you to look through and come to the conclusion.