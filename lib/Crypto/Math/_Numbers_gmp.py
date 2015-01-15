# ===================================================================
#
# Copyright (c) 2014, Legrandin <helderijs@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===================================================================

from Crypto.Util.py3compat import *


class _GMP(object):
    pass
_gmp = _GMP()

try:
    from cffi import FFI

    ffi = FFI()
    try:
        lib = ffi.dlopen("gmp")
    except OSError, desc:
        raise ImportError("Cannot load GMP library (%s)" % desc)

    ffi.cdef("""
        typedef struct { int a; int b; void *c; } MPZ;
        typedef MPZ mpz_t[1];
        typedef unsigned long        mp_bitcnt_t;
        void __gmpz_init_set (mpz_t rop, const mpz_t op);
        void __gmpz_init_set_ui (mpz_t rop, unsigned long op);
        int __gmpz_init_set_str (mpz_t rop, const char *str, int base);
        void __gmpz_set (mpz_t rop, const mpz_t op);
        int __gmpz_set_str (mpz_t rop, const char *str, int base);
        int __gmp_snprintf (char *buf, size_t size, const char *fmt, ...);
        void __gmpz_add (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_add_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        void __gmpz_sub_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        void __gmpz_addmul (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_addmul_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        void __gmpz_submul_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        void __gmpz_import (mpz_t rop, size_t count, int order, size_t size,
                            int endian, size_t nails, const void *op);
        void * __gmpz_export (void *rop, size_t *countp, int order, size_t size,
                              int endian, size_t nails, const mpz_t op);
        size_t __gmpz_sizeinbase (const mpz_t op, int base);
        void __gmpz_sub (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_mul (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_mul_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        int __gmpz_cmp (const mpz_t op1, const mpz_t op2);
        void __gmpz_powm (mpz_t rop, const mpz_t base, const mpz_t exp, const
                          mpz_t mod);
        void __gmpz_powm_ui (mpz_t rop, const mpz_t base, unsigned long exp,
                             const mpz_t mod);
        void __gmpz_pow_ui (mpz_t rop, const mpz_t base, unsigned long exp);
        void __gmpz_mod (mpz_t r, const mpz_t n, const mpz_t d);
        void __gmpz_neg (mpz_t rop, const mpz_t op);
        void __gmpz_and (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_ior (mpz_t rop, const mpz_t op1, const mpz_t op2);
        void __gmpz_clear (mpz_t x);
        void __gmpz_tdiv_q_2exp (mpz_t q, const mpz_t n, mp_bitcnt_t b);
        void __gmpz_fdiv_q (mpz_t q, const mpz_t n, const mpz_t d);
        void __gmpz_mul_2exp (mpz_t rop, const mpz_t op1, mp_bitcnt_t op2);
        int __gmpz_tstbit (const mpz_t op, mp_bitcnt_t bit_index);
        int __gmpz_perfect_square_p (const mpz_t op);
        int __gmpz_jacobi (const mpz_t a, const mpz_t b);
        void __gmpz_gcd (mpz_t rop, const mpz_t op1, const mpz_t op2);
        unsigned long __gmpz_gcd_ui (mpz_t rop, const mpz_t op1, unsigned long op2);
        int __gmpz_invert (mpz_t rop, const mpz_t op1, const mpz_t op2);
        int __gmpz_divisible_p (const mpz_t n, const mpz_t d);
        int __gmpz_divisible_ui_p (const mpz_t n, unsigned long d);
        """)

    null_pointer = ffi.NULL

    def c_ulong(x):
        return x

    def c_size_t(x):
        return x

    def new_mpz():
        return ffi.new("MPZ*")

    def create_string_buffer(size):
        return ffi.new("char[]", size)

    def get_c_string(c_string):
        return ffi.string(c_string)

    def get_raw_buffer(buf):
        return ffi.buffer(buf)[:]

except ImportError:

    from ctypes import (CDLL, Structure, c_void_p, c_ulong, c_int,
                        byref, c_size_t, create_string_buffer)
    from ctypes.util import find_library

    gmp_lib_path = find_library("gmp")
    if gmp_lib_path is None:
        raise ImportError("Cannot find GMP library")
    try:
        lib = CDLL(gmp_lib_path)
    except OSError, desc:
        raise ImportError("Cannot load GMP library (%s)" % desc)

    class _MPZ(Structure):
        _fields_ = [('_mp_alloc', c_int),
                    ('_mp_size', c_int),
                    ('_mp_d', c_void_p)]

    null_pointer = None

    def new_mpz():
        return byref(_MPZ())

    def get_c_string(c_string):
        return c_string.value

    def get_raw_buffer(buf):
        return buf.raw

