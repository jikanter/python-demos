from sumordflib import metameta
from rdflib import Graph
from pathlib import Path

def ingest(fname):
    content = ''
    with open(fname, 'r') as fd:
        content = fd.read()
    return content

"""
creates an RDF graph from an N3 file
Args:
fname: the name of the N3 file
Returns:
    the RDF graph
"""
def createRdfGraphFromN3File(fname):
    g = Graph(bind_namespaces="rdflib")
    content = None
    parsed = None
    p = Path(fname)
    if not (p.exists() and p.is_file()):
        raise IOError(f"file {fname} does not exist")
    with open(fname, 'r') as fd:
        content = fd.read()
    if content:
        parsed = g.parse(data=content, format="n3")
    return parsed

"""
creates an RDF/XML file from an N3 file
Args:
fname: the name of the N3 file
Returns:
    the RDF/XML file as a string
"""
def createRdfXmlFromN3File(fname):
    parsedGraph = createRdfGraphFromN3File(fname)
    return parsedGraph.serialize(format="xml")


