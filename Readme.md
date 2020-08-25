# Finders

Finders is a Python script with a CLI aimed to be used
in a functional automation environment to process info
from JSON files.
The main functions available are find_element and find_element_near_to.
The function find_element receives element A element name and
looks for the specific element or for the locator representing
the element A in the provided data set.
The function find_element_near_to receives an element A and
a locator X and returns the element object of the element
with locator X that is nearest to element A.

## Installation

For the sake of simplicity, no specific libraries are needed as dependency as
the Python standard library utilities are used and no
extra dependencies have been added.

This script has been tested with Python 3.8.3.

## Usage

finders.py -h will return help on how to use the script and information about the parameters

finders.py <element_a_name> will perform a find_element operation, returning the element
if if exist or None if it doesn't

finders.py <element_a_name> <locator_x> will perform a find_element_near_to operation,
returning the element closest to element A that matches the locator X.

## Considerations

- We assume that json1.json is the name of the initial json file to load and that is
available in the same directory as the script. The name of the initial json file to load
can be updated in the global constant available at the beginning of the script.
- The current implementation makes use of an auxiliar data structure to keep in memory
the information related to the elements provided in the data set. This is not efficient
for big data sets and more sophisticated tooling should be used instead for scalable
solutions. This is a quick and simple solution for the proposed requirement.
- Circular references have been controlled by keeping a list of opened files.
If a file has been loaded already then it won't be loaded again.
- Is it possible that jsonN.json files are loaded and this will impact in overall
system performance. We don't make any control over this and it's the operator main
responsibility to make sure the system is not overloaded.
- Elements are represented as Python dictionaries for simplicity.
We don't implement an Element class, which would be the more adequate thing to do.
Functions like get_position and get_size are simply extra keys.
- find_element_near_to will look for the closes element B to the element A that
matches locator X. We will discard the found element if it's the same element as
the one taken for reference (element A).
- find_element_near_to will not take into consideration the size of the element object.
We only consider the coordinates in which it is located.
- A better error handling and logging should be made. For automation sake, we should at
least add return POSIX compliant return codes (errno library in Python std) and add
different levels logging for easier debugging.
- A data set including json1.json, json2.json, json3.json is provided.
json4.json doesn't exist in purpose.
- When returning an element for any of the functions we return the element name and the
dictionary representing the element. E.g. { 'element_a': {'locator': '...',
'position': { 'x': 120, 'y': 150}} ...}
- Inline comments have been added in the script so it's easier to follow. If something has
not been contemplated, please let me know. I'm open for discussion on any of the design
decisions that has been made.