# Unfortunately, all symbols exported by the GMP library start with "__"
# and have no trailing underscore.
# You cannot directly refer to them as members of the ctypes' library
# object from within any class because Python will replace the double
# underscore with "_classname_".
_gmp = _GMP()
_gmp.mpz_init_set = lib.__gmpz_init_set
_gmp.mpz_init_set_ui = lib.__gmpz_init_set_ui
_gmp.mpz_init_set_str = lib.__gmpz_init_set_str
_gmp.mpz_set = lib.__gmpz_set
_gmp.mpz_set_str = lib.__gmpz_set_str
_gmp.gmp_snprintf = lib.__gmp_snprintf
_gmp.mpz_add = lib.__gmpz_add
_gmp.mpz_add_ui = lib.__gmpz_add_ui
_gmp.mpz_sub_ui = lib.__gmpz_sub_ui
_gmp.mpz_addmul = lib.__gmpz_addmul
_gmp.mpz_addmul_ui = lib.__gmpz_addmul_ui
_gmp.mpz_submul_ui = lib.__gmpz_submul_ui
_gmp.mpz_import = lib.__gmpz_import
_gmp.mpz_export = lib.__gmpz_export
_gmp.mpz_sizeinbase = lib.__gmpz_sizeinbase
_gmp.mpz_sub = lib.__gmpz_sub
_gmp.mpz_mul = lib.__gmpz_mul
_gmp.mpz_mul_ui = lib.__gmpz_mul_ui
_gmp.mpz_cmp = lib.__gmpz_cmp
_gmp.mpz_powm = lib.__gmpz_powm
_gmp.mpz_powm_ui = lib.__gmpz_powm_ui
_gmp.mpz_pow_ui = lib.__gmpz_pow_ui
_gmp.mpz_mod = lib.__gmpz_mod
_gmp.mpz_neg = lib.__gmpz_neg
_gmp.mpz_and = lib.__gmpz_and
_gmp.mpz_ior = lib.__gmpz_ior
_gmp.mpz_clear = lib.__gmpz_clear
_gmp.mpz_tdiv_q_2exp = lib.__gmpz_tdiv_q_2exp
_gmp.mpz_fdiv_q = lib.__gmpz_fdiv_q
_gmp.mpz_mul_2exp = lib.__gmpz_mul_2exp
_gmp.mpz_tstbit = lib.__gmpz_tstbit
_gmp.mpz_perfect_square_p = lib.__gmpz_perfect_square_p
_gmp.mpz_jacobi = lib.__gmpz_jacobi
_gmp.mpz_gcd = lib.__gmpz_gcd
_gmp.mpz_gcd_ui = lib.__gmpz_gcd_ui
_gmp.mpz_invert = lib.__gmpz_invert
_gmp.mpz_divisible_p = lib.__gmpz_divisible_p
_gmp.mpz_divisible_ui_p = lib.__gmpz_divisible_ui_p


