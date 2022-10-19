import numpy as np

"""

	Implementation of the Sinkhorn algorithm for rescaling a 
	matrix to have prescribed row and column sums:

		Diagonal Equivalence to Matrices with Prescribed Row and Column Sums
		Richard Sinkhorn, The American Mathematical Monthly, Vol. 74, No. 4 (Apr., 1967), pp. 402-405

"""

D1 = lambda x: np.diag( x )
D2 = lambda y: np.diag( y )

def _alpha( x, y, r, A ):

	return np.sum( D1( x ).dot( A.dot( D2( y ) ) ), axis=1 ) / r

def _beta( alpha, x, y, c, A ):

	return np.sum( np.diag( 1 / alpha ).dot( D1( x ).dot( A.dot( D2( y ) ) ) ), axis=0 ) / c

def _phi(x, y, r, A):
 
	m = _alpha( x, y, r, A )

	return np.max( m ) - np.min( m )


def sinkhorn( A, r, c, tol=1e-12 ):

	delta = np.sqrt( np.max( np.concatenate( ( r, c ) ) ) )
	a = np.sqrt( np.min( A ) )
	x = np.full( len( r ), delta / a )
	y = ( c * a ) / ( delta * np.sum( A, axis=0 ) )

	while ( _phi( x, y, r, A ) >= tol ):
	
		alpha = _alpha( x, y, r, A )
		beta = _beta( alpha, x, y, c, A )
		M = np.max( x / alpha )
		x =  ( delta * x ) / ( a * M * alpha )
		y = ( a * M * y ) / ( delta * beta )

	return D1( x ).dot( A.dot( D2( y ) ) )
