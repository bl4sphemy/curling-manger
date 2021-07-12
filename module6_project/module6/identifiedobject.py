class IdentifiedObject:

    """
    Abstract Class for creating and returning an object id. We use this superclass to ensure
    all of the subsequent objects use an immutable has for their object id.
    """

    # Initializes an object with an OID (and sets current ID one higher)
    def __init__(self, oid):
        self._oid = oid

    # Use property decoration to get the instance id
    @property
    def oid(self):
        return self._oid
    # Two IndentifiedObjects are equal if they have the same type and the same oid
    def __eq__(self, other):
        return self._oid == other.oid
    # Return has code based on object's oid
    def __hash__(self):
        return hash(self._oid)
