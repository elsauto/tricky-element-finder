#!/bin/python3

import argparse

# FIXME could use the errno lib to provide UNIX error codes
# to be consumed by automation scripts
import errno

import json
import math
import sys

MAIN_JSON="json1.json"


def _update_finders(name, elements):
    """Utility to replace finders provided in the data set
    with the desired element name

    Parameters
    ----------

    name : str
        Element name which will be used in the locator definitions

    elements : dict
        Representation of the data set

    Returns
    -------

    finders : list
       List with all finders present in the elements dict
       with actual value of the element name
    """

    finders = []

    # Iterate over filenames
    for f in elements.keys():
        # Iterate over keys (ElementN), import, __FINDERS__
        for ek in elements[f].keys():
            if (ek == '__FINDERS__'):
                # Get all possible finders and replace _ELEMENT_NAME_ with
                # element name
                finders.extend(elements[f][ek])

    for item in finders:
        item['locator'] = item['locator'].replace('_ELEMENT_NAME_', name)

    return finders


def find_element_by_locator(locator):
    """find_locator receives a locator and uses load_json()
    and get_elements() to find the element and return a list
    containing all the elements that matched with the search
    (or an empty list if None found)
    Used by exercise 2

    Parameters
    ----------

    locator : str
        Locator to retrieve elements from
        the data set

    Return
    ------

    all_elements : list
        List containing all the elements that matched with
        the search criteria

    Complexity
    ----------
    Best case == O(1)
    Worst case == O(n)
    """

    all_elements = []

    # Load JSON
    data = load_json(MAIN_JSON)

    elements = get_elements(data, locator)
    
    if elements:
        all_elements.extend(elements)

    return all_elements


def find_element(element):
    """Receives an element name and uses load_json() and
    get_elements() to find element and return an element
    object (or None if not found)

    Parameters
    ----------

    element : str
        The element to look for

    Returns
    -------

    element
        Element object or none

    Complexity
    ----------

    Best case == O(1)
    Worst case == O(n)
    """

    # Load JSON
    data = load_json(MAIN_JSON)

    # Search by key first

    # Iterate over filenames
    for f in data.keys():
        # Iterate over keys (ElementN), import, __FINDERS__
        for ek in data[f].keys():
            # If key == ElementN == element name
            if ek == element:
                return {ek : data[f][ek]}

    # Search by finders

    # Update finders
    finders = _update_finders(element, data)

    for locator in finders:
        elements = get_elements(data, locator['locator'])

        if elements:
            # Return first match
            # This could be optimized by returning element on first match
            # instead of getting all results and then returning the first
            return elements[0]

    return None


def load_json(filename, opened_files=[], elements={}):
    """Receives a JSON file and loads its content in the elements
    auxiliar structure. If an "import" key is found, the function
    will recurse and load the corresponding file.

    Parameters
    ----------

    filename : str
        The file path to load

    opened_files : list
        A list of files that has been opened
        Info required to avoid circular references

    elements : dict
        Representation of the data set

    Returns
    -------

    elements : dict
        Representation of the data set

    """
    try:
        with open(filename, 'r') as f:
            data = f.read()
            opened_files.append(filename)
            data_dict = json.loads(data)
            elements[filename] = data_dict
            if 'import' in data_dict:
                import_files = data_dict['import']
                for f in import_files:
                    if f not in opened_files:
                        load_json(f, opened_files, elements)
    except Exception as e:
        # FIXME Could be improved with proper logging
        print(e)

    return elements


def get_elements(elements, locator):
    """Receives a data set and a locator and returns
    a list of all elements objects found within this locator

    Parameters
    ----------

    elements : dict
        A representation of the data set

    locator : str
        A string representing a locator for a specific
        element object

    Returns
    -------

    match_elements : list
        Returns a list of all elements that matched
        the locator
    """

    match_elements = []

    # Iterate over filenames
    for f in elements.keys():
        # Iterate over keys (ElementN), import, __FINDERS__
        for ek in elements[f].keys():
            if (ek != 'import') and (ek != '__FINDERS__'):
                # Try to match data only in element objects
                if elements[f][ek]['locator'] == locator:
                    match_elements.append({ek : elements[f][ek]})

    return match_elements


def _distance_two_points(a_x, a_y, b_x, b_y):
    """Basic distance between two points
    formula

    Parameters
    ----------

    a_x : float
        Coordinate X for element A

    a_y : float
        Coordinate Y for element A

    b_x : float
        Coordinate X for element B

    b_y : float
        Coordinate Y for element B

    Returns
    -------

    distance : float
        Distance between A and B
    """
    return math.sqrt(((a_x-b_x)**2)+((a_y-b_y)**2))


def find_element_near_to(element, locator):
    """Receives an element A and a locator X
    and returns the element object of the element
    with locator X that is neareast to element A
    
    Parameters
    ----------

    element : str
        Element A name

    locator : str
        Locator X to look for closest to element A

    Returns
    -------

    element : dict
        Element with locator X that is nearest to element A
    """

    element_a = find_element(element)

    if not element_a:
        # We didn't find a matching element, return with empty dict
        return {}

    element_name = next(iter(element_a))

    element_a_x = float(element_a[element_name]['position']['x'])
    element_a_y = float(element_a[element_name]['position']['y'])

    coordinates_a = (element_a_x, element_a_y)

    all_elements_locator_x = find_element_by_locator(locator)

    shortest_distance = float("inf") # max float value
    element_shortest_distance = None

    for element in all_elements_locator_x:
        # Discard if it's the same element
        if not element == element_a:
            element_name = next(iter(element))
            element_x_x = float(element[element_name]['position']['x'])
            element_y_x = float(element[element_name]['position']['y'])
            coordinates_x = (element_x_x, element_y_x)
            distance = _distance_two_points(*coordinates_a, *coordinates_x)

            if distance < shortest_distance:
                shortest_distance = distance
                element_shortest_distance = element

    return element_shortest_distance


def main(argv):
   parser = argparse.ArgumentParser(description='Search elements in data set.')
   parser.add_argument('element', metavar='<element>', type=str,
                       help='element to search')
   parser.add_argument('locator', metavar='<locator>', type=str, nargs='?',
                       help='locator to search (optional)')
   args = parser.parse_args()

   if args.element and args.locator:
       print("The closest element to element %s that matches the locator %s is: "
               % (args.element, args.locator), find_element_near_to(args.element, args.locator))
   elif args.element:
       print("The search for %s resulted in the element: "
               % args.element, find_element(args.element))


if __name__ == "__main__":
    main(sys.argv[1:])
