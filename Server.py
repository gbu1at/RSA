import math
from primes import get_random_prime, get_random_pair_prime


def my_gcd(a: int, b: int) -> tuple[int, int, int]:
    _b = b
    _a = a
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    if x < 0:
        k = (abs(x) // _b + 1)
        x += k * _b
        y -= k * _a

    d = a
    assert _a * x + _b * y == d
    return x, y, d


def fast_power(x: int, n: int, mod: int) -> int:
    res = 1
    while n > 0:
        if n % 2 == 1:
            res *= x

        n //= 2
        x *= x

        x %= mod
        res %= mod

    return res


class Server:
    def __init__(self, server_id: int, pair_primes: tuple[int, int]):

        self.server_id = server_id
        self.message: list[list[int, int]] = []

        self._p, self._q = pair_primes

        self.N = self._p * self._q

        self._fi_N = (self._p - 1) * (self._q - 1)

        self._close_key, self.open_key = self._generate_keys()

    def request(self, other, x: int):
        y = fast_power(x, other.open_key, other.N)
        other.response(self, y)

    def response(self, other, y: int):
        x = fast_power(y, self._close_key, self.N)
        self.message.append([other.server_id, x])

    def _generate_keys(self) -> [int, int]:
        while True:
            open_key = get_random_prime() % self._fi_N
            if math.gcd(open_key, self._fi_N) != 1:
                continue
            x, y, d = my_gcd(open_key, self._fi_N)
            _close_key = x

            assert (open_key * _close_key) % self._fi_N == 1

            return open_key, _close_key

    def show_last_message(self):
        self._print_message(self.message[-1])

    def _print_message(self, message):
        server_id, message = message
        print(f"Server {server_id} send for you message: {message}")

    def show_all_message(self):
        for message in self.message:
            self._print_message(message)


if __name__ == "__main__":
    # TEST
    server1 = Server(server_id=1, pair_primes=get_random_pair_prime())
    server2 = Server(server_id=2, pair_primes=get_random_pair_prime())
    server3 = Server(server_id=3, pair_primes=get_random_pair_prime())

    server3.request(server1, 3001)
    server3.request(server1, 3002)
    server2.request(server1, 2001)
    server3.request(server1, 3003)
    server2.request(server1, 2002)
    server2.request(server1, 2003)

    server1.show_all_message()
