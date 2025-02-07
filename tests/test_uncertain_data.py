# Copyright © 2021 United States Government as represented by the Administrator of the National Aeronautics and Space Administration. All Rights Reserved.

import unittest
from prog_algs.uncertain_data import UnweightedSamples, MultivariateNormalDist, ScalarData
from numpy import array


class TestUncertainData(unittest.TestCase):
    def test_unweightedsamples(self):
        empty_samples = UnweightedSamples()
        self.assertEqual(empty_samples.size, 0)
        try:
            empty_samples.sample()
            self.fail() # Cant sample from 0 samples
        except ValueError:
            pass

        empty_samples.append({'a': 1, 'b': 2})
        self.assertEqual(empty_samples.size, 1)
        self.assertDictEqual(empty_samples.mean, {'a': 1, 'b': 2})
        samples = empty_samples.sample()
        self.assertDictEqual(samples[0], {'a': 1, 'b': 2})
        self.assertEqual(samples.size, 1)

        s = UnweightedSamples([{'a': 1, 'b':2}, {'a': 3, 'b':-2}])
        self.assertDictEqual(s.mean, {'a': 2, 'b': 0})
        self.assertEqual(s.size, 2)
        samples = s.sample(10)
        self.assertEqual(samples.size, 10)
        del s[0]
        self.assertEqual(s.size, 1)
        k = s.keys()
        self.assertEqual(len(s.raw_samples()), 1)
        s[0] = {'a': 2, 'b': 10}
        self.assertDictEqual(s[0], {'a': 2, 'b': 10})
        for i in range(50):
            s.append({'a': i, 'b': 9})
        covar = s.cov
        self.assertEqual(len(covar), 2)
        self.assertEqual(len(covar[0]), 2)

        # Test median value
        data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 1, 'b': 4}, {'a': 2, 'b': 3}, {'a': 3, 'b': 1}]
        data = UnweightedSamples(data)
        self.assertEqual(data.median, {'a': 2, 'b': 3})

    def test_multivariatenormaldist(self):
        try: 
            dist = MultivariateNormalDist()
            self.fail()
        except Exception:
            pass
    
        dist = MultivariateNormalDist(['a', 'b'], array([2, 10]), array([[1, 0], [0, 1]]))
        self.assertDictEqual(dist.mean, {'a': 2, 'b':10})
        self.assertDictEqual(dist.median, {'a': 2, 'b':10})
        self.assertEqual(dist.sample().size, 1)
        self.assertEqual(dist.sample(10).size, 10)
        self.assertTrue((dist.cov == array([[1, 0], [0, 1]])).all())

    def test_scalardist(self):
        d = ScalarData(12)
        self.assertEqual(d.mean, 12)
        self.assertEqual(d.median, 12)
        self.assertListEqual(list(d.sample(10)), [12]*10)

# This allows the module to be executed directly    
def run_tests():
    l = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    print("\n\nTesting Uncertain Data")
    result = runner.run(l.loadTestsFromTestCase(TestUncertainData)).wasSuccessful()

    if not result:
        raise Exception("Failed test")

if __name__ == '__main__':
    run_tests()