class Integer(object):

    _zero_mpz_p = new_mpz()
    _gmp.mpz_init_set_ui(_zero_mpz_p, c_ulong(0))

    def __init__(self, value):

        self._mpz_p = new_mpz()

        if isinstance(value, float):
            raise ValueError("A floating point type is not a natural number")

        if isinstance(value, (int, long)):
            if 0 <= value < 65536:
                _gmp.mpz_init_set_ui(self._mpz_p, c_ulong(value))
            else:
                if _gmp.mpz_init_set_str(self._mpz_p,
                                         tobytes(str(abs(value))),
                                         10) != 0:
                    _gmp.mpz_clear(self._mpz_p)
                    raise ValueError("Error converting '%d'" % value)
                if value < 0:
                    _gmp.mpz_neg(self._mpz_p, self._mpz_p)
        else:
            _gmp.mpz_init_set(self._mpz_p, value._mpz_p)

    # Conversions
    def __int__(self):

        # buf will contain the integer encoded in decimal plus the trailing
        # zero, and possibly the negative sign.
        # dig10(x) < log10(x) + 1 = log2(x)/log2(10) + 1 < log2(x)/3 + 1
        buf_len = _gmp.mpz_sizeinbase(self._mpz_p, 2) // 3 + 3
        buf = create_string_buffer(buf_len)

        _gmp.gmp_snprintf(buf, c_size_t(buf_len), b("%Zd"), self._mpz_p)
        return int(get_c_string(buf))

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return "Integer(%s)" % str(self)

    def to_bytes(self, block_size=0):
        """Convert the number into a byte string.

        This method encodes the number in network order and prepends
        as many zero bytes as required. It only works for non-negative
        values.

        :Parameters:
          block_size : integer
            The exact size the output byte string must have.
            If zero, the string has the minimal length.
        :Returns:
          A byte string.
        :Raises:
          ``ValueError`` if the value is negative or if ``block_size`` is
          provided and the length of the byte string would exceed it.
        """

        if self < 0:
            raise ValueError("Conversion only valid for non-negative numbers")

        buf_len = (_gmp.mpz_sizeinbase(self._mpz_p, 2) + 7) // 8
        if buf_len > block_size > 0:
            raise ValueError("Number is too big to convert to byte string"
                             "of prescribed length")
        buf = create_string_buffer(buf_len)

        _gmp.mpz_export(
                buf,
                null_pointer,  # Ignore countp
                1,             # Big endian
                c_size_t(1),   # Each word is 1 byte long
                0,             # Endianess within a word - not relevant
                c_size_t(0),   # No nails
                self._mpz_p)

        return bchr(0) * max(0, block_size - buf_len) + get_raw_buffer(buf)

    @staticmethod
    def from_bytes(byte_string):
        """Convert a byte string into a number.

        :Parameters:
          byte_string : byte string
            The input number, encoded in network order.
            It can only be non-negative.
        :Return:
          The ``Integer`` object carrying the same value as the input.
        """
        result = Integer(0)
        _gmp.mpz_import(
                        result._mpz_p,
                        c_size_t(len(byte_string)),  # Amount of words to read
                        1,            # Big endian
                        c_size_t(1),  # Each word is 1 byte long
                        0,            # Endianess within a word - not relevant
                        c_size_t(0),  # No nails
                        byte_string)
        return result

    # Relations
    def _apply_and_return(self, func, term):
        if not isinstance(term, Integer):
            term = Integer(term)
        return func(self._mpz_p, term._mpz_p)

    def __eq__(self, term):
        if not isinstance(term, (Integer, int, long)):
            return False
        return self._apply_and_return(_gmp.mpz_cmp, term) == 0

    def __ne__(self, term):
        if not isinstance(term, (Integer, int, long)):
            return True
        return self._apply_and_return(_gmp.mpz_cmp, term) != 0

    def __lt__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) < 0

    def __le__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) <= 0

    def __gt__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) > 0

    def __ge__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) >= 0

    def __nonzero__(self):
        return _gmp.mpz_cmp(self._mpz_p, self._zero_mpz_p) != 0

    def is_negative(self):
        return _gmp.mpz_cmp(self._mpz_p, self._zero_mpz_p) < 0

    # Arithmetic operations
    def __add__(self, term):
        result = Integer(0)
        if not isinstance(term, Integer):
            term = Integer(term)
        _gmp.mpz_add(result._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return result

    def __sub__(self, term):
        result = Integer(0)
        if not isinstance(term, Integer):
            term = Integer(term)
        _gmp.mpz_sub(result._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return result

    def __mul__(self, term):
        result = Integer(0)
        if not isinstance(term, Integer):
            term = Integer(term)
        _gmp.mpz_mul(result._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return result

    def __floordiv__(self, divisor):
        if not isinstance(divisor, Integer):
            divisor = Integer(divisor)
        if _gmp.mpz_cmp(divisor._mpz_p,
                        self._zero_mpz_p) == 0:
            raise ZeroDivisionError("Division by zero")
        result = Integer(0)
        _gmp.mpz_fdiv_q(result._mpz_p,
                        self._mpz_p,
                        divisor._mpz_p)
        return result

    def __mod__(self, divisor):
        if not isinstance(divisor, Integer):
            divisor = Integer(divisor)
        comp = _gmp.mpz_cmp(divisor._mpz_p,
                            self._zero_mpz_p)
        if comp == 0:
            raise ZeroDivisionError("Division by zero")
        if comp < 0:
            raise ValueError("Modulus must be positive")
        result = Integer(0)
        _gmp.mpz_mod(result._mpz_p,
                     self._mpz_p,
                     divisor._mpz_p)
        return result

    def __pow__(self, exponent, modulus=None):

        result = Integer(0)

        if modulus is None:
            if exponent < 0:
                raise ValueError("Exponent must not be negative")

            # Normal exponentiation
            result = Integer(0)
            if exponent > 256:
                raise ValueError("Exponent is too big")
            _gmp.mpz_pow_ui(result._mpz_p,
                            self._mpz_p,   # Base
                            c_ulong(int(exponent))
                            )
            return result
        else:
            # Modular exponentiation
            if not isinstance(modulus, Integer):
                modulus = Integer(modulus)
            if not modulus:
                raise ZeroDivisionError("Division by zero")
            if modulus.is_negative():
                raise ValueError("Modulus must be positive")
            if isinstance(exponent, (int, long)):
                if exponent < 0:
                    raise ValueError("Exponent must not be negative")
                if exponent < 65536:
                    _gmp.mpz_powm_ui(result._mpz_p,
                                     self._mpz_p,
                                     c_ulong(exponent),
                                     modulus._mpz_p)
                    return result
                exponent = Integer(exponent)
            elif exponent.is_negative():
                raise ValueError("Exponent must not be negative")
            _gmp.mpz_powm(result._mpz_p,
                          self._mpz_p,
                          exponent._mpz_p,
                          modulus._mpz_p)
            return result

    def __iadd__(self, term):
        if isinstance(term, (int, long)):
            if 0 <= term < 65536:
                _gmp.mpz_add_ui(self._mpz_p,
                                self._mpz_p,
                                c_ulong(term))
                return self
            if -65535 < term < 0:
                _gmp.mpz_sub_ui(self._mpz_p,
                                self._mpz_p,
                                c_ulong(-term))
                return self
            term = Integer(term)
        _gmp.mpz_add(self._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return self

    def __imul__(self, term):
        if isinstance(term, (int, long)):
            if 0 <= term < 65536:
                _gmp.mpz_mul_ui(self._mpz_p,
                                self._mpz_p,
                                c_ulong(term))
                return self
            if -65535 < term < 0:
                _gmp.mpz_mul_ui(self._mpz_p,
                                self._mpz_p,
                                c_ulong(-term))
                _gmp.mpz_neg(self._mpz_p, self._mpz_p)
                return self
            term = Integer(term)
        _gmp.mpz_mul(self._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return self

    def __imod__(self, divisor):
        if not isinstance(divisor, Integer):
            divisor = Integer(divisor)
        comp = _gmp.mpz_cmp(divisor._mpz_p,
                            divisor._zero_mpz_p)
        if comp == 0:
            raise ZeroDivisionError("Division by zero")
        if comp < 0:
            raise ValueError("Modulus must be positive")
        _gmp.mpz_mod(self._mpz_p,
                     self._mpz_p,
                     divisor._mpz_p)
        return self

    # Boolean/bit operations
    def __and__(self, term):
        result = Integer(0)
        if not isinstance(term, Integer):
            term = Integer(term)
        _gmp.mpz_and(result._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return result

    def __or__(self, term):
        result = Integer(0)
        if not isinstance(term, Integer):
            term = Integer(term)
        _gmp.mpz_ior(result._mpz_p,
                     self._mpz_p,
                     term._mpz_p)
        return result

    def __rshift__(self, pos):
        result = Integer(0)
        if not 0 <= pos < 65536:
            raise ValueError("Incorrect shift count")
        _gmp.mpz_tdiv_q_2exp(result._mpz_p,
                             self._mpz_p,
                             c_ulong(int(pos)))
        return result

    def __irshift__(self, pos):
        if not 0 <= pos < 65536:
            raise ValueError("Incorrect shift count")
        _gmp.mpz_tdiv_q_2exp(self._mpz_p,
                             self._mpz_p,
                             c_ulong(int(pos)))
        return self

    def __lshift__(self, pos):
        result = Integer(0)
        if not 0 <= pos < 65536:
            raise ValueError("Incorrect shift count")
        _gmp.mpz_mul_2exp(result._mpz_p,
                          self._mpz_p,
                          c_ulong(int(pos)))
        return result

    def __ilshift__(self, pos):
        if not 0 <= pos < 65536:
            raise ValueError("Incorrect shift count")
        _gmp.mpz_mul_2exp(self._mpz_p,
                          self._mpz_p,
                          c_ulong(int(pos)))
        return self

    def get_bit(self, n):
        """Return True if the n-th bit is set to 1.
        Bit 0 is the least significant."""

        if not 0 <= n < 65536:
            raise ValueError("Incorrect bit position")
        return bool(_gmp.mpz_tstbit(self._mpz_p,
                                    c_ulong(int(n))))

    # Extra
    def is_odd(self):
        return _gmp.mpz_tstbit(self._mpz_p, 0) == 1

    def is_even(self):
        return _gmp.mpz_tstbit(self._mpz_p, 0) == 0

    def size_in_bits(self):
        """Return the minimum number of bits that can encode the number."""

        if self < 0:
            raise ValueError("Conversion only valid for non-negative numbers")
        return _gmp.mpz_sizeinbase(self._mpz_p, 2)

    def is_perfect_square(self):
        return _gmp.mpz_perfect_square_p(self._mpz_p) != 0

    def fail_if_divisible_by(self, small_prime):
        """Raise an exception if the small prime is a divisor."""

        if isinstance(small_prime, (int, long)):
            if 0 < small_prime < 65536:
                if _gmp.mpz_divisible_ui_p(self._mpz_p,
                                           c_ulong(small_prime)):
                    raise ValueError("The value is composite")
                return
            small_prime = Integer(small_prime)
        if _gmp.mpz_divisible_p(self._mpz_p,
                                small_prime._mpz_p):
            raise ValueError("The value is composite")

    def multiply_accumulate(self, a, b):
        """Increment the number by the product of a and b."""

        if not isinstance(a, Integer):
            a = Integer(a)
        if isinstance(b, (int, long)):
            if 0 < b < 65536:
                _gmp.mpz_addmul_ui(self._mpz_p,
                                   a._mpz_p,
                                   c_ulong(b))
                return self
            if -65535 < b < 0:
                _gmp.mpz_submul_ui(self._mpz_p,
                                   a._mpz_p,
                                   c_ulong(-b))
                return self
            b = Integer(b)
        _gmp.mpz_addmul(self._mpz_p,
                        a._mpz_p,
                        b._mpz_p)
        return self

    def set(self, source):
        if not isinstance(source, Integer):
            source = Integer(source)
        _gmp.mpz_set(self._mpz_p,
                     source._mpz_p)
        return self

    def inverse(self, modulus):
        """Compute the inverse of this number in the ring of
        modulo integers.

        Raise an exception if no inverse exists.
        """

        if not isinstance(modulus, Integer):
            modulus = Integer(modulus)

        comp = _gmp.mpz_cmp(modulus._mpz_p,
                            self._zero_mpz_p)
        if comp == 0:
            raise ZeroDivisionError("Modulus cannot be zero")
        if comp < 0:
            raise ValueError("Modulus must be positive")

        result = Integer(0)
        _gmp.mpz_invert(result._mpz_p,
                        self._mpz_p,
                        modulus._mpz_p)
        if not result:
            raise ValueError("No inverse value can be computed")
        return result

    def gcd(self, term):
        """Compute the greatest common denominator between this
        number and another term."""

        result = Integer(0)
        if isinstance(term, (int, long)):
            if 0 < term < 65535:
                _gmp.mpz_gcd_ui(result._mpz_p,
                                self._mpz_p,
                                c_ulong(term))
                return result
            term = Integer(term)
        _gmp.mpz_gcd(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    @staticmethod
    def jacobi_symbol(a, n):

        if not isinstance(a, Integer):
            a = Integer(a)
        if not isinstance(n, Integer):
            n = Integer(n)
        if n <= 0 or n.is_even():
            raise ValueError("n must be positive even for the Jacobi symbol")
        return _gmp.mpz_jacobi(a._mpz_p, n._mpz_p)

    # Clean-up
    def __del__(self):

        try:
            if self._mpz_p is not None:
                _gmp.mpz_clear(self._mpz_p)
            self._mpz_p = None
        except AttributeError:
            pass
