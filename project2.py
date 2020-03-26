import math
import numpy as np
import matplotlib.pyplot as plot

x0 = 1000
a = 24693
c = 3517
K = 2**15

def random_num_generator(i, x):
    if i == 0:
        return x / K
    else: 
        x = (a * x + c) % K 
    return random_num_generator(i-1, x)

def random_num_generator_iter(i):
    count = i
    x = x0
    while count >= 0:
        if count == 0:
            return x / K
        else:
            x = (a * x + c) % K 
        count -= 1

def simulate_one_run(iteration_num):
    w = 0 
    num_calls = 1
    random_number = random_num_generator_iter(iteration_num)
    
    while True:
        if random_number < 0.2:
            w += 10
            random_number = random_number / 0.2
            if num_calls >= 4:
                return w
        elif random_number > 0.2 and random_number < 0.5:
            w += 32
            random_number = (random_number - 0.2) / 0.3
            if num_calls >= 4:
                return w
        else:
            x = -12 * math.log(1 - random_number)
            if x > 25:
                w += 32
                random_number = (random_number - 0.5) / 0.5
                if num_calls >= 4:
                    return w
            else:
                w += 6 + x
                return w
        num_calls += 1    

def simulate_n_times(n):
    w_times = []
    rand_nums_generated = []

    for k in range(0, n):
        w_times.append(simulate_one_run(k))

    return w_times
    
def less_than(w_times,val):
    count = 0
    for i in w_times:
        if i <= val:
            count += 1
    return count
    
def greater_than(w_times,val):
    count = 0
    for i in w_times:
        if i > val:
            count += 1
    return count

def collect_data(n):
    w_times = simulate_n_times(n)
    mean = np.mean(w_times)
    median = np.median(w_times)
    first_quartile = np.percentile(w_times, 25)
    third_quartile = np.percentile(w_times, 75)
    w15 = less_than(w_times, 15)
    w20 = less_than(w_times, 20)
    w30 = less_than(w_times, 30)
    w40 = greater_than(w_times, 40)
    w5 = greater_than(w_times, 60)
    w6 = greater_than(w_times, 110)
    w7 = greater_than(w_times, 125)
    
    print("Mean: {}".format(mean))
    print("Median: {}".format(median))
    print("First Quartile: {}".format(first_quartile))
    print("Third Quartile: {}".format(third_quartile))
    print("W <= 15: {}".format(w15/1000))
    print("W <= 20: {}".format(w20/1000))
    print("W <= 30: {}".format(w30/1000))
    print("W > 40: {}".format(w40/1000))
    print("W > W5 ({}): {}".format(60, w5/1000))
    print("W > W6 ({}): {}".format(110, w6/1000))
    print("W > W7 ({}): {}".format(127, w7/1000))
    
    values, bins = np.histogram (w_times, bins=25, normed=True)
    cum_values = np.cumsum(values)
    plot.plot(bins[1:], cum_values/cum_values[-1], 'o')
    plot.xlabel("W, seconds")
    plot.ylabel("$F(w)$")
    plot.title("CDF of W")
    plot.show()



collect_data(1000)
