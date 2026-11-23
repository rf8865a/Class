def fizzbuzz(n=100):
    """Print numbers from 1 to n with FizzBuzz rules.
    For multiples of 3, print 'Fizz' instead of the number.
    For multiples of 5, print 'Buzz' instead of the number.
    For multiples of both 3 and 5, print 'FizzBuzz'.
    """
    for i in range(1, n + 1):
        output = ''
        if i % 3 == 0:
            output += 'Fizz'
        if i % 5 == 0:
            output += 'Buzz'
        print(output or i)

if __name__ == "__main__":
    fizzbuzz()
