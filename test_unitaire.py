import unittest

from fonctions_utiles import assign_rank, score_rank

class TestFonctions_utiles(unittest.TestCase):
    """
        Teste certaines fonctions de fonctions_utiles
    """
    def test_assign_rank(self):
        l = [1,7,3,6,5,3]
        l_rank = assign_rank(l)
        self.assertEqual(l_rank, [[1,6],[7,1],[3,4],[6,2],[5,3],[3,4]])

    def test_score_rank(self):
        y_rank = [[3, 11], [9, 3], [8, 5], [3, 11], [4, 9], [11, 1], [0, 15], [6, 7], [2, 13], [4, 9], [5, 8], [0, 15], [2, 13], [8, 5], [9, 3], [10, 2]]
        y_p_rank = [[4, 10], [10, 3], [8, 4], [3, 12], [5, 9], [13, 1], [2, 14], [6, 6], [3, 12], [4, 10], [6, 6], [2, 14], [2, 14], [8, 4], [6, 6], [11, 2]]
        (score, premier, podium) = score_rank(y_rank, y_p_rank)
        self.assertEqual((score, premier, podium),(0.6601891714363072, 1, 1))

if __name__ == '__main__':
    unittest.main()
    