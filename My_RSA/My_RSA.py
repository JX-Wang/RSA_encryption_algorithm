#! /usr/bin/env python
# coding:utf-8
"""
RSA encryption algorithm
========================
date @ 2018.10.03
author @ WUD

Using way -> RSA(m).encryption()

Contact
wud@wangjunx.top, wjx.wud@gmail.com, 1411349759@qq.com

wud's blog
http://blog.wangjunx.top, https://github.com/JX-Wang
"""
import random  # 随机数产生
import math  # 对数运算

min = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
max = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


class RSA:
    """RSA class"""
    def __init__(self, m):
        """initial"""
        self.p = 0  # prime q
        self.q = 0  # prime p
        self.e = 0  # random e
        self.d = 0  # inverse of e
        self.n = 0  # p*q
        self.fn = 0  # fn = (p-1)*(q-1)
        self.prime = 0
        self.m = m

    @staticmethod
    def _miller_rabin_check(unchecked_prime):
        """This func is for checking a prime"""
        # print unchecked_prime
        if unchecked_prime % 2 == 0:  # 偶数不为素数
            return False
        for i in range(1, int(math.log(unchecked_prime-1, 2))+1):
            m = (unchecked_prime-1) / (2**i)
            if (m+1) % 2 == 0:  # 选出m
                # print "m is ", m
                k = i  # 选出k
                if unchecked_prime - 1 > 1000:  # 如果数字大于1000，在区间中选择2个a进行计算
                    test_time = 2
                    while test_time != 4:
                        a = random.randint(2, unchecked_prime-1)  # 产生随机数a∈(1,unchecked_prime-1)
                        # print test_time, "doing ", a, "^", m, "mod", unchecked_prime
                        # b = a**m % unchecked_prime  # 简单未优化的大数幂/模运算
                        b = pow(a, m, unchecked_prime)  # 调用math模块儿的pow函数
                        if b == 1 or b == unchecked_prime-1:
                            pass
                        else:
                            return False  # b!=±1 则不为素数
                        test_time += 1
                    return True
                else:
                    test_time = 2
                    while test_time != unchecked_prime - 1:
                        a = random.randint(2, unchecked_prime - 1)  # 产生随机数a∈(1,unchecked_prime-1)
                        # b = a ** m % unchecked_prime  # 简单未优化的幂/模运算
                        b = pow(a, m, unchecked_prime)  # 调用math模块儿的pow函数
                        if b == 1 or b == unchecked_prime - 1:
                            # print test_time
                            pass
                        else:
                            return False  # b!=±1 则不为素数
                        test_time += 1
                    return True
            else:  # 没有找到合适的m，增加k的值继续寻找
                pass
        return True  # 经过所有检测后没有错误则经过了miller_rabin素性检验，返回True

    @staticmethod
    def _check_five(unchecked_prime):
        str_num = str(unchecked_prime)
        if str_num.endswith("5") or str_num.endswith("0"):
            return False
        else:
            return True

    @staticmethod
    def _check_three(unchecked_prime):
        num_str = ""
        str_num = str(unchecked_prime)
        for i in str_num:
            num_str = num_str + i + "+"
        num_str = num_str[:-1]
        sum = eval(num_str)
        if sum % 3 == 0:
            return False
        else:
            return True

    def get_prime(self, a, b):
        """:return prime"""
        prime = random.randint(a, b)
        if (prime + 1) % 2 == 0:
            if self._check_three(prime):
                if self._check_five(prime):
                    if self._miller_rabin_check(prime):
                        # print "Uncheck prime is:", prime, "passed all check, it's a prime!"
                        self.prime = prime
                    else:
                        # print "Uncheck prime is:", prime, "can't pass miller rabin check, it's not a prime"
                        self.get_prime(a, b)
                else:
                    # print "Uncheck prime is:", prime, "can be divided by 5, so it's not a prime"
                    self.get_prime(a, b)
            else:
                # print "Uncheck prime is:", prime, "can be divided by 3, so it's not a prime"
                self.get_prime(a, b)
        else:
            # print "Uncheck prime is:", prime, "can be divided by 2, so it's not a prime"
            self.get_prime(a, b)

    def get_p_q(self):
        """This is function is for getting a large prime between MIN and MAX"""
        try:
            self.get_prime(min, max)
            self.p = self.prime
            self.get_prime(min, max)
            self.q = self.prime
            print "P is :", self.p, "\nQ is:", self.q
        except Exception as e:
            print "There must be something wrong in function -> _random_num:", str(e)

    def get_n_fn_e_d(self):
        """This function is for getting n, φ(n) and e"""
        self.n = self.p * self.q
        print "N is :", self.n
        self.fn =(self.p-1) * (self.q-1)
        print "FN is :", self.fn
        self.get_prime(2, self.fn)
        self.e = self.prime
        print "E is :", self.e
        self.d = self._inv_e(self.fn, self.e)
        print "D is :", self.d

    @staticmethod
    def _inv_e(n, e):
        """This function is for getting inverse of E"""
        counter_a = []
        counter_b = []
        N = n
        while n % e != 0:  # commit a[i]
            stmp_e = n % e
            a = (n-stmp_e)/e
            counter_a.append(a)
            stmp_n = (n-stmp_e)/a
            n, e = stmp_n, stmp_e  # exchange n,e  stmp_n,stmp_e
        size = len(counter_a)
        counter_b.append(counter_a[size-1])  # b[0] = a[n]
        counter_b.append(counter_a[size-2]*counter_b[0]+1)
        for i in range(2, size):
            counter_b.append(counter_a[size-i-1]*counter_b[i-1]+counter_b[i-2])
        if size%2==0:
            return counter_b[size-1]
        else:
            return N-counter_b[size-1]

    def encryption(self):
        print "RSA by Wangjunxiong: 2018.10.4"
        self.get_p_q()  # get prime p&q
        self.get_n_fn_e_d()  #
        c = pow(self.m, self.e, self.n)
        print "--------------------------------------------------------------"
        print "MESSAGE IS :0x%x"%m
        print "AFTER RSA ENCRYPT:0x%x"%c
        print "--------------------------------------------------------------"
        self.decryption(c)

    def decryption(self, c):
        m = pow(c, self.d, self.n)
        print "CIPHERTEXT IS:0x%x"%c
        print "AFTER RSA DECRYPT:0x%x"%m
        print "=============================================================="


if __name__ == '__main__':
    # RSA.get_prime()
    m = 0x123048024098240192abcdefbdbeacbabfeab4bf94b174e208742e4f27f4737498274b2348e80f00d808da595d5959f59595e95a959c9f341123f41231b12313f1313e123d1131c1231a121f131b13d123f
    RSA(m).encryption()

