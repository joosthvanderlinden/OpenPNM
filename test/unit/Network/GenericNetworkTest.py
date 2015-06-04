import OpenPNM
import scipy as sp

class GenericNetworkTest:

    def setup_class(self):
        self.network = OpenPNM.Network.Cubic(shape=[10,10,10])

    def test_setitem(self):
        pass

    def test_find_connected_pores_numeric_not_flattend(self):
        a = self.network.find_connected_pores(throats=[0,1])
        assert sp.all(a.flatten() == [0, 1, 1, 2])

    def test_find_connected_pores_numeric_flattend(self):
        a = self.network.find_connected_pores(throats=[0,1], flatten=True)
        assert sp.all(a == [0, 1, 2])

    def test_find_connected_pores_boolean_flattend(self):
        Tind = sp.zeros((self.network.Nt,), dtype=bool)
        Tind[[0,1]] = True
        a = self.network.find_connected_pores(throats=Tind, flatten=True)
        assert sp.all(a == [0, 1, 2])

    def test_find_connected_pores_empty_flattend(self):
        a = self.network.find_connected_pores(throats=[], flatten=True)
        assert sp.shape(a) == (0,2)

    def test_find_neighbor_pores_numeric(self):
        a = self.network.find_neighbor_pores(pores=[])
        assert sp.size(a) == 0

    def test_find_neighbor_pores_boolean(self):
        Pind = sp.zeros((self.network.Np,), dtype=bool)
        Pind[[0,1]] = True
        a = self.network.find_neighbor_pores(pores=Pind)
        assert sp.all(a == [2, 10, 11, 100, 101])

    def test_find_neighbor_pores_numeric_union(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='union')
        assert sp.all(a == [1, 3, 10,  12, 100, 102])

    def test_find_neighbor_pores_numeric_intersection(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='intersection')
        assert sp.all(a == [1])

    def test_find_neighbor_pores_numeric_notintersection(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='not_intersection')
        assert sp.all(a == [3, 10, 12, 100, 102])

    def test_find_neighbor_pores_numeric_union_incl_self(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='union',
                                             excl_self=False)
        assert sp.all(a == [ 0, 1, 2, 3, 10, 12, 100, 102])
    def test_find_neighbor_pores_numeric_intersection_incl_self(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='intersection',
                                             excl_self=False)
        assert sp.all(a == [1])
    def test_find_neighbor_pores_numeric_notintersection_incl_self(self):
        a = self.network.find_neighbor_pores(pores=[0, 2],
                                             mode='not_intersection',
                                             excl_self=False)
        assert sp.all(a == [0, 2, 3, 10, 12, 100, 102])

    def test_find_neighbor_throats_empty(self):
        a = self.network.find_neighbor_throats(pores=[])
        assert sp.size(a) == 0

    def test_find_neighbor_throats_boolean(self):
        Pind = sp.zeros((self.network.Np,), dtype=bool)
        Pind[[0,1]] = True
        a = self.network.find_neighbor_throats(pores=Pind)
        assert sp.all(a == [ 0, 1, 900, 901, 1800, 1801])

    def test_find_neighbor_throats_numeric_union(self):
        a = self.network.find_neighbor_throats(pores=[0, 2], mode='union')
        assert sp.all(a == [ 0, 1, 2, 900, 902, 1800, 1802])

    def test_find_neighbor_throats_numeric_intersection(self):
        a = self.network.find_neighbor_throats(pores=[0, 2], mode='intersection')
        assert sp.size(a) == 0

    def test_find_neighbor_throats_numeric_notintersection(self):
        a = self.network.find_neighbor_throats(pores=[0, 2], mode='not_intersection')
        assert sp.all(a == [ 0, 1, 2,  900,  902, 1800, 1802])

    def test_num_neighbors_empty(self):
        a = self.network.num_neighbors(pores=[])
        assert sp.size(a) == 0

    def test_num_neighbors_boolean(self):
        Pind = sp.zeros((self.network.Np,), dtype=bool)
        Pind[0] = True
        a = self.network.num_neighbors(pores=Pind)
        assert a == 3

    def test_num_neighbors_numeric_flattened(self):
        a = self.network.num_neighbors(pores=[0,2], flatten=True)
        assert a == 6
        assert isinstance(a, int)

    def test_num_neighbors_numeric_notflattened(self):
        a = self.network.num_neighbors(pores=[0,2], flatten=False)
        assert sp.all(a == [3, 4])

    def test_num_neighbors_single_pore_notflattened(self):
        a = self.network.num_neighbors(pores=0, flatten=False)
        assert sp.all(a = [3])
        assert isinstance(a, sp.ndarray)

    def test_find_interface_throats(self):
        self.network['pore.domain1'] = False
        self.network['pore.domain2'] = False
        self.network['pore.domain3'] = False
        self.network['pore.domain1'][[0, 1, 2]] = True
        self.network['pore.domain2'][[5, 6, 7]] = True
        self.network['pore.domain3'][18:26] = True
        a = self.network.find_interface_throats(labels=['domain1', 'domain2'])
        assert a == [20]
        a = self.network.find_interface_throats(labels=['domain1', 'domain3'])
        assert sp.size(a) == 0



