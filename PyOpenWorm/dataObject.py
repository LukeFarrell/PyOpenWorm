import rdflib as R
from PyOpenWorm import DataUser, Configure

class DataObject(DataUser):
    """ An object backed by the database """
    # Must resolve, somehow, to a set of triples that we can manipulate
    # For instance, one or more construct query could represent the object or
    # the triples might be stored in memory.
    def __init__(self,ident="",triples=[],conf=False):
        DataUser.__init__(self,conf=conf)
        self._id = ident
        self._triples = triples

    def identifier(self):
        return R.URIRef(self._id)

    def triples(self):
        """ Should be overridden by derived classes to return appropriate triples
        :return: An iterable of triples
        """
        for x in self._triples:
            yield x

    def _n3(self):
        return ".\n".join( " ".join(y.n3() for y in x) for x in self.triples())

    def save(self):
        """ Write in memory data to the database. Derived classes should call this to update the store. """
        self.add_statements(self.triples())

    def uploader(self):
        """ Get the uploader for this relationship """
        uploader_n3_uri = self.conf['rdf.namespace']['uploader'].n3()
        q = """
        Select ?u where
        {
        GRAPH ?g {
        """+self._n3()+"""}

        ?g """+uploader_n3_uri+""" ?u.
        } LIMIT 1
        """
        qres = self.conf['rdf.graph'].query(q)
        uploader = None
        for x in qres:
            uploader = x['u']
            break
        return str(uploader)

    def upload_date(self):
        """ Get the date of upload for this relationship
        :return: the date(s) of upload for this object
        """
        upload_date_n3_uri = self.conf['rdf.namespace']['upload_date'].n3()
        q = """
        Select ?u where
        {
        GRAPH ?g {
        """+self._n3()+"""}

        ?g """+upload_date_n3_uri+""" ?u.
        } LIMIT 1
        """
        qres = self.conf['rdf.graph'].query(q)
        ud = None
        for x in qres:
            ud = x['u']
            break

        return str(ud)
