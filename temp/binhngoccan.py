# import math
#
#
# def run_case():
#     n, x, y = map(int, input().split())
#     my_gcd = math.gcd(x, y)
#     x = int(x / my_gcd)
#     y = int(y / my_gcd)
#     a = []
#     b = []
#     for i in range(n):
#         ai, bi = map(int, input().split())
#         # print(math.gcd(ai, bi), math.lcm(ai, bi))
#         my_gcd = math.gcd(ai, bi)
#         ai /= my_gcd
#         bi /= my_gcd
#         # print(int(ai), int(bi))
#         a.append(int(ai))
#         b.append(int(bi))
#     ra = a[0]
#     rb = b[0]
#     for i in range(n-1):
#         my_lcm = math.lcm(rb, b[i+1])
#         ra = int(ra*(my_lcm/rb)+a[i+1]*(my_lcm/b[i+1]))
#         rb = my_lcm
#         my_gcd = math.gcd(ra, rb)
#         ra = int(ra/my_gcd)
#         rb = int(rb/my_gcd)
#     print(ra, rb)
#     if ra == x and rb == y:
#         print('Yes')
#     else:
#         print('No')
#
#
# t = int(input())
# for i in range(t):
#     run_case()
t = int(input())
while t > 0:
    t -= 1
    N = int(input())
    i = 1/(N + 1)
    print(i * 10**9)
