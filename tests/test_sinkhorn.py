import unittest

import numpy as np

from optimisation.sinkhorn import sinkhorn

class TestSinkhorn( unittest.TestCase ):

	def testSinkhorn( self ):
		"""

			Use the Sinkhorn algorithm to generate doubly-stochastic matrices
		
		"""
		m = 500
		n = 400
		tol = 1e-12
		r = np.ones( m )
		c = np.ones( n )

		A = np.random.uniform( size=( m, n ) )
		M = sinkhorn( A, r, c )

		# scaling factor
		mu = np.sum( c )/np.sum( r )
		
		# for arbitrary matrices the columns sums of M
		# should converge to the prescribed columns sums
		self.assertTrue( all( np.abs( np.sum( M, axis=0 ) - c ) ) < tol )

		# ..and the row sums of M should converge to 
		# 1/mu times the prescribed row sums
		self.assertTrue( all( np.abs( np.sum( M, axis=1 ) / mu - r ) ) < tol )
		
		n = 500
		c = np.ones( n )
		A = np.random.uniform( size=( m, n ) )
		M = sinkhorn( A, r, c )

		# for square matrices where the prescribed sums
		# are equal the row sums of M will converge to
		# the prescribed row sums
		self.assertTrue( all( np.abs( np.sum( M, axis=1 ) - r ) ) < tol )

