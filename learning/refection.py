#! /usr/local/bin/python3

import numpy 

def reflect_vector(incident_vector, normal_vector):
    """
    calculates the reflection vector of an incident vector off a surface normal.

    args:
        incident_vector (numpy.ndarray): the incoming vector (v).
        normal_vector (numpy.ndarray): the surface normal vector (n).

    returns:
        numpy.ndarray: the reflected vector (r).
    """
    # normalize the normal vector
    n = normal_vector / numpy.linalg.norm(normal_vector)

    # calculate the dot product of the incident vector and the normalized normal
    v_dot_n = numpy.dot(incident_vector, n)

    # apply the reflection formula: r = v - 2 * (v . n) * n
    reflected_vector = incident_vector - 2 * v_dot_n * n

    return reflected_vector

def main():
    # define the incident vector (e.g., a light ray direction)
    v = numpy.array([1.0, 2.0])
    # define the surface normal vector (it does not need to be normalized beforehand)
    normal = numpy.array([-1.0, 0.0])

    # Calculate the reflected vector
    reflected = reflect_vector(v, normal)

    print("Original vector =", v)
    print("Normal vector =", normal)
    print("Reflected vector =", reflected, "x=", reflected[0], "y=", reflected[1])
    return

if __name__ == "__main__":
    main()
